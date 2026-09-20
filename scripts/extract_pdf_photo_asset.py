#!/usr/bin/env python3
"""Extract a rights-cleared photograph embedded in a registered PDF source.

The batch manifest identifies a registry-selected source document, 1-based PDF
page number and image rank. The script downloads only allowlisted HTTPS PDF
sources, extracts an embedded raster without resampling, validates the image,
records SHA-256/pixel dimensions and links it back to the photograph registry.

Extracted files are SOURCE CANDIDATES, not automatic final-layout approvals.
"""

from __future__ import annotations

import hashlib
import json
import sys
from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler

import fitz  # PyMuPDF
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "assets" / "photo-source-registry.json"
OUTPUT_DIR = ROOT / "assets" / "photos" / "a-core" / "source-candidates"

ALLOWED_HOSTS = {"eprints.ncl.ac.uk", "mdpi-res.com", "www.mdpi.com", "orbi.uliege.be"}
MAX_PDF_BYTES = 100 * 1024 * 1024


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


def fetch_pdf(url: str) -> bytes:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise RuntimeError(f"only HTTPS is allowed: {url}")
    host = (parsed.hostname or "").lower()
    if host not in ALLOWED_HOSTS:
        raise RuntimeError(f"host not allowlisted: {host}")
    req = Request(url, headers={
        "User-Agent": "Practical-Beekeeping-Handbook/1.0 scientific-photo-extractor",
        "Accept": "application/pdf,*/*;q=0.8",
    })
    opener = build_opener(SafeRedirect())
    try:
        with opener.open(req, timeout=90) as response:
            final_host = (urlparse(response.geturl()).hostname or "").lower()
            if final_host not in ALLOWED_HOSTS:
                raise RuntimeError(f"final host not allowlisted: {final_host}")
            data = response.read(MAX_PDF_BYTES + 1)
    except (HTTPError, URLError) as exc:
        raise RuntimeError(f"failed to fetch PDF: {exc}") from exc
    if len(data) > MAX_PDF_BYTES:
        raise RuntimeError("PDF payload exceeded maximum allowed size")
    if not data.startswith(b"%PDF"):
        raise RuntimeError("downloaded payload is not a PDF")
    return data


def inspect_image(data: bytes):
    bio = BytesIO(data)
    with Image.open(bio) as im:
        im.verify()
    bio.seek(0)
    with Image.open(bio) as im:
        return (im.format or "").upper(), im.width, im.height, im.mode


def extension_for(fmt: str) -> str:
    if fmt == "JPEG":
        return ".jpg"
    if fmt == "PNG":
        return ".png"
    raise RuntimeError(f"unsupported raster format: {fmt}")


def effective_size(width: int, height: int, ppi: int = 300):
    return {
        "ppi_reference": ppi,
        "width_in": round(width / ppi, 2),
        "height_in": round(height / ppi, 2),
        "width_mm": round(width / ppi * 25.4, 1),
        "height_mm": round(height / ppi * 25.4, 1),
    }


def extract_ranked_image(pdf_bytes: bytes, page_number: int, image_rank: int):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    if page_number < 1 or page_number > doc.page_count:
        raise RuntimeError(f"page {page_number} outside PDF page count {doc.page_count}")
    page = doc[page_number - 1]
    infos = [i for i in page.get_image_info(xrefs=True) if i.get("xref", 0) > 0 and i.get("width", 0) >= 200 and i.get("height", 0) >= 150]
    if not infos:
        raise RuntimeError(f"no qualifying embedded raster found on page {page_number}")
    infos.sort(key=lambda i: (float(i["bbox"][1]), float(i["bbox"][0])))
    if image_rank < 0 or image_rank >= len(infos):
        raise RuntimeError(f"image_rank {image_rank} outside qualifying image count {len(infos)}")
    info = infos[image_rank]
    extracted = doc.extract_image(info["xref"])
    return extracted["image"], {
        "xref": info["xref"],
        "bbox": list(info["bbox"]),
        "embedded_width_px": info["width"],
        "embedded_height_px": info["height"],
        "qualifying_image_count": len(infos),
    }


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: extract_pdf_photo_asset.py <batch-manifest.json>")
    batch_path=(ROOT / sys.argv[1]).resolve()
    if ROOT not in batch_path.parents:
        raise SystemExit("batch manifest must be inside repository")
    batch=load_json(batch_path)
    output_manifest=(ROOT / batch["output_manifest"]).resolve()
    registry=load_json(REGISTRY)
    photos={p["asset_id"]:p for p in registry["photos"]}
    OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
    results=[]

    for item in batch["assets"]:
        asset_id=item["asset_id"]
        photo=photos.get(asset_id)
        if not photo:
            raise RuntimeError(f"asset_id absent from registry: {asset_id}")
        selected=photo.get("selected_source")
        if selected != item["source_page_url"]:
            raise RuntimeError(f"{asset_id} selected source does not match batch source page")
        candidate=next((c for c in photo.get("candidates",[]) if c.get("source_page_url")==selected and c.get("source_document_url")==item["source_document_url"]),None)
        if candidate is None:
            raise RuntimeError(f"{asset_id} selected PDF candidate not found in registry")
        rights=candidate.get("rights_status","")
        if not (rights.startswith("VERIFIED_PUBLIC_DOMAIN") or rights.startswith("VERIFIED_CC0") or rights.startswith("VERIFIED_CC_BY")):
            raise RuntimeError(f"{asset_id} rights not cleared: {rights}")

        pdf=fetch_pdf(item["source_document_url"])
        image_bytes, extraction=extract_ranked_image(pdf,int(item["page_number"]),int(item.get("image_rank",0)))
        fmt,width,height,mode=inspect_image(image_bytes)
        suffix=extension_for(fmt)
        out_path=OUTPUT_DIR / f"{asset_id.lower().replace('.','-')}-{item['slug']}{suffix}"
        out_path.write_bytes(image_bytes)
        sha256=hashlib.sha256(image_bytes).hexdigest()
        min_w=int(item.get("minimum_width_px",0)); min_h=int(item.get("minimum_height_px",0))
        resolution_pass=width>=min_w and height>=min_h
        placement_status="SOURCE_FILE_READY" if resolution_pass else "HOLD_RESOLUTION"

        record={
            "asset_id":asset_id,"photo_id":photo["photo_id"],"title":photo["title"],
            "source_page_url":selected,"source_document_url":item["source_document_url"],
            "source_figure":candidate.get("source_figure"),"page_number":int(item["page_number"]),
            "repository_path":out_path.relative_to(ROOT).as_posix(),
            "sha256":sha256,"bytes":len(image_bytes),"format":fmt,"mode":mode,
            "width_px":width,"height_px":height,"effective_size_at_300ppi":effective_size(width,height),
            "minimum_width_px":min_w,"minimum_height_px":min_h,
            "resolution_gate_pass":resolution_pass,"placement_status":placement_status,
            "rights_status":rights,"creator":candidate.get("creator"),
            "credit":candidate.get("required_or_requested_credit"),
            "license_url":candidate.get("license_url"),"rights_basis":candidate.get("rights_basis"),
            "extraction":extraction,
        }
        results.append(record)
        candidate["repository_source_path"]=record["repository_path"]
        candidate["source_sha256"]=sha256
        candidate["downloaded_width_px"]=width
        candidate["downloaded_height_px"]=height
        candidate["downloaded_bytes"]=len(image_bytes)
        candidate["resolution_gate_pass"]=resolution_pass
        candidate["placement_status"]=placement_status
        candidate["extraction_record"]=extraction
        photo["download_status"]="SOURCE_FILE_READY" if resolution_pass else "SOURCE_FILE_DOWNLOADED_HOLD"
        photo["repository_source_path"]=record["repository_path"]

    output={
        "schema_version":"1.0","batch_id":batch["batch_id"],
        "policy":{"embedded_raster_extracted_without_resampling":True,"automatic_final_layout_approval":False,"sha256_required":True,"rights_and_technical_review_remain_required":True},
        "asset_count":len(results),
        "resolution_pass_count":sum(1 for r in results if r["resolution_gate_pass"]),
        "resolution_hold_count":sum(1 for r in results if not r["resolution_gate_pass"]),
        "assets":results,
    }
    save_json(output_manifest,output)
    save_json(REGISTRY,registry)
    print(json.dumps({"batch_id":output["batch_id"],"asset_count":output["asset_count"],"resolution_pass_count":output["resolution_pass_count"],"resolution_hold_count":output["resolution_hold_count"]},indent=2))


if __name__=="__main__":
    main()
