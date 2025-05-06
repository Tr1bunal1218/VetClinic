from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.pet import router as pet_router
from src.api.medCard import router as card_router
from src.api.auth import router as auth_router
from src.api.doctors import router as doctors_router
from src.api.medInventory import router as med_router
from src.api.clinic import router as clinic_router
from src.config import settings
from src.db import *

app = FastAPI()
app.include_router(pet_router)
app.include_router(card_router)
app.include_router(auth_router)
app.include_router(doctors_router)
app.include_router(med_router)
app.include_router(clinic_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", port=8001)
