# backend/schemas/irrigation_input.py

from pydantic import BaseModel, Field
from backend.core.config import INPUT_LIMITS

class IrrigationInput(BaseModel):
    Region: str
    Crop_Type: str
    Soil_Type: str
    Season: str

    Farm_Area: float = Field(..., ge=INPUT_LIMITS["farm_area"][0], le=INPUT_LIMITS["farm_area"][1], description="Farm_Area (acres)")
    Soil_pH: float = Field(..., ge=INPUT_LIMITS["ph"][0], le=INPUT_LIMITS["ph"][1])
    Nitrogen: float = Field(..., ge=INPUT_LIMITS["n"][0], le=INPUT_LIMITS["n"][1])
    Phosphorus: float = Field(..., ge=INPUT_LIMITS["p"][0], le=INPUT_LIMITS["p"][1])
    Potassium: float = Field(..., ge=INPUT_LIMITS["k"][0], le=INPUT_LIMITS["k"][1])
    Soil_Moisture: float = Field(..., ge=INPUT_LIMITS["soil_moisture"][0], le=INPUT_LIMITS["soil_moisture"][1])
    Temperature: float = Field(..., ge=INPUT_LIMITS["temperature"][0], le=INPUT_LIMITS["temperature"][1], description="Temperature °C")
    Rainfall: float = Field(..., ge=INPUT_LIMITS["rainfall"][0], le=INPUT_LIMITS["rainfall"][1], description="Rainfall mm")
