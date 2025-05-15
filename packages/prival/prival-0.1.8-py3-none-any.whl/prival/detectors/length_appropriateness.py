# detectors/length_appropriateness.py
from ..utils.nlp_helpers import sentence_length

def detect_length_appropriateness(prompt: str, min_len: int = 10, max_len: int = 200) -> dict:
    length = sentence_length(prompt)
    score = 1.0 if min_len <= length <= max_len else 0.5
    suggestions = []
    if length < min_len:
        suggestions.append(f"Prompt 太短（{length}），建议至少 {min_len} 个词。")
    if length > max_len:
        suggestions.append(f"Prompt 太长（{length}），建议不超过 {max_len} 个词。")
    return {"score": score, "suggestions": suggestions}