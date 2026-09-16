"""
repository.py - Structured Polar Knowledge Repository Router for Publications & Datasets
"""

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import BaseModel
from typing import Optional, List
import re
from server.data_store import data_store
from server.rag_engine import rag_engine
from server.pdf_generator import generate_publication_pdf
from server.dataset_generator import generate_dataset_csv

router = APIRouter(prefix="/api/repository", tags=["Knowledge Repository"])


class NewPublicationRequest(BaseModel):
    title: str
    authors: str
    affiliation: Optional[str] = "NCPOR, Ministry of Earth Sciences"
    year: Optional[int] = 2024
    expedition: str
    station: str
    vertical: str
    topic: Optional[str] = "General Polar Science"
    abstract: str
    keywords: Optional[List[str]] = ["Polar Science", "NCPOR"]
    plain_summary: Optional[str] = ""


@router.get("/publications")
def search_publications(
    q: Optional[str] = Query(None, description="Search query"),
    station: Optional[str] = Query(None, description="Filter by station"),
    vertical: Optional[str] = Query(None, description="Filter by scientific vertical"),
    year: Optional[int] = Query(None, description="Filter by publication year"),
    sort_by: Optional[str] = Query("newest", description="Sort by newest, oldest, citations, title")
):
    """Searches, filters, and sorts publications in the NCPOR polar knowledge repository."""
    results = data_store.search_publications(
        query=q or "",
        station=station or "",
        vertical=vertical or "",
        year=year,
        sort_by=sort_by or "newest"
    )
    return {
        "count": len(results),
        "query": q,
        "filters": {"station": station, "vertical": vertical, "year": year, "sort_by": sort_by},
        "publications": results
    }


@router.get("/publication/{pub_id}")
def get_publication(pub_id: str):
    pub = data_store.get_publication_by_id(pub_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publication not found")
    return pub


@router.post("/publications")
def add_publication_resource(req: NewPublicationRequest):
    """Allows authenticated researchers / admins to add a new scientific publication directly."""
    new_pub = data_store.add_publication({
        "title": req.title,
        "authors": req.authors,
        "affiliation": req.affiliation,
        "year": req.year,
        "expedition": req.expedition,
        "station": req.station,
        "vertical": req.vertical,
        "topic": req.topic,
        "abstract": req.abstract,
        "keywords": req.keywords,
        "plain_summary": req.plain_summary or f"Research breakdown on {req.title}"
    })
    return {"status": "Success", "message": "Resource added to repository", "publication": new_pub}


@router.delete("/publications/{pub_id}")
def delete_publication_resource(pub_id: str):
    """Removes a publication from the repository catalog."""
    deleted = data_store.delete_publication(pub_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Publication not found")
    return {"status": "Success", "message": f"Resource {pub_id} removed"}


@router.get("/datasets")
def get_all_datasets():
    """Returns all open scientific polar datasets with parameter metadata."""
    return data_store.get_datasets()


@router.get("/citation/{pub_id}")
def get_citation_formats(pub_id: str):
    """Generates BibTeX, APA, and RIS citations for researchers."""
    pub = data_store.get_publication_by_id(pub_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publication not found")

    apa = f"{pub['authors']} ({pub['year']}). {pub['title']}. Polar Research Repository / MoES, DOI: {pub['doi']}."
    ris = f"""TY  - JOUR
TI  - {pub['title']}
AU  - {pub['authors']}
PY  - {pub['year']}
DO  - {pub['doi']}
PB  - National Centre for Polar and Ocean Research
ER  -"""

    return {
        "pub_id": pub["id"],
        "bibtex": pub.get("bibtex", ""),
        "apa": apa,
        "ris": ris
    }


@router.get("/explain/{pub_id}")
def explain_publication(pub_id: str):
    """Triggers AI 'Explain This Paper' multi-tier plain-language summary."""
    explanation = rag_engine.explain_paper(pub_id)
    if "error" in explanation:
        raise HTTPException(status_code=404, detail=explanation["error"])
    return explanation


@router.get("/download/{dataset_id}")
def download_dataset_file(dataset_id: str):
    """
    Downloads an authentic demonstration CSV representation with verified metadata
    and parameters for the requested polar dataset.
    """
    dataset = data_store.get_dataset_by_id(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    csv_content = generate_dataset_csv(dataset)
    safe_id = re.sub(r'[^a-zA-Z0-9_\-]', '_', dataset_id)
    filename = f"{safe_id}_dataset.csv"

    return Response(
        content=csv_content.encode("utf-8"),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-cache, no-store, must-revalidate"
        }
    )


@router.get("/publication/{pub_id}/download")
def download_publication_document(pub_id: str):
    """
    Downloads an official verified PDF publication document generated from
    repository metadata, abstract, plain summary, and citation records.
    """
    pub = data_store.get_publication_by_id(pub_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publication not found")

    pdf_bytes = generate_publication_pdf(pub)
    safe_id = re.sub(r'[^a-zA-Z0-9_\-]', '_', pub_id)
    filename = f"{safe_id}_publication.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-cache, no-store, must-revalidate"
        }
    )

