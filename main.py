# main.py

from fastapi import FastAPI
from backend.routes import crop, fertilizer, irrigation

app = FastAPI(title="GrowWell API - Smart Farming")

app.include_router(crop.router)
app.include_router(fertilizer.router)
app.include_router(irrigation.router)

@app.get("/")
def health():
    return {"status": "ok"}
