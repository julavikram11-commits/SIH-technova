"""
outreach.py - Outreach, Stations Explorer, Live Telemetry, Articles, Toolkits, Events, and Student Quiz Router
"""

import random
import re
from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from server.data_store import data_store
from server.pdf_generator import generate_toolkit_pdf

router = APIRouter(prefix="/api/outreach", tags=["Outreach & Education"])


@router.get("/stations")
def get_all_stations():
    """Returns all Indian polar stations with latest coordinates and telemetry."""
    return data_store.get_stations()


@router.get("/stations/{station_id}")
def get_station_detail(station_id: str):
    station = data_store.get_station_by_id(station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    return station


@router.get("/telemetry/live")
def get_live_telemetry():
    """Generates dynamic live telemetry with slight realistic fluctuations."""
    stations = data_store.get_stations()
    live_feed = []
    for s in stations:
        base_temp = s["telemetry"]["temp_c"]
        fluctuated_temp = round(base_temp + random.uniform(-0.4, 0.4), 1)
        base_wind = s["telemetry"]["wind_speed_knots"]
        fluctuated_wind = max(5, int(base_wind + random.randint(-2, 3)))
        live_feed.append({
            "station_id": s["id"],
            "name": s["name"],
            "region": s["region"],
            "temp_c": fluctuated_temp,
            "wind_knots": fluctuated_wind,
            "wind_direction": s["telemetry"]["wind_direction"],
            "pressure_hpa": s["telemetry"]["pressure_hpa"],
            "daylight_hours": s["telemetry"]["daylight_hours"],
            "solar_radiation": s["telemetry"]["solar_radiation"],
            "geomagnetic_index": s["telemetry"]["geomagnetic_index"]
        })
    return {"timestamp": "Live Real-Time Feed", "data": live_feed}


# Science Outreach Articles
@router.get("/articles")
def get_outreach_articles(
    audience: Optional[str] = Query(None, description="Filter by audience (School Students, General Public, Educators & College, Policy Makers)"),
    topic: Optional[str] = Query(None, description="Filter by topic")
):
    """Returns curated science outreach explainers and articles."""
    articles = data_store.get_outreach_articles(audience=audience or "", topic=topic or "")
    return {"count": len(articles), "articles": articles}


class NewArticleRequest(BaseModel):
    title: str
    audience: str
    topic: str
    read_time: Optional[str] = "5 min"
    summary: str
    content: str
    key_takeaways: Optional[List[str]] = []


@router.post("/articles")
def create_outreach_article(req: NewArticleRequest):
    """Publishes a new science communication article for outreach."""
    new_art = data_store.add_outreach_article({
        "title": req.title,
        "audience": req.audience,
        "topic": req.topic,
        "read_time": req.read_time,
        "summary": req.summary,
        "content": req.content,
        "key_takeaways": req.key_takeaways or ["Essential polar insight"]
    })
    return {"status": "Success", "article": new_art}


@router.delete("/articles/{article_id}")
def delete_outreach_article(article_id: str):
    deleted = data_store.delete_outreach_article(article_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"status": "Success", "message": f"Article {article_id} removed"}


# Educational Content & Toolkits
@router.get("/toolkits")
def get_educational_toolkits():
    """Returns downloadable educational toolkits, posters, and lab manuals."""
    return data_store.get_educational_toolkits()


@router.get("/toolkits/download/{toolkit_id}")
def download_educational_toolkit(toolkit_id: str):
    """
    Downloads an official verified PDF educational package generated from
    outreach toolkit metadata, objectives, and curriculum mapping.
    """
    kit = data_store.get_toolkit_by_id(toolkit_id)
    if not kit:
        raise HTTPException(status_code=404, detail="Educational toolkit not found")

    pdf_bytes = generate_toolkit_pdf(kit)
    safe_id = re.sub(r'[^a-zA-Z0-9_\-]', '_', toolkit_id)
    filename = f"{safe_id}_educational_toolkit.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-cache, no-store, must-revalidate"
        }
    )



# Events & Announcements
@router.get("/events")
def get_events():
    """Returns polar science events, symposiums, and calls for proposals."""
    return data_store.get_events()


class NewEventRequest(BaseModel):
    title: str
    date: str
    status: Optional[str] = "Upcoming"
    category: str
    organizer: Optional[str] = "NCPOR / MoES"
    summary: str


@router.post("/events")
def create_event(req: NewEventRequest):
    new_evt = data_store.add_event({
        "title": req.title,
        "date": req.date,
        "status": req.status,
        "category": req.category,
        "organizer": req.organizer,
        "summary": req.summary
    })
    return {"status": "Success", "event": new_evt}


@router.delete("/events/{event_id}")
def delete_event(event_id: str):
    deleted = data_store.delete_event(event_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"status": "Success", "message": f"Event {event_id} removed"}


# Student Interactive Quiz
@router.get("/quiz")
def get_quiz_questions():
    return data_store.quiz


class QuizSubmitRequest(BaseModel):
    student_name: str
    school_institution: Optional[str] = "Student Explorer"
    answers: Dict[int, int]


@router.post("/quiz/submit")
def submit_quiz(submission: QuizSubmitRequest):
    questions = {q["id"]: q for q in data_store.quiz}
    score = 0
    detailed_results = []

    for q_id, q in questions.items():
        user_ans = submission.answers.get(q_id, -1)
        is_correct = user_ans == q["correct_index"]
        if is_correct:
            score += 1
        detailed_results.append({
            "question_id": q_id,
            "question": q["question"],
            "user_answer": q["options"][user_ans] if 0 <= user_ans < len(q["options"]) else "Skipped",
            "correct_answer": q["options"][q["correct_index"]],
            "is_correct": is_correct,
            "explanation": q["explanation"]
        })

    total = len(questions)
    percentage = int((score / total) * 100)
    badge = "Polar Junior Explorer"
    if percentage == 100:
        badge = "Master Polar Scientist Cadet"
    elif percentage >= 60:
        badge = "Senior Polar Science Scout"

    certificate = {
        "certificate_id": f"NCPOR-CERT-2024-{random.randint(10000, 99999)}",
        "student_name": submission.student_name,
        "institution": submission.school_institution,
        "score": f"{score}/{total}",
        "percentage": percentage,
        "badge": badge,
        "issued_by": "National Centre for Polar and Ocean Research (NCPOR), Ministry of Earth Sciences, Govt. of India",
        "date": "2024-06-01"
    }

    return {
        "score": score,
        "total": total,
        "percentage": percentage,
        "badge": badge,
        "certificate": certificate,
        "results": detailed_results
    }
