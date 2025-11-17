# backend/services/fertilizer_service.py
import joblib
import pandas as pd
from backend.core.config import MODEL_PATHS, FERTILIZER_MAPPING

# Load model
try:
    model = joblib.load(MODEL_PATHS["fertilizer"])
except Exception as e:
    raise RuntimeError(f"Failed to load fertilizer model: {str(e)}")

def recommend_fertilizer(input_data: dict):
    """
    input_data keys (from Streamlit):
    'Temparature', 'Humidity', 'Moisture', 'Soil_Type', 'Crop_Type',
    'Nitrogen', 'Potassium', 'Phosphorous'
    """

    try:
        # Convert input to DataFrame (1 row)
        df = pd.DataFrame([input_data])

        # Rename columns to match model training
        df.rename(columns={
            "Temparature": "Temperature",
            "Moisture": "Soil_Moisture"
        }, inplace=True)

        # Predict numeric label
        predicted_label = model.predict(df)[0]

        # Map numeric label to fertilizer name
        try:
            predicted_fertilizer = FERTILIZER_MAPPING[int(predicted_label)]
        except:
            predicted_fertilizer = str(predicted_label)

        return predicted_fertilizer

    except Exception as e:
        return {"error": "Fertilizer prediction failed", "details": str(e)}
