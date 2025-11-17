# backend/routes/crop.py

from fastapi import APIRouter
from backend.schemas.crop_input import CropInput
from backend.services.crop_service import recommend_crop

router = APIRouter(prefix="/crop", tags=["Crop"])

@router.post("/recommend")
def crop_recommendation(input: CropInput):
    return recommend_crop(
        n=input.N,
        p=input.P,
        k=input.K,
        ph=input.ph,
        temperature=input.temperature,
        humidity=input.humidity,
        rainfall=input.rainfall
    )
