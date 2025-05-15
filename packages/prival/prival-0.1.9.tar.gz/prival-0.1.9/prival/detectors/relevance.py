# detectors/relevance.py
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def detect_relevance(prompt: str, reference: str = None) -> dict:
    if reference:
        sim = util.cos_sim(model.encode(prompt), model.encode(reference)).item()
    else:
        sim = 0.5
    score = sim
    suggestions = []
    return {"score": round(score,2), "suggestions": suggestions}