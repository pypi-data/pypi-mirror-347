# detectors/context_completeness.py

def detect_context_completeness(prompt: str) -> dict:
    # 简易：检测是否包含关键词示例或上下文标签
    has_context = '背景' in prompt or '示例' in prompt
    score = 1.0 if has_context else 0.5
    suggestions = [] if has_context else ["提示：如有必要，可添加背景或示例以提升上下文完整性。"]
    return {"score": score, "suggestions": suggestions}