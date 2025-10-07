from __future__ import annotations
from typing import Any, Dict, Optional
from pathlib import Path
import yaml

_PROMPTS_PATH = Path("prompts/parahelp.yaml")

_DEFAULT = {
    "summarize": {
        "system": (
            "You are ParaHelp, an expert study note-taker. Extract 5-7 concise, non-redundant "
            "key points that capture facts, definitions, steps, or big ideas. Avoid filler."
        ),
        "user_prefix": "Transcript:"
    },
    "explain": {
        "system": (
            "You are ParaHelp, a patient teacher. Explain these key points to a 7-year-old "
            "using short sentences, simple words, and friendly tone. Use bullets."
        ),
        "user_prefix": "Key points:"
    }
}

_cached: Optional[Dict[str, Any]] = None
_cached_mtime: Optional[float] = None


def load_parahelp_prompts() -> Dict[str, Any]:
    global _cached, _cached_mtime
    try:
        if _PROMPTS_PATH.exists():
            mtime = _PROMPTS_PATH.stat().st_mtime
            if _cached is None or _cached_mtime != mtime:
                with _PROMPTS_PATH.open("r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                # Merge with defaults
                merged = _DEFAULT.copy()
                for k, v in (data or {}).items():
                    if isinstance(v, dict) and k in merged:
                        merged[k] = {**merged[k], **v}
                    else:
                        merged[k] = v
                _cached = merged
                _cached_mtime = mtime
            return _cached or _DEFAULT
    except Exception:
        # On any parse error, fall back to defaults
        return _DEFAULT
    return _DEFAULT
