import numpy as np
from .db import load_all_embeddings
from .utils.common import normalize
from .config import THRESHOLD

names = []
embeddings = None

def reload_gallery():
    global names, embeddings
    n, e = load_all_embeddings()
    names = n
    embeddings = np.array(e) if e else None

def recognize(embedding):
    if embeddings is None:
        return "unknown", 0.0

    emb = normalize(embedding)
    scores = embeddings @ emb
    idx = int(np.argmax(scores))
    score = float(scores[idx])

    if score < THRESHOLD:
        return "unknown", score

    return names[idx], score
