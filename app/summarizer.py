from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import List


_STOPWORDS = set(
    """
    a an the and or but if then else when while of to in on for with at by from up down out over under again further
    is are was were be been being do does did doing have has had having not no nor so too very can will just should
    you your yours me my mine we our ours they their them he him his she her hers it its this that these those as
    """.split()
)


def _sentences(text: str) -> List[str]:
    # naive split on punctuation; keeps abbreviations simple
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def _tokenize(text: str) -> List[str]:
    tokens = re.findall(r"[A-Za-z']+", text.lower())
    return [t for t in tokens if t not in _STOPWORDS]


@dataclass
class Summary:
    key_points: List[str]
    top_sentences: List[str]


def summarize(text: str, max_points: int = 7, max_sentences: int = 5) -> Summary:
    if not text or not text.strip():
        return Summary(key_points=[], top_sentences=[])

    sentences = _sentences(text)
    if not sentences:
        return Summary(key_points=[], top_sentences=[])

    # Build word frequency
    word_freq = Counter()
    for s in sentences:
        word_freq.update(_tokenize(s))

    if not word_freq:
        return Summary(key_points=sentences[:max_points], top_sentences=sentences[:max_sentences])

    # Score sentences by sum of word frequencies, normalized by sentence length
    sentence_scores = []
    for s in sentences:
        tokens = _tokenize(s)
        if not tokens:
            sentence_scores.append((0.0, s))
            continue
        score = sum(word_freq[t] for t in tokens) / math.sqrt(len(tokens))
        sentence_scores.append((score, s))

    sentence_scores.sort(key=lambda x: x[0], reverse=True)

    top_sentences = [s for _, s in sentence_scores[:max_sentences]]

    # Derive key points as bullet-like short phrases: take first clause up to ~120 chars
    key_points = []
    for s in top_sentences:
        clause = re.split(r"[.;:!?]", s)[0]
        clause = clause.strip()
        if len(clause) > 120:
            clause = clause[:117].rstrip() + "..."
        if clause and clause not in key_points:
            key_points.append(clause)
        if len(key_points) >= max_points:
            break

    return Summary(key_points=key_points, top_sentences=top_sentences)
