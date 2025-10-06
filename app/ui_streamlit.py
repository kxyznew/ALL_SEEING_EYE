import json
from datetime import datetime
from pathlib import Path
import streamlit as st

from app.youtube_utils import extract_video_id
from app.transcript_service import TranscriptService
from app.summarizer import summarize
from app.eli5 import simplify_text


st.set_page_config(page_title="YouTube Key Points (ELI5)", layout="wide")


@st.cache_data(show_spinner=False)
def _cached_transcript(video_id: str) -> str:
    svc = TranscriptService()
    return svc.fetch_transcript_text(video_id)


@st.cache_data(show_spinner=False)
def _cached_summary(text: str):
    s = summarize(text)
    return {"key_points": s.key_points, "top_sentences": s.top_sentences}


def _init_state():
    if "notes" not in st.session_state:
        st.session_state["notes"] = []
    if "last_result" not in st.session_state:
        st.session_state["last_result"] = None


def _save_text_button(label: str, content: str, file_prefix: str):
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    filename = f"{file_prefix}-{ts}.txt"
    st.download_button(label=label, data=content, file_name=filename, mime="text/plain")


def main():
    _init_state()
    st.title("YouTube Video Key Points and ELI5 Explainer")
    st.write("Paste a YouTube link, get the main points, and read simple explanations.")

    url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        do_summarize = st.button("Summarize")
    with col2:
        clear = st.button("Clear")
    with col3:
        eli5_all = st.button("ELI5 All Key Points")

    if clear:
        st.session_state["last_result"] = None
        st.session_state["notes"] = []

    if do_summarize:
        vid = extract_video_id(url)
        if not vid:
            st.error("Please enter a valid YouTube URL.")
        else:
            with st.spinner("Fetching transcript..."):
                try:
                    text = _cached_transcript(vid)
                except Exception as e:
                    st.error(f"Couldn't get transcript: {e}")
                    text = None
            if text:
                with st.spinner("Summarizing..."):
                    result = _cached_summary(text)
                    st.session_state["last_result"] = {"video_id": vid, "text": text, **result}

    result = st.session_state.get("last_result")
    if result:
        st.subheader("Key points")
        for idx, kp in enumerate(result["key_points"], start=1):
            with st.expander(f"{idx}. {kp}"):
                eli5_text = simplify_text(kp)
                st.write(eli5_text)
                c1, c2 = st.columns([1, 1])
                with c1:
                    if st.button(f"Add to Notes #{idx}"):
                        st.session_state["notes"].append(f"- {kp}\n  ELI5: {eli5_text}")
                        st.success("Added to notes.")
                with c2:
                    st.caption("Say it in your own words:")
                    st.text_area(f"Your explanation for point #{idx}", key=f"explain_{idx}", height=80)

        st.divider()
        st.subheader("Download")
        summary_text = "# Key Points\n" + "\n".join(f"- {kp}" for kp in result["key_points"]) + "\n\n# Top Sentences\n" + "\n".join(
            f"- {s}" for s in result["top_sentences"]
        )
        _save_text_button("Download Summary (.txt)", summary_text, file_prefix=f"summary-{result['video_id']}")

        notes_text = "\n".join(st.session_state["notes"]) if st.session_state["notes"] else "(no notes yet)"
        _save_text_button("Download Notes (.txt)", notes_text, file_prefix=f"notes-{result['video_id']}")

    if eli5_all and result:
        st.subheader("ELI5 for all key points")
        for idx, kp in enumerate(result["key_points"], start=1):
            st.markdown(f"**{idx}.** {simplify_text(kp)}")

    st.caption("Tip: You can run this via: streamlit run app/ui_streamlit.py")


if __name__ == "__main__":
    main()
