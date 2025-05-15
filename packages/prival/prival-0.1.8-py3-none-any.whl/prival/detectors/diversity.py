# detectors/diversity.py
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def detect_diversity(batch_prompts: list) -> dict:
    vec = TfidfVectorizer().fit_transform(batch_prompts)
    sim = (vec * vec.T).A
    avg_sim = np.mean(sim[np.triu_indices_from(sim, k=1)])
    score = 1 - avg_sim
    suggestions = []
    if avg_sim > 0.8:
        suggestions.append("批量 prompt 相似度过高，建议增加多样性。")
    return {"score": round(score,2), "suggestions": suggestions}