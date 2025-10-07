from typing import List, Optional, Tuple
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import re
import httpx

_YT_ID_REGEX = re.compile(r"(?:v=|youtu\.be/|embed/)([\w-]{11})")

async def fetch_title(session: httpx.AsyncClient, video_id: str) -> Optional[str]:
    try:
        # Use oEmbed as a lightweight title fetch
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        r = await session.get(url, timeout=10)
        if r.status_code == 200:
            return r.json().get("title")
    except Exception:
        pass
    return None

def extract_video_id(url: str) -> Optional[str]:
    m = _YT_ID_REGEX.search(url)
    return m.group(1) if m else None

async def fetch_transcript(url: str, languages: Optional[List[str]] = None) -> Tuple[str, List[str]]:
    vid = extract_video_id(url)
    if not vid:
        raise ValueError("Could not extract YouTube video id")
    # Transcript
    try:
        transcript = YouTubeTranscriptApi.get_transcript(vid, languages=languages or ['en'])
        lines = [chunk['text'] for chunk in transcript if chunk.get('text') and chunk['text'] != '[Music]']
    except (NoTranscriptFound, TranscriptsDisabled):
        lines = []
    # Title via async client
    async with httpx.AsyncClient() as client:
        title = await fetch_title(client, vid)
    return title or f"YouTube Video {vid}", lines
