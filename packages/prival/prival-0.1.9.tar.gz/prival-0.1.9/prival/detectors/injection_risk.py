# detectors/injection_risk.py
import re

def detect_injection_risk(prompt: str) -> dict:
    patterns = [r"\bignore previous\b", r"\bmalicious\b"]
    hits = [p for p in patterns if re.search(p, prompt, re.IGNORECASE)]
    score = 1.0 - len(hits)*0.5
    suggestions = ["检测到潜在注入风险模式：%s" % h for h in hits]
    return {"score": max(score,0.0), "suggestions": suggestions}