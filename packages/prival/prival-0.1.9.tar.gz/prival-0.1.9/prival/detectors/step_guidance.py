# detectors/step_guidance.py
from ..utils.nlp_helpers import tokenize

def detect_step_guidance(prompt: str) -> dict:
    tokens = tokenize(prompt)
    has_step = any(w in ["步骤","首先","然后","最后"] for w in tokens)
    score = 1.0 if has_step else 0.0
    suggestions = [] if has_step else ["建议在 prompt 中添加明确步骤提示，如'首先...'、'然后...'" ]
    return {"score": score, "suggestions": suggestions}# detectors/step_guidance.py