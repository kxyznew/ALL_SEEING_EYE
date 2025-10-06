from typing import List, Optional

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript


class TranscriptService:
    def __init__(self, languages: Optional[list[str]] = None) -> None:
        self.languages = languages or ["en", "en-US", "en-GB", "auto"]

    def fetch_transcript_text(self, video_id: str) -> str:
        """
        Fetch transcript as a single concatenated string.
        Preserves minimal spacing between segments (single space between non-empty parts).
        """
        segments = self.fetch_segments(video_id)
        non_empty_parts = [segment["text"].strip() for segment in segments if segment.get("text")]
        return " ".join(part for part in non_empty_parts if part)

    def fetch_segments(self, video_id: str) -> List[dict]:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        except (TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript) as e:
            raise RuntimeError(f"Transcript not available: {e}")
        # Prefer manually created, else auto-generated in preferred languages
        try:
            transcript = transcript_list.find_generated_transcript(self.languages)
        except Exception:
            # Fallback to any transcript
            transcript = transcript_list.find_transcript(self.languages)
        return transcript.fetch()
