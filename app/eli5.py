import re
from typing import List


_SIMPLE_REPLACEMENTS = {
    "utilize": "use",
    "approximately": "about",
    "assistance": "help",
    "purchase": "buy",
    "objective": "goal",
    "assume": "think",
    "complex": "hard",
    "difficult": "hard",
    "advantage": "plus",
    "benefit": "good thing",
    "disadvantage": "bad thing",
    "requirement": "need",
    "method": "way",
    "function": "job",
    "however": "but",
    "therefore": "so",
    "consequently": "so",
    "nevertheless": "but",
    "approximately": "about",
    "individual": "person",
    "children": "kids",
    "sufficient": "enough",
}


def _split_sentences(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def _simplify_sentence(sentence: str, max_words: int = 24) -> str:
    # Remove parentheticals
    sentence = re.sub(r"\([^)]*\)", "", sentence)

    # Replace fancy words with simpler ones
    def replace_word(match: re.Match) -> str:
        word = match.group(0)
        lower = word.lower()
        simple = _SIMPLE_REPLACEMENTS.get(lower)
        if simple is None:
            return word
        # Keep capitalization if original was capitalized
        return simple.capitalize() if word[0].isupper() else simple

    sentence = re.sub(r"[A-Za-z']+", replace_word, sentence)

    # Split long sentences by commas/semicolons and keep the most informative first chunk
    chunks = re.split(r"[,;]\s+", sentence)
    if chunks:
        sentence = chunks[0].strip()

    # Trim to max words
    words = sentence.split()
    if len(words) > max_words:
        sentence = " ".join(words[:max_words]) + "..."

    # Ensure ends with a period
    if sentence and sentence[-1] not in ".!?":
        sentence += "."

    return sentence


def simplify_text(text: str, max_sentences: int = 6) -> str:
    if not text or not text.strip():
        return ""
    sentences = _split_sentences(text)
    simplified = [_simplify_sentence(s) for s in sentences[:max_sentences]]
    # Friendly ELI5 tone prefix for the first sentence
    if simplified:
        simplified[0] = "Imagine I'm your friend: " + simplified[0][0].lower() + simplified[0][1:]
    return " " .join(simplified)
