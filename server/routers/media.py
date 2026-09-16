"""
media.py - Verified Media Dissemination Hub Router for Journalists, Media, and Citizens
"""

import os
import re
from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import BaseModel
from typing import Optional, List
from server.data_store import data_store
from server.press_kit_generator import generate_press_kit_zip

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "static")

router = APIRouter(prefix="/api/media", tags=["Media Dissemination"])


class NewMediaRequest(BaseModel):
    title: str
    type: str  # photo, video, audio, article
    category: str
    expedition: str
    station: str
    location: str
    coordinates: str
    url: Optional[str] = "/assets/images/bharati.jpg"
    resolution: Optional[str] = "4K UHD"
    credit: str
    license: Optional[str] = "Government Open Access / CC-BY 4.0"
    tags: Optional[List[str]] = ["PolarScience"]
    description: str
    press_kit_eligible: Optional[bool] = False


@router.get("/assets")
def get_media_assets(
    media_type: Optional[str] = Query(None, description="Filter by photo, video, audio, article"),
    station: Optional[str] = Query(None, description="Filter by station"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    q: Optional[str] = Query(None, description="Search query across title, tags, description")
):
    """Returns curated polar media assets with verified provenance and licensing."""
    assets = data_store.get_media_assets(
        media_type=media_type or "",
        station=station or "",
        tag=tag or "",
        search=q or ""
    )
    return {
        "count": len(assets),
        "filters": {"type": media_type, "station": station, "tag": tag, "query": q},
        "assets": assets
    }


@router.post("/assets")
def create_media_asset(req: NewMediaRequest):
    """Adds a new verified media asset to the dissemination repository."""
    new_asset = data_store.add_media_asset({
        "title": req.title,
        "type": req.type,
        "category": req.category,
        "expedition": req.expedition,
        "station": req.station,
        "location": req.location,
        "coordinates": req.coordinates,
        "url": req.url or "/assets/images/bharati.jpg",
        "thumbnail": req.url or "/assets/images/bharati.jpg",
        "resolution": req.resolution or "4K UHD",
        "credit": req.credit,
        "license": req.license or "Government Open Access / CC-BY 4.0",
        "tags": req.tags or ["PolarScience"],
        "description": req.description,
        "press_kit_eligible": req.press_kit_eligible or False
    })
    return {"status": "Success", "asset": new_asset}


@router.delete("/assets/{asset_id}")
def delete_media_asset(asset_id: str):
    deleted = data_store.delete_media_asset(asset_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Media asset not found")
    return {"status": "Success", "message": f"Asset {asset_id} removed"}


@router.get("/press-kits")
def get_press_kits():
    """Returns curated high-priority press release kits for journalists."""
    return data_store.get_press_kits()


@router.get("/press-kits/{pk_id}/download")
@router.get("/press-kits/download/{pk_id}")
def download_press_kit(pk_id: str):
    """
    Builds and streams an authentic press kit ZIP package containing:
    1. Authentic image assets included in this press release dossier.
    2. Sidecar metadata TXT files for each asset.
    3. Official PRESS_RELEASE_DOSSIER.txt with ministerial statements.
    4. Machine-readable MEDIA_MANIFEST.json with credits & coordinates.
    5. ATTRIBUTION_AND_LICENSING.txt with CC-BY 4.0 government open-access terms.
    6. EXPEDITION_STATION_FACTSHEET.txt with polar station specs.
    """
    pk = data_store.get_press_kit_by_id(pk_id)
    if not pk:
        raise HTTPException(status_code=404, detail="Press kit not found")

    zip_bytes = generate_press_kit_zip(pk, data_store.media, STATIC_DIR)
    safe_id = re.sub(r'[^a-zA-Z0-9_\-]', '_', pk_id)
    filename = f"{safe_id}_press_kit.zip"

    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-cache, no-store, must-revalidate"
        }
    )


@router.get("/download/{asset_id}")
def download_asset_package(asset_id: str):
    """Simulates packaged download with metadata certificate and license manifest."""
    asset = None
    for a in data_store.media:
        if a["id"].lower() == asset_id.lower():
            asset = a
            break
    if not asset:
        raise HTTPException(status_code=404, detail="Media asset not found")

    return {
        "download_status": "Ready",
        "asset_id": asset["id"],
        "title": asset["title"],
        "file_url": asset["url"],
        "resolution": asset.get("resolution", "High-Res"),
        "license_manifest": {
            "license": asset["license"],
            "credit_line_required": asset["credit"],
            "usage_terms": "Govt of India Open Data / Attribution Required for Broadcast and Print",
            "sha256_checksum": "a8f341b52c0989f6d7a421eef001c43b9281745402a7b"
        }
    }
