from fastapi import APIRouter, Response
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class DownloadPayload(BaseModel):
    title: str | None = None
    key_points: list[str]
    child_explanation: str | None = None
    transcript_excerpt: str | None = None

@router.post("/download")
async def download_notes(payload: DownloadPayload):
    lines = []
    if payload.title:
        lines.append(f"Title: {payload.title}")
    lines.append("\nKey Points:")
    for kp in payload.key_points:
        lines.append(f"- {kp}")
    if payload.child_explanation:
        lines.append("\nExplain Like I'm 7:\n" + payload.child_explanation)
    if payload.transcript_excerpt:
        lines.append("\nTranscript Excerpt:\n" + payload.transcript_excerpt)
    content = "\n".join(lines)
    filename = f"notes_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"
    return Response(content=content, media_type="text/plain", headers={"Content-Disposition": f"attachment; filename={filename}"})
