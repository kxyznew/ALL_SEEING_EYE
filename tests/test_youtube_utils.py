import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.youtube_utils import extract_video_id


def test_extract_video_id_watch():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert extract_video_id(url) == "dQw4w9WgXcQ"


def test_extract_video_id_youtu_be():
    url = "https://youtu.be/dQw4w9WgXcQ"
    assert extract_video_id(url) == "dQw4w9WgXcQ"


def test_extract_video_id_shorts():
    url = "https://www.youtube.com/shorts/abcDEF123_-"
    assert extract_video_id(url) == "abcDEF123_-"


def test_extract_video_id_embed():
    url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
    assert extract_video_id(url) == "dQw4w9WgXcQ"


def test_invalid_host():
    url = "https://example.com/watch?v=dQw4w9WgXcQ"
    assert extract_video_id(url) is None


def test_garbage():
    url = "not a url"
    assert extract_video_id(url) is None
