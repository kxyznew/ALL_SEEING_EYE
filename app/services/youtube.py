from typing import List, Optional, Dict
import re

YOUTUBE_REGEX = re.compile(r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$")

# Minimal, no external API key requirement: try youtubetranscriptapi, else fallback to basic extract from watchpage captions when available

def validate_youtube_url(url: str) -> bool:
    return bool(YOUTUBE_REGEX.match(url))
