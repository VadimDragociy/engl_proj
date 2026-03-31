from insightface.app import FaceAnalysis
from .config import USE_GPU

model = FaceAnalysis(name="buffalo_l")

def load_model():
    global model
    model.prepare(ctx_id=0 if USE_GPU else -1)
    return model
