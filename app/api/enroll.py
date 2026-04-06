from fastapi import APIRouter, UploadFile, File, Form
from ..models import model
from ..utils.image import read_image
from ..db import add_sample
from ..recognition import reload_gallery
from ..utils.common import normalize
from ..config import IMAGES_DIR
import cv2
import uuid

router = APIRouter()

@router.post("")
async def enroll(name: str = Form(...), files: list[UploadFile] = File(...)):
    added = 0

    for f in files:
        # print(10)
        data = await f.read()
        img = read_image(data)

        faces = model.get(img)
        if not faces:
            continue

        emb = normalize(faces[0].embedding)

        path = IMAGES_DIR / f"{uuid.uuid4()}.jpg"
        cv2.imwrite(str(path), img)

        add_sample(name, str(path), emb)
        added += 1

    reload_gallery()
    return {"added": added}
