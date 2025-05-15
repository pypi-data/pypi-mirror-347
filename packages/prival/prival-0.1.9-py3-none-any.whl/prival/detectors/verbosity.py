# detectors/verbosity.py
from ..utils.nlp_helpers import sentence_length

def detect_verbosity(prompt: str) -> dict:
    length = sentence_length(prompt)
    score = 1.0 if length < 60 else max(0.0, 1.0 - (length-60)/200)
    suggestions = []
    if length > 80:
        suggestions.append("Prompt 内容冗长，考虑精简无关信息。")
    return {"score": round(score,2), "suggestions": suggestions}