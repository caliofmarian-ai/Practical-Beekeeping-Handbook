#!/usr/bin/env python3
"""Extract a reproducible still frame from a rights-cleared video source."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler

import cv2

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "assets" / "photo-source-registry.json"
OUTPUT_DIR = ROOT / "assets" / "photos" / "a-core" / "source-candidates"
ALLOWED_HOSTS = {"journals.plos.org", "storage.googleapis.com"}
MAX_BYTES = 150 * 1024 * 1024

class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        host = (urlparse(newurl).hostname or "").lower()
        if host not in ALLOWED_HOSTS:
            raise RuntimeError(f"redirect blocked to non-allowlisted host: {host}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def save_json(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def fetch_video(url):
    parsed=urlparse(url)
    if parsed.scheme!="https" or (parsed.hostname or "").lower() not in ALLOWED_HOSTS:
        raise RuntimeError(f"video host not allowlisted: {url}")
    req=Request(url,headers={"User-Agent":"Practical-Beekeeping-Handbook/1.0 video-frame-extractor"})
    with build_opener(SafeRedirect()).open(req,timeout=120) as response:
        data=response.read(MAX_BYTES+1)
    if len(data)>MAX_BYTES:
        raise RuntimeError("video payload too large")
    return data

def main():
    if len(sys.argv)!=2:
        raise SystemExit("usage: extract_video_frame_asset.py <batch-manifest.json>")
    batch_path=(ROOT / sys.argv[1]).resolve()
    batch=load_json(batch_path)
    registry=load_json(REGISTRY)
    photos={p["asset_id"]:p for p in registry["photos"]}
    OUTPUT_DIR.mkdir(parents=True,exist_ok=True)
    results=[]
    for item in batch["assets"]:
        photo=photos[item["asset_id"]]
        if photo.get("selected_source") != item["source_page_url"]:
            raise RuntimeError("selected source mismatch")
        candidate=next((c for c in photo.get("candidates",[]) if c.get("source_page_url")==item["source_page_url"] and c.get("direct_video_url")==item["direct_video_url"]),None)
        if candidate is None:
            raise RuntimeError("registered video candidate not found")
        rights=candidate.get("rights_status","")
        if not (rights.startswith("VERIFIED_CC_BY") or rights.startswith("VERIFIED_PUBLIC_DOMAIN") or rights.startswith("VERIFIED_CC0")):
            raise RuntimeError("video rights not cleared")
        video=fetch_video(item["direct_video_url"])
        with tempfile.NamedTemporaryFile(suffix=".mp4") as tmp:
            tmp.write(video); tmp.flush()
            cap=cv2.VideoCapture(tmp.name)
            fps=cap.get(cv2.CAP_PROP_FPS)
            frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if not fps or fps <= 0 or frames <= 0:
                raise RuntimeError("could not inspect video")
            duration=frames/fps
            fraction=float(item.get("timestamp_fraction",0.4))
            timestamp=max(0.0,min(duration-0.05,duration*fraction))
            cap.set(cv2.CAP_PROP_POS_MSEC,timestamp*1000)
            ok,frame=cap.read()
            cap.release()
            if not ok:
                raise RuntimeError("frame extraction failed")
        height,width=frame.shape[:2]
        out_path=OUTPUT_DIR / f"{item['asset_id'].lower().replace('.','-')}-{item['slug']}.jpg"
        ok,encoded=cv2.imencode(".jpg",frame,[int(cv2.IMWRITE_JPEG_QUALITY),95])
        if not ok:
            raise RuntimeError("JPEG encoding failed")
        data=encoded.tobytes()
        out_path.write_bytes(data)
        sha=hashlib.sha256(data).hexdigest()
        min_w=int(item.get("minimum_width_px",0)); min_h=int(item.get("minimum_height_px",0))
        passed=width>=min_w and height>=min_h
        record={
          "asset_id":item["asset_id"],"photo_id":photo["photo_id"],"title":photo["title"],
          "source_page_url":item["source_page_url"],"direct_video_url":item["direct_video_url"],
          "repository_path":out_path.relative_to(ROOT).as_posix(),"sha256":sha,"bytes":len(data),
          "width_px":width,"height_px":height,"video_duration_seconds":round(duration,3),
          "frame_timestamp_seconds":round(timestamp,3),"frame_fraction":fraction,
          "minimum_width_px":min_w,"minimum_height_px":min_h,
          "resolution_gate_pass":passed,"placement_status":"SOURCE_FILE_READY" if passed else "HOLD_RESOLUTION",
          "rights_status":rights,"creator":candidate.get("creator"),"credit":candidate.get("required_or_requested_credit"),
          "license_url":candidate.get("license_url"),"rights_basis":candidate.get("rights_basis")
        }
        results.append(record)
        candidate.update({
          "repository_source_path":record["repository_path"],"source_sha256":sha,
          "downloaded_width_px":width,"downloaded_height_px":height,"downloaded_bytes":len(data),
          "resolution_gate_pass":passed,"placement_status":record["placement_status"],
          "frame_timestamp_seconds":record["frame_timestamp_seconds"],"video_duration_seconds":record["video_duration_seconds"]
        })
        photo["download_status"]="SOURCE_FILE_READY" if passed else "SOURCE_FILE_DOWNLOADED_HOLD"
        photo["repository_source_path"]=record["repository_path"]
    output={"schema_version":"1.0","batch_id":batch["batch_id"],"policy":{"real_video_frame_only":True,"automatic_final_layout_approval":False,"sha256_required":True},"asset_count":len(results),"resolution_pass_count":sum(1 for r in results if r["resolution_gate_pass"]),"resolution_hold_count":sum(1 for r in results if not r["resolution_gate_pass"]),"assets":results}
    save_json(ROOT / batch["output_manifest"],output)
    save_json(REGISTRY,registry)
    print(json.dumps(output,indent=2))

if __name__=="__main__":
    main()
