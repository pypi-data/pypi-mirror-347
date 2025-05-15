# detectors/feasibility.py
from ..utils.nlp_helpers import sentence_length

def detect_feasibility(prompt: str, max_tokens: int = 512) -> dict:
    length = sentence_length(prompt)
    score = 1.0 if length < max_tokens/2 else 0.5
    suggestions = []
    if length > max_tokens:
        suggestions.append("Prompt 太长，可能超出模型最大长度限制。")
    return {"score": score, "suggestions": suggestions}