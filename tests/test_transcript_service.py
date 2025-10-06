import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.transcript_service import TranscriptService


@patch("app.transcript_service.YouTubeTranscriptApi")
def test_fetch_segments_success(mock_api):
    mock_transcripts = MagicMock()
    mock_transcript = MagicMock()
    mock_transcript.fetch.return_value = [{"text": "hello"}, {"text": "world"}]
    mock_transcripts.find_generated_transcript.side_effect = Exception("no generated")
    mock_transcripts.find_transcript.return_value = mock_transcript
    mock_api.list_transcripts.return_value = mock_transcripts

    svc = TranscriptService()
    segments = svc.fetch_segments("abc123")
    assert segments == [{"text": "hello"}, {"text": "world"}]


@patch("app.transcript_service.YouTubeTranscriptApi")
def test_fetch_transcript_text(mock_api):
    mock_transcripts = MagicMock()
    mock_transcript = MagicMock()
    mock_transcript.fetch.return_value = [
        {"text": "This is"},
        {"text": " a test"},
        {"text": ""},
        {"no_text": True},
    ]
    mock_transcripts.find_generated_transcript.side_effect = Exception("no generated")
    mock_transcripts.find_transcript.return_value = mock_transcript
    mock_api.list_transcripts.return_value = mock_transcripts

    svc = TranscriptService()
    text = svc.fetch_transcript_text("abc123")
    assert text == "This is a test"
