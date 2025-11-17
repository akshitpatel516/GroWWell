from pydantic import BaseModel, Field
from backend.core.config import INPUT_LIMITS

class FertilizerInput(BaseModel):
    Temparature: float = Field(..., ge=INPUT_LIMITS["temperature"][0], le=INPUT_LIMITS["temperature"][1], alias="Temparature")
    Humidity: float = Field(..., ge=INPUT_LIMITS["humidity"][0], le=INPUT_LIMITS["humidity"][1], alias="Humidity")
    Moisture: float = Field(..., ge=INPUT_LIMITS["soil_moisture"][0], le=INPUT_LIMITS["soil_moisture"][1], alias="Moisture")
    Soil_Type: str = Field(..., alias="Soil_Type")
    Crop_Type: str = Field(..., alias="Crop_Type")
    Nitrogen: float = Field(..., ge=INPUT_LIMITS["n"][0], le=INPUT_LIMITS["n"][1], alias="Nitrogen")
    Potassium: float = Field(..., ge=INPUT_LIMITS["k"][0], le=INPUT_LIMITS["k"][1], alias="Potassium")
    Phosphorous: float = Field(..., ge=INPUT_LIMITS["p"][0], le=INPUT_LIMITS["p"][1], alias="Phosphorous")

    class Config:
        allow_population_by_field_name = True
