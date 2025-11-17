# backend/schemas/crop_input.py

from pydantic import BaseModel, Field
from backend.core.config import INPUT_LIMITS

class CropInput(BaseModel):
    N: float = Field(..., ge=INPUT_LIMITS["n"][0], le=INPUT_LIMITS["n"][1], description="Nitrogen (kg/ha)")
    P: float = Field(..., ge=INPUT_LIMITS["p"][0], le=INPUT_LIMITS["p"][1], description="Phosphorus (kg/ha)")
    K: float = Field(..., ge=INPUT_LIMITS["k"][0], le=INPUT_LIMITS["k"][1], description="Potassium (kg/ha)")
    ph: float = Field(..., ge=INPUT_LIMITS["ph"][0], le=INPUT_LIMITS["ph"][1], description="Soil pH")
    temperature: float = Field(..., ge=INPUT_LIMITS["temperature"][0], le=INPUT_LIMITS["temperature"][1], description="Temperature °C")
    humidity: float = Field(..., ge=INPUT_LIMITS["humidity"][0], le=INPUT_LIMITS["humidity"][1], description="Humidity %")
    rainfall: float = Field(..., ge=INPUT_LIMITS["rainfall"][0], le=INPUT_LIMITS["rainfall"][1], description="Rainfall mm/day")
