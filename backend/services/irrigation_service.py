# backend/services/irrigation_service.py

import pandas as pd
import numpy as np
import joblib
import traceback
from backend.core.config import MODEL_PATHS, INPUT_LIMITS

# Load the trained irrigation model
try:
    model = joblib.load(MODEL_PATHS["irrigation"])
except Exception as e:
    raise RuntimeError(f"Failed to load irrigation model: {str(e)}")

def validate_irrigation_inputs(n, p, k, ph, temperature, rainfall, soil_moisture, farm_area):
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
    if not (INPUT_LIMITS["rainfall"][0] <= rainfall <= INPUT_LIMITS["rainfall"][1]):
        errors.append(f"Rainfall {rainfall} mm is out of range {INPUT_LIMITS['rainfall']}")
    if not (INPUT_LIMITS["soil_moisture"][0] <= soil_moisture <= INPUT_LIMITS["soil_moisture"][1]):
        errors.append(f"Soil moisture {soil_moisture}% is out of range {INPUT_LIMITS['soil_moisture']}")
    if not (INPUT_LIMITS["farm_area"][0] <= farm_area <= INPUT_LIMITS["farm_area"][1]):
        errors.append(f"Farm area {farm_area} is out of range {INPUT_LIMITS['farm_area']}")

    return errors

def predict_irrigation(crop_type, soil_type, season, farm_area, soil_moisture,
                       temperature, rainfall, n, p, k, ph, region):
    """
    Predict irrigation water usage in cubic meters.
    """

    try:
        # Validate inputs
        validation_errors = validate_irrigation_inputs(n, p, k, ph, temperature, rainfall, soil_moisture, farm_area)
        if validation_errors:
            return {"error": "Invalid input values", "details": validation_errors}

        # Prepare dataframe with exact column names (matching dataset)
        input_data = pd.DataFrame([{
            "Region": region,
            "Crop_Type": crop_type,
            "Soil_Type": soil_type,
            "Season": season,
            "Farm_Area(acres)": farm_area,
            "Soil_pH": ph,
            "Nitrogen(kg/ha)": n,
            "Phosphorus(kg/ha)": p,
            "Potassium(kg/ha)": k,
            "Soil_Moisture(%)": soil_moisture,
            "Temperature(°C)": temperature,
            "Rainfall(mm)": rainfall
        }])

        # Predict
        prediction = model.predict(input_data)[0]
        if isinstance(prediction, np.generic):
            prediction = prediction.item()

        return round(float(prediction), 2)

    except Exception as e:
        traceback.print_exc()
        return {"error": f"Irrigation prediction failed: {str(e)}"}
