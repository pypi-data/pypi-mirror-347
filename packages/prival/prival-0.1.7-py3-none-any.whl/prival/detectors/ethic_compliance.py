# detectors/ethic_compliance.py

def detect_ethic_compliance(prompt: str) -> dict:
    # 简易词库检测
    blacklist = ['暴力','歧视','仇恨']
    hits = [w for w in blacklist if w in prompt]
    score = 1.0 if not hits else 0.0
    suggestions = [] if not hits else ["检测到不当词汇：%s" % w for w in hits]
    return {"score": score, "suggestions": suggestions}