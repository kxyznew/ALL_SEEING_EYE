from typing import List, Dict
import os

def simple_extractive_summary(lines: List[str], max_points: int = 7) -> List[str]:
    # naive: pick distinct longest lines as key points
    cleaned = [l.strip() for l in lines if l and len(l.strip()) > 20]
    uniq = []
    seen = set()
    for l in sorted(cleaned, key=len, reverse=True):
        key = l.lower()
        if key not in seen:
            uniq.append(l)
            seen.add(key)
        if len(uniq) >= max_points:
            break
    return uniq

def _try_llm_key_points(text: str, max_points: int = 7) -> List[str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return []
    try:
        from openai import OpenAI
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Extract the 5-7 most important points as concise bullets."},
                {"role": "user", "content": text[:8000]},
            ],
            temperature=0.2,
        )
        content = completion.choices[0].message.content or ""
        raw_lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
        cleaned: List[str] = []
        seen = set()
        for ln in raw_lines:
            ln = ln.lstrip("-•* ").strip()
            if len(ln) < 3:
                continue
            low = ln.lower()
            if low in seen:
                continue
            cleaned.append(ln)
            seen.add(low)
            if len(cleaned) >= max_points:
                break
        return cleaned
    except Exception:
        return []

def generate_key_points(lines: List[str], max_points: int = 7) -> List[str]:
    long_text = " ".join(lines)
    llm_points = _try_llm_key_points(long_text, max_points=max_points)
    if llm_points:
        return llm_points
    return simple_extractive_summary(lines, max_points=max_points)

def explain_like_child(key_points: List[str]) -> str:
    if not key_points:
        return "I couldn't find the main ideas."
    parts = []
    for kp in key_points[:5]:
        parts.append(f"- {kp}")
    return ("Here are the big ideas in simple words.\n" + "\n".join(parts) +
            "\nImagine you are telling a story to a friend. These are the steps.")

def build_quiz_question(key_points: List[str]) -> str:
    if not key_points:
        return "What is one idea you remember from the video?"
    return f"In your own words, explain: {key_points[0]}"

def grade_answer(question: str, answer: str, key_points: List[str]) -> str:
    if not answer.strip():
        return "Try to write a short sentence."
    if not key_points:
        return "Thanks! I can't check against notes, but that makes sense."
    good = 0
    for kp in key_points:
        if kp.lower()[:20] in answer.lower():
            good += 1
    if good:
        return "Nice! You mentioned an important idea."
    return "Good try. Re-read the key points and try again with one example."
