import numpy as np

def normalize(v):
    v = v.astype("float32")
    return v / (np.linalg.norm(v) + 1e-10)
