from fastapi import APIRouter, UploadFile, File
from ..models import model
from ..utils.image import read_image
from ..recognition import recognize

router = APIRouter()

@router.post("")
async def recognize_frame(file: UploadFile = File(...)):
    data = await file.read()
    img = read_image(data)

    faces = model.get(img)

    results = []
    for f in faces:
        name, score = recognize(f.embedding)
        results.append({
            "bbox": f.bbox.astype(int).tolist(),
            "name": name,
            "score": score
        })

    return {"faces": results}
