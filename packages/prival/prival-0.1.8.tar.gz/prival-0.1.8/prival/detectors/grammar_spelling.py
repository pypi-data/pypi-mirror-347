"""
Grammar and spelling detector for PRIVAL.
"""

try:
    from language_tool_python import LanguageTool
except Exception:
    LanguageTool = None


def grammar_spelling(prompt: str):
    """
    使用 LanguageTool 检测语法和拼写错误，如果不可用则跳过。
    """
    # 如果 LanguageTool 不可用，跳过此检测
    if LanguageTool is None:
        return {"score": None, "suggestions": ["LanguageTool not available; skipped grammar checks."]}

    # 尝试初始化 LanguageTool 服务
    try:
        tool = LanguageTool('en-US')
    except Exception:
        return {"score": None, "suggestions": ["Failed to start LanguageTool; skipped grammar checks."]}

    # 执行检查
    matches = tool.check(prompt)
    suggestions = []
    for match in matches:
        suggestions.append(f"{match.ruleId}: {match.message} at position {match.offset}")

    # 计算分数：错误越少得分越高
    length = len(prompt.split()) if prompt else 1
    score = max(0.0, 1.0 - len(matches) / length)
    return {"score": score, "suggestions": suggestions}
