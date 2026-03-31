from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = DATA_DIR / "images"
DB_PATH = DATA_DIR / "faces.sqlite3"

DATA_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)

THRESHOLD = float(os.getenv("FACE_THRESHOLD", "0.35"))
USE_GPU = os.getenv("USE_GPU", "0") == "1"
