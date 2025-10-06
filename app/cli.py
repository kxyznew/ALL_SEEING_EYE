import argparse
import json
from pathlib import Path

from app.youtube_utils import extract_video_id
from app.transcript_service import TranscriptService
from app.summarizer import summarize


def main():
    parser = argparse.ArgumentParser(description="YouTube transcript summarizer")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--out", "-o", help="Output JSON file", default=None)
    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    if not video_id:
        raise SystemExit("Invalid YouTube URL")

    svc = TranscriptService()
    text = svc.fetch_transcript_text(video_id)
    summary = summarize(text)

    result = {
        "video_id": video_id,
        "key_points": summary.key_points,
        "top_sentences": summary.top_sentences,
    }

    if args.out:
        out_path = Path(args.out)
        out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"Saved to {out_path}")
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
