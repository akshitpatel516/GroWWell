# backend/routes/irrigation.py

from fastapi import APIRouter
from backend.schemas.irrigation_input import IrrigationInput
from backend.services.irrigation_service import predict_irrigation

router = APIRouter(prefix="/irrigation", tags=["Irrigation"])

@router.post("/predict")
def irrigation_prediction(input: IrrigationInput):
    return predict_irrigation(
        crop_type=input.Crop_Type,
        soil_type=input.Soil_Type,
        season=input.Season,
        farm_area=input.Farm_Area,
        soil_moisture=input.Soil_Moisture,
        temperature=input.Temperature,
        rainfall=input.Rainfall,
        n=input.Nitrogen if hasattr(input, "Nitrogen") else input.Nitrogen,
        p=input.Phosphorus,
        k=input.Potassium,
        ph=input.Soil_pH,
        region=input.Region
    )
