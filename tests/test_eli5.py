import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.eli5 import simplify_text


def test_simplify_empty():
    assert simplify_text("") == ""


def test_simplify_basic_shortening_and_replacements():
    text = "We will utilize a complex method to achieve the objective."
    out = simplify_text(text)
    assert "use" in out.lower()
    assert len(out) <= len(text) + 40  # allow small overhead for prefix
