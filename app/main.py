from fastapi import FastAPI
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from .db import init_db
from .models import load_model
from .recognition import reload_gallery
import asyncio

from .api import enroll, recognize, people

@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()

    await loop.run_in_executor(None, init_db)
    await loop.run_in_executor(None, load_model)
    await loop.run_in_executor(None, reload_gallery)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(enroll.router, prefix="/api/enroll")
app.include_router(recognize.router, prefix="/api/recognize_frame")
app.include_router(people.router, prefix="/api/people")

@app.get("/")
def index():
    return FileResponse("app/static/index.html")
