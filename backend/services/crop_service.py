# backend/services/crop_service.py

import joblib
import pandas as pd
import numpy as np
import traceback
from backend.core.config import MODEL_PATHS, INPUT_LIMITS, CROP_MAPPING

# Load crop model
try:
    model = joblib.load(MODEL_PATHS["crop"])
except Exception as e:
    raise RuntimeError(f"Failed to load crop model: {str(e)}")

def validate_crop_inputs(n, p, k, ph, temperature, humidity, rainfall):
    errors = []
    if not (INPUT_LIMITS["n"][0] <= n <= INPUT_LIMITS["n"][1]):
        errors.append(f"Nitrogen {n} kg/ha is out of range {INPUT_LIMITS['n']}")
    if not (INPUT_LIMITS["p"][0] <= p <= INPUT_LIMITS["p"][1]):
        errors.append(f"Phosphorus {p} kg/ha is out of range {INPUT_LIMITS['p']}")
    if not (INPUT_LIMITS["k"][0] <= k <= INPUT_LIMITS["k"][1]):
        errors.append(f"Potassium {k} kg/ha is out of range {INPUT_LIMITS['k']}")
    if not (INPUT_LIMITS["ph"][0] <= ph <= INPUT_LIMITS["ph"][1]):
        errors.append(f"Soil pH {ph} is out of range {INPUT_LIMITS['ph']}")
    if not (INPUT_LIMITS["temperature"][0] <= temperature <= INPUT_LIMITS["temperature"][1]):
        errors.append(f"Temperature {temperature}°C is out of range {INPUT_LIMITS['temperature']}")
    if not (INPUT_LIMITS["humidity"][0] <= humidity <= INPUT_LIMITS["humidity"][1]):
        errors.append(f"Humidity {humidity}% is out of range {INPUT_LIMITS['humidity']}")
    if not (INPUT_LIMITS["rainfall"][0] <= rainfall <= INPUT_LIMITS["rainfall"][1]):
        errors.append(f"Rainfall {rainfall} mm/day is out of range {INPUT_LIMITS['rainfall']}")
    return errors

def recommend_crop(n, p, k, ph, temperature, humidity, rainfall):
    try:
        errors = validate_crop_inputs(n, p, k, ph, temperature, humidity, rainfall)
        if errors:
            return {"error": "Invalid input values", "details": errors}

        df = pd.DataFrame([{
            "N": n,
            "P": p,
            "K": k,
            "ph": ph,
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall
        }])

        pred_index = model.predict(df)[0]
        pred_index = int(pred_index)
        crop_name = CROP_MAPPING[pred_index] if 0 <= pred_index < len(CROP_MAPPING) else "Unknown"
        return crop_name

    except Exception as e:
        traceback.print_exc()
        return {"error": f"Crop prediction failed: {str(e)}"}
