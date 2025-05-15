# prival/prival/detectors/structural_cleanness.py

# 1. 捕获 spacy 不存在的情况
try:
    import spacy
except ImportError:
    spacy = None

from ..utils.nlp_helpers import dependency_depth, sentence_length
# …其它 imports…

def structural_cleanness(prompt: str):
    # 2. 如果没有安装 spaCy，就跳过
    if spacy is None:
        return {
            "score": None,
            "suggestions": ["spaCy not installed; structural_cleanness skipped."]
        }

    # 原有的 spaCy 分析逻辑，例如：
    # nlp = spacy.load("en_core_web_sm")
    # doc = nlp(prompt)
    # depth = dependency_depth(doc)
    # …计算分数、生成 suggestions …

    # 最终返回一个 dict
    return {"score": computed_score, "suggestions": suggestions}