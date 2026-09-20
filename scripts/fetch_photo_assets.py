#!/usr/bin/env python3
"""Fetch rights-cleared photograph source candidates reproducibly.

This script downloads only URLs declared in an explicit batch manifest, enforces
an allowlist, validates the payload as a real raster image, records SHA-256 and
pixel dimensions, and links the downloaded source file back to
assets/photo-source-registry.json.

Downloaded files are SOURCE CANDIDATES, not automatically final layout assets.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener, HTTPRedirectHandler

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "assets" / "photo-source-registry.json"
OUTPUT_DIR = ROOT / "assets" / "photos" / "a-core" / "source-candidates"
OUTPUT_MANIFEST = OUTPUT_DIR / "photo-source-files.json"

ALLOWED_HOSTS = {
    "www.ars.usda.gov",
    "upload.wikimedia.org",
    "thumb.wikimedia.org",
}
MAX_BYTES = 30 * 1024 * 1024
MAX_FETCH_ATTEMPTS = 5
RETRY_DELAYS_SECONDS = (2, 5, 10, 20)


class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        host = (urlparse(newurl).hostname or "").lower()
        if host not in ALLOWED_HOSTS:
            raise RuntimeError(f"redirect blocked to non-allowlisted host: {host}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def fetch_bytes(url: str) -> bytes:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise RuntimeError(f"only HTTPS is allowed: {url}")
    host = (parsed.hostname or "").lower()
    if host not in ALLOWED_HOSTS:
        raise RuntimeError(f"host not allowlisted: {host}")

    req = Request(
        url,
        headers={
            "User-Agent": "Practical-Beekeeping-Handbook/1.0 photo-source-fetch",
            "Accept": "image/*",
        },
    )
    opener = build_opener(SafeRedirect())
    for attempt in range(1, MAX_FETCH_ATTEMPTS + 1):
        try:
            with opener.open(req, timeout=60) as response:
                final_host = (urlparse(response.geturl()).hostname or "").lower()
                if final_host not in ALLOWED_HOSTS:
                    raise RuntimeError(f"final host not allowlisted: {final_host}")
                length = response.headers.get("Content-Length")
                if length and int(length) > MAX_BYTES:
                    raise RuntimeError(f"payload too large: {length} bytes")
                data = response.read(MAX_BYTES + 1)
                if len(data) > MAX_BYTES:
                    raise RuntimeError("payload exceeded maximum allowed size")
                return data
        except HTTPError as exc:
            retryable = exc.code in {429, 500, 502, 503, 504}
            if not retryable or attempt == MAX_FETCH_ATTEMPTS:
                raise
            retry_after = exc.headers.get("Retry-After")
            delay = int(retry_after) if retry_after and retry_after.isdigit() else RETRY_DELAYS_SECONDS[attempt - 1]
            print(f"HTTP {exc.code} for {url}; retrying in {delay}s", file=sys.stderr)
            time.sleep(delay)
        except URLError:
            if attempt == MAX_FETCH_ATTEMPTS:
                raise
            delay = RETRY_DELAYS_SECONDS[attempt - 1]
            print(f"Network error for {url}; retrying in {delay}s", file=sys.stderr)
            time.sleep(delay)

    raise RuntimeError(f"failed to fetch after {MAX_FETCH_ATTEMPTS} attempts: {url}")


def inspect_image(data: bytes):
    bio = BytesIO(data)
    with Image.open(bio) as im:
        im.verify()
    bio.seek(0)
    with Image.open(bio) as im:
        fmt = (im.format or "").upper()
        width, height = im.size
        mode = im.mode
    if fmt not in {"JPEG", "PNG"}:
        raise RuntimeError(f"unsupported raster format: {fmt}")
    return fmt, width, height, mode


def extension_for(fmt: str) -> str:
    return ".jpg" if fmt == "JPEG" else ".png"


def effective_size(width: int, height: int, ppi: int = 300):
    inch_w = width / ppi
    inch_h = height / ppi
    return {
        "ppi_reference": ppi,
        "width_in": round(inch_w, 2),
        "height_in": round(inch_h, 2),
        "width_mm": round(inch_w * 25.4, 1),
        "height_mm": round(inch_h * 25.4, 1),
    }


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: fetch_photo_assets.py <batch-manifest.json>")

    batch_path = (ROOT / sys.argv[1]).resolve()
    if ROOT not in batch_path.parents:
        raise SystemExit("batch manifest must be inside repository")

    batch = load_json(batch_path)
    registry = load_json(REGISTRY)
    photos = {p["asset_id"]: p for p in registry["photos"]}

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    for item in batch["assets"]:
        asset_id = item["asset_id"]
        if asset_id not in photos:
            raise RuntimeError(f"asset_id absent from registry: {asset_id}")

        photo = photos[asset_id]
        selected = photo.get("selected_source")
        if not selected:
            raise RuntimeError(f"{asset_id} has no selected source in registry")
        if selected != item["source_page_url"]:
            raise RuntimeError(f"{asset_id} source page does not match registry selection")

        direct_url = item["direct_image_url"]
        candidate = next(
            (
                c
                for c in photo.get("candidates", [])
                if c.get("source_page_url") == selected
                and c.get("direct_image_url") == direct_url
            ),
            None,
        )
        if candidate is None:
            raise RuntimeError(f"{asset_id} direct URL is not the selected registered candidate")

        rights = candidate.get("rights_status", "")
        if not (
            rights.startswith("VERIFIED_PUBLIC_DOMAIN")
            or rights.startswith("VERIFIED_CC0")
            or rights.startswith("VERIFIED_CC_BY")
        ):
            raise RuntimeError(f"{asset_id} rights not cleared for fetch: {rights}")

        data = fetch_bytes(direct_url)
        fmt, width, height, mode = inspect_image(data)
        sha256 = hashlib.sha256(data).hexdigest()
        suffix = extension_for(fmt)
        filename = f"{asset_id.lower().replace('.', '-')}-{item['slug']}{suffix}"
        out_path = OUTPUT_DIR / filename
        out_path.write_bytes(data)

        min_w = int(item.get("minimum_width_px", 0))
        min_h = int(item.get("minimum_height_px", 0))
        resolution_pass = width >= min_w and height >= min_h
        placement_status = "SOURCE_FILE_READY" if resolution_pass else "HOLD_RESOLUTION"

        record = {
            "asset_id": asset_id,
            "photo_id": photo["photo_id"],
            "title": photo["title"],
            "source_page_url": selected,
            "direct_image_url": direct_url,
            "repository_path": out_path.relative_to(ROOT).as_posix(),
            "sha256": sha256,
            "bytes": len(data),
            "format": fmt,
            "mode": mode,
            "width_px": width,
            "height_px": height,
            "effective_size_at_300ppi": effective_size(width, height),
            "minimum_width_px": min_w,
            "minimum_height_px": min_h,
            "resolution_gate_pass": resolution_pass,
            "placement_status": placement_status,
            "rights_status": rights,
            "creator": candidate.get("creator"),
            "credit": candidate.get("required_or_requested_credit"),
            "license_url": candidate.get("license_url"),
            "rights_basis": candidate.get("rights_basis"),
            "source_image_id": candidate.get("source_image_id"),
        }
        results.append(record)

        candidate["repository_source_path"] = record["repository_path"]
        candidate["source_sha256"] = sha256
        candidate["downloaded_width_px"] = width
        candidate["downloaded_height_px"] = height
        candidate["downloaded_bytes"] = len(data)
        candidate["resolution_gate_pass"] = resolution_pass
        candidate["placement_status"] = placement_status
        photo["download_status"] = "SOURCE_FILE_READY" if resolution_pass else "SOURCE_FILE_DOWNLOADED_HOLD"
        photo["repository_source_path"] = record["repository_path"]

    output = {
        "schema_version": "1.0",
        "batch_id": batch["batch_id"],
        "policy": {
            "files_are_unmodified_source_candidates": True,
            "automatic_final_layout_approval": False,
            "sha256_required": True,
            "rights_and_technical_review_remain_required": True,
        },
        "asset_count": len(results),
        "resolution_pass_count": sum(1 for r in results if r["resolution_gate_pass"]),
        "resolution_hold_count": sum(1 for r in results if not r["resolution_gate_pass"]),
        "assets": results,
    }
    save_json(OUTPUT_MANIFEST, output)
    save_json(REGISTRY, registry)

    print(json.dumps({
        "batch_id": output["batch_id"],
        "asset_count": output["asset_count"],
        "resolution_pass_count": output["resolution_pass_count"],
        "resolution_hold_count": output["resolution_hold_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
