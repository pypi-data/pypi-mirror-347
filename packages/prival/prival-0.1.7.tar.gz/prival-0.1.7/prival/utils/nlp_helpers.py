"""
NLP helper functions for PRIVAL. Guards against missing spaCy.
"""

try:
    import spacy
except ImportError:
    spacy = None

# Lazy-loaded spaCy model (English small by default)
_nlp = None
def _get_nlp(model_name: str = "en_core_web_sm"):
    global _nlp
    if spacy is None:
        return None
    if _nlp is None:
        try:
            _nlp = spacy.load(model_name)
        except Exception:
            _nlp = None
    return _nlp

def tokenize(text: str) -> list[str]:
    """
    分词：有 spaCy 则用它，否则按空白切分。
    """
    nlp = _get_nlp()
    if nlp:
        return [tok.text for tok in nlp(text)]
    return text.split()

def sentence_length(text: str) -> int:
    """
    句子长度（以词计数）：依赖 tokenize。
    """
    return len(tokenize(text))

def dependency_depth(doc) -> int:
    """
    句法依存树深度：需要传入 spaCy Doc；无 spaCy 时返回 0。
    """
    if spacy is None or doc is None:
        return 0
    # 计算最大依存链长度
    def depth(tok):
        if not list(tok.children):
            return 1
        return 1 + max(depth(child) for child in tok.children)
    return max(depth(sent.root) for sent in doc.sents)

# 你可以根据需要，继续添加其它工具（比如词性标注、命名实体等）