# detectors/ambiguity.py
import re
from ..utils.nlp_helpers import tokenize

def detect_ambiguity(prompt: str) -> dict:
    # 简单检测多义词列表
    ambiguous = [w for w in ["或者","可能","大概"] if w in prompt]
    score = 1.0 - len(ambiguous)*0.2
    suggestions = [f"检测到歧义词：{w}" for w in ambiguous]
    return {"score": max(score, 0.0), "suggestions": suggestions}