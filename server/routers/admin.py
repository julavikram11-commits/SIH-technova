"""
admin.py - Unified Admin CMS & Ingestion Pipeline Router for MoES / NCPOR staff
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from server.data_store import data_store

router = APIRouter(prefix="/api/admin", tags=["Admin CMS & Publishing"])


class SubmissionRequest(BaseModel):
    title: str
    submitter: str
    expedition: str
    station: str
    type: Optional[str] = "Research Paper"
    abstract_content: str
    tags: Optional[List[str]] = []
    plain_summary: Optional[str] = ""


@router.get("/overview")
def get_dashboard_overview():
    """Provides overall statistics and KPIs for the NCPOR institutional dashboard."""
    return data_store.get_analytics_summary()


@router.get("/queue")
def get_submission_queue():
    """Returns the current scientific moderation and publishing review queue."""
    return data_store.get_admin_queue()


@router.post("/submit")
def submit_expedition_content(req: SubmissionRequest):
    """Submits a new expedition research paper, dataset, or media log into the governance queue."""
    new_sub = data_store.add_submission({
        "title": req.title,
        "submitter": req.submitter,
        "expedition": req.expedition,
        "station": req.station,
        "type": req.type,
        "tags": req.tags or ["Polar Science"],
        "plain_summary": req.plain_summary or f"Plain language breakdown for {req.title}"
    })
    return {
        "status": "Submitted to Governance Queue",
        "submission": new_sub,
        "next_step": "Awaiting MoES Scientific Editorial & GIGW Compliance Review"
    }


@router.post("/approve/{sub_id}")
def approve_and_publish_item(sub_id: str):
    """Approves a queued item and instantly disseminates it across all 3 pillars."""
    approved_item = data_store.approve_and_publish(sub_id)
    if not approved_item:
        raise HTTPException(status_code=404, detail="Submission item not found")

    return {
        "status": "Success - Published across Outreach, Repository, and Media Hub",
        "published_item": approved_item,
        "message": f"Item '{approved_item['title']}' is now live on the public portal!"
    }
