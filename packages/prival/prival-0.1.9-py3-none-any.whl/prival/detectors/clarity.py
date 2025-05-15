# detectors/clarity.py
from ..utils.nlp_helpers import sentence_length

def detect_clarity(prompt: str) -> dict:
    length = sentence_length(prompt)
    score = 1.0 if length < 50 else max(0.0, 1.0 - (length - 50)/100)
    suggestions = []
    if length > 100:
        suggestions.append("Prompt 太长，建议拆分或简化。")
    return {"score": round(score, 2), "suggestions": suggestions}