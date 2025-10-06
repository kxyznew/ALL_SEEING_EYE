import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.summarizer import summarize


def test_summarize_empty():
    s = summarize("")
    assert s.key_points == [] and s.top_sentences == []


def test_summarize_basic():
    text = (
        "Deep learning is a subset of machine learning. It uses neural networks. "
        "Neural networks learn hierarchical representations. This leads to strong results in vision and NLP. "
        "Training requires large datasets and compute."
    )
    s = summarize(text, max_points=3, max_sentences=3)
    assert 1 <= len(s.key_points) <= 3
    assert 1 <= len(s.top_sentences) <= 3
    # Top sentences should be subset of original sentences
    for ts in s.top_sentences:
        assert ts in text
