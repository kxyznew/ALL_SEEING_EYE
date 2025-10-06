from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from pathlib import Path
from datetime import datetime
from app.services.transcript import fetch_transcript
from app.services.youtube import validate_youtube_url
from app.services.summarize import generate_key_points, explain_like_child

router = APIRouter()

class AnalyzeRequest(BaseModel):
    url: HttpUrl
    simplify_for_child: bool = True
    language: Optional[str] = "en"

@router.post("/analyze")
async def analyze_video(req: AnalyzeRequest):
    url_str = str(req.url)
    if not validate_youtube_url(url_str):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    try:
        title, lines = await fetch_transcript(url_str, languages=[req.language] if req.language else None)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch transcript")

    key_points: List[str] = generate_key_points(lines)
    excerpt_text = " ".join(lines[:30]).strip()
    if len(excerpt_text) > 1200:
        excerpt_text = excerpt_text[:1200] + "..."
    child_text = explain_like_child(key_points) if req.simplify_for_child else ""

    notes_parts: List[str] = []
    if title:
        notes_parts.append(f"Title: {title}")
    notes_parts.append("\nKey Points:")
    for kp in key_points:
        notes_parts.append(f"- {kp}")
    if child_text:
        notes_parts.append("\nExplain Like I'm 7:\n" + child_text)
    if excerpt_text:
        notes_parts.append("\nTranscript Excerpt:\n" + excerpt_text)
    content = "\n".join(notes_parts)

    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(ch for ch in (title or "notes") if ch.isalnum() or ch in (" ", "_", "-")).strip().replace(" ", "_")
    file_path = data_dir / f"{safe_title or 'notes'}_{timestamp}.txt"
    try:
        file_path.write_text(content, encoding="utf-8")
        saved_path = str(file_path)
    except Exception:
        saved_path = None

    return {
        "title": title,
        "key_points": key_points,
        "child_explanation": child_text,
        "transcript_excerpt": excerpt_text,
        "saved_path": saved_path,
    }
