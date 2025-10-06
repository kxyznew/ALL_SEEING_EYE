import re
from urllib.parse import urlparse, parse_qs


YOUTUBE_HOSTS = {"www.youtube.com", "youtube.com", "m.youtube.com", "youtu.be", "www.youtu.be"}


def extract_video_id(url: str) -> str | None:
    """
    Extract a YouTube video ID from common URL formats.

    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    """
    if not url or not isinstance(url, str):
        return None

    try:
        parsed = urlparse(url)
    except Exception:
        return None

    if parsed.netloc.lower() not in YOUTUBE_HOSTS:
        return None

    # youtu.be/<id>
    if parsed.netloc.lower().endswith("youtu.be"):
        path_parts = parsed.path.strip("/").split("/")
        if path_parts and re.fullmatch(r"[A-Za-z0-9_-]{6,}", path_parts[0]):
            return path_parts[0]
        return None

    # youtube.com/watch?v=<id>
    if parsed.path == "/watch":
        vid = parse_qs(parsed.query).get("v", [None])[0]
        if vid and re.fullmatch(r"[A-Za-z0-9_-]{6,}", vid):
            return vid
        return None

    # youtube.com/shorts/<id>
    if parsed.path.startswith("/shorts/"):
        vid = parsed.path.split("/")[2] if len(parsed.path.split("/")) > 2 else None
        if vid and re.fullmatch(r"[A-Za-z0-9_-]{6,}", vid):
            return vid
        return None

    # youtube.com/embed/<id>
    if parsed.path.startswith("/embed/"):
        vid = parsed.path.split("/")[2] if len(parsed.path.split("/")) > 2 else None
        if vid and re.fullmatch(r"[A-Za-z0-9_-]{6,}", vid):
            return vid
        return None

    # Fallback: look for v param anywhere
    vid = parse_qs(parsed.query).get("v", [None])[0]
    if vid and re.fullmatch(r"[A-Za-z0-9_-]{6,}", vid):
        return vid

    return None
