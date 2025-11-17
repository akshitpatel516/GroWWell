# backend/routes/fertilizer.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.schemas.fertilizer_input import FertilizerInput
from backend.services.fertilizer_service import recommend_fertilizer

router = APIRouter(prefix="/fertilizer", tags=["Fertilizer"])

@router.post("/recommend")
def fertilizer_recommendation(payload: FertilizerInput):
    try:
        result = recommend_fertilizer({
            "Temparature": payload.Temparature,
            "Humidity": payload.Humidity,
            "Moisture": payload.Moisture,
            "Soil_Type": payload.Soil_Type,
            "Crop_Type": payload.Crop_Type,
            "Nitrogen": payload.Nitrogen,
            "Potassium": payload.Potassium,
            "Phosphorous": payload.Phosphorous
        })

        # Always return fertilizer name
        return JSONResponse(content={"fertilizer": result})

    except Exception as e:
        return JSONResponse(content={"error": "Fertilizer prediction failed", "details": str(e)})
