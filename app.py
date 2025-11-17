# app.py - Interactive GrowWell Dashboard
import streamlit as st
import os
from PIL import Image
from backend.services.crop_service import recommend_crop
from backend.services.fertilizer_service import recommend_fertilizer
from backend.services.irrigation_service import predict_irrigation
from backend.core.config import INPUT_LIMITS, CROP_MAPPING, FERTILIZER_MAPPING
import requests

# -------------------- Backend URL --------------------
# Use Docker service name 'backend' if running in Docker; fallback to localhost
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# -------------------- Static Dropdown Options --------------------
REGIONS = ["North India", "South India", "East India", "West India", "Central India"]
SOIL_TYPES = ["Sandy", "Loamy", "Clay", "Silty"]
SEASONS = ["Rabi", "Kharif", "Zaid"]

F_CROP_TYPES = [
    "Pomegranate", "Tomato", "Wheat", "Watermelon", "Maize", "Oil seeds",
    "Ground Nuts"
]

# ---------- Page Title ----------
st.set_page_config(page_title="🌱 GrowWell Dashboard", layout="wide")
st.markdown("<h1 style='color:#1b7a32'>🌱 GrowWell - Smart Farming Dashboard</h1>", unsafe_allow_html=True)
st.write("Predict the best crop, fertilizer, and irrigation requirements in real-time.")

# ---------- Tabs ----------
tab_crop, tab_fert, tab_irrig = st.tabs(["🌾 Crop Recommendation", "🧪 Fertilizer Recommendation", "💧 Irrigation Prediction"])

# -------------------- Crop Tab --------------------
with tab_crop:
    st.header("🌾 Crop Recommendation")
    col1, col2, col3 = st.columns(3)
    n = col1.slider("Nitrogen (kg/ha)", INPUT_LIMITS["n"][0], INPUT_LIMITS["n"][1], value=0, key="crop_n")
    p = col2.slider("Phosphorus (kg/ha)", INPUT_LIMITS["p"][0], INPUT_LIMITS["p"][1], value=0, key="crop_p")
    k = col3.slider("Potassium (kg/ha)", INPUT_LIMITS["k"][0], INPUT_LIMITS["k"][1], value=0, key="crop_k")

    col4, col5, col6 = st.columns(3)
    ph = col4.slider("Soil pH", INPUT_LIMITS["ph"][0], INPUT_LIMITS["ph"][1], value=6.5, key="crop_ph")
    temperature = col5.slider("Temperature (°C)", INPUT_LIMITS["temperature"][0], INPUT_LIMITS["temperature"][1], value=25, key="crop_temp")
    humidity = col6.slider("Humidity (%)", INPUT_LIMITS["humidity"][0], INPUT_LIMITS["humidity"][1], value=50, key="crop_humidity")

    rainfall = st.slider("Rainfall (mm/day)", INPUT_LIMITS["rainfall"][0], INPUT_LIMITS["rainfall"][1], value=0, key="crop_rainfall")

    if st.button("Predict Crop", key="predict_crop_btn"):
        with st.spinner("Predicting the best crop..."):
            try:
                crop_result = recommend_crop(n, p, k, ph, temperature, humidity, rainfall)
                if isinstance(crop_result, dict) and "error" in crop_result:
                    st.error(crop_result["error"])
                    if "details" in crop_result:
                        st.json(crop_result["details"])
                else:
                    st.success(f"🌾 Recommended Crop: **{crop_result}**")

                    # Display crop image
                    crop_image_jpg = os.path.join("assets", "crops", f"{crop_result.lower()}.jpg")
                    crop_image_webp = os.path.join("assets", "crops", f"{crop_result.lower()}.webp")
                    image_path = crop_image_webp if os.path.exists(crop_image_webp) else crop_image_jpg if os.path.exists(crop_image_jpg) else None

                    if image_path:
                        image = Image.open(image_path)
                        st.image(image, caption=crop_result, width=300)
                    else:
                        st.info(f"No image available for {crop_result}.")
            except Exception as e:
                st.error(f"Crop prediction failed: {str(e)}")

# -------------------- Fertilizer Tab --------------------
with tab_fert:
    st.header("🧪 Fertilizer Recommendation")
    st.info("Enter all soil and crop parameters below to get the best fertilizer recommendation.")

    # Input Sliders
    col1, col2, col3 = st.columns(3)
    f_temp = col1.slider("Temperature (°C)", INPUT_LIMITS["temperature"][0], INPUT_LIMITS["temperature"][1], value=25)
    f_humidity = col2.slider("Humidity (%)", INPUT_LIMITS["humidity"][0], INPUT_LIMITS["humidity"][1], value=50)
    f_moisture = col3.slider("Soil Moisture (%)", INPUT_LIMITS["soil_moisture"][0], INPUT_LIMITS["soil_moisture"][1], value=30)

    col4, col5, col6 = st.columns(3)
    f_n = col4.slider("Nitrogen (kg/ha)", INPUT_LIMITS["n"][0], INPUT_LIMITS["n"][1], value=50)
    f_p = col5.slider("Phosphorus (kg/ha)", INPUT_LIMITS["p"][0], INPUT_LIMITS["p"][1], value=30)
    f_k = col6.slider("Potassium (kg/ha)", INPUT_LIMITS["k"][0], INPUT_LIMITS["k"][1], value=20)

    col7, col8 = st.columns(2)
    f_soil = col7.selectbox("Soil Type", ["Loamy", "Sandy", "Clayey", "Red", "Black"])
    f_crop = col8.selectbox("Crop Type", F_CROP_TYPES)

    if st.button("Predict Fertilizer", key="predict_fert_btn"):
        with st.spinner("Analyzing soil & crop..."):
            try:
                payload = {
                    "Temparature": f_temp,
                    "Humidity": f_humidity,
                    "Moisture": f_moisture,
                    "Soil_Type": f_soil,
                    "Crop_Type": f_crop,
                    "Nitrogen": f_n,
                    "Potassium": f_k,
                    "Phosphorous": f_p
                }

                response = requests.post(f"{BACKEND_URL}/fertilizer/recommend", json=payload, timeout=10)
                data = response.json()

                if "fertilizer" in data:
                    st.success(f"🧪 Recommended Fertilizer: **{data['fertilizer']}**")
                elif "error" in data:
                    st.error(data["error"])
                    if "details" in data:
                        st.json(data["details"])
                else:
                    st.error(f"Unexpected response: {data}")

            except Exception as e:
                st.error(f"Fertilizer prediction failed: {str(e)}")

# -------------------- Irrigation Tab --------------------
with tab_irrig:
    st.header("💧 Irrigation Prediction")
    col1, col2 = st.columns(2)
    region = col1.selectbox("Region", REGIONS, key="ir_region")
    soil_type = col1.selectbox("Soil Type", SOIL_TYPES, key="ir_soil_type")
    season = col1.selectbox("Season", SEASONS, key="ir_season")

    farm_area = col2.slider("Farm Area (acres)", INPUT_LIMITS["farm_area"][0], INPUT_LIMITS["farm_area"][1], value=1.0, key="ir_farm_area")
    soil_moisture = col2.slider("Soil Moisture (%)", INPUT_LIMITS["soil_moisture"][0], INPUT_LIMITS["soil_moisture"][1], value=30, key="ir_soil_moisture")
    ir_temp = col2.slider("Temperature (°C)", INPUT_LIMITS["temperature"][0], INPUT_LIMITS["temperature"][1], value=25, key="ir_temp")
    ir_rain = col2.slider("Rainfall (mm)", INPUT_LIMITS["rainfall"][0], INPUT_LIMITS["rainfall"][1], value=0, key="ir_rain")
    ir_n = col2.slider("Nitrogen (kg/ha)", INPUT_LIMITS["n"][0], INPUT_LIMITS["n"][1], value=0, key="ir_n")
    ir_p = col2.slider("Phosphorus (kg/ha)", INPUT_LIMITS["p"][0], INPUT_LIMITS["p"][1], value=0, key="ir_p")
    ir_k = col2.slider("Potassium (kg/ha)", INPUT_LIMITS["k"][0], INPUT_LIMITS["k"][1], value=0, key="ir_k")
    ir_ph = col2.slider("Soil pH", INPUT_LIMITS["ph"][0], INPUT_LIMITS["ph"][1], value=6.5, key="ir_ph")
    f_crop_for_irrigation = col1.selectbox("Crop (for irrigation)", F_CROP_TYPES, key="ir_crop")

    if st.button("Predict Irrigation", key="predict_ir_btn"):
        with st.spinner("Estimating irrigation water usage..."):
            try:
                irrigation_result = predict_irrigation(
                    crop_type=f_crop_for_irrigation,
                    soil_type=soil_type,
                    season=season,
                    farm_area=farm_area,
                    soil_moisture=soil_moisture,
                    temperature=ir_temp,
                    rainfall=ir_rain,
                    n=ir_n,
                    p=ir_p,
                    k=ir_k,
                    ph=ir_ph,
                    region=region
                )
                if isinstance(irrigation_result, dict) and "error" in irrigation_result:
                    st.error(irrigation_result["error"])
                    if "details" in irrigation_result:
                        st.json(irrigation_result["details"])
                else:
                    st.success(f"💧 Recommended Irrigation: {irrigation_result} cubic meters")
                    st.metric(label="Estimated Irrigation (m³)", value=f"{irrigation_result}")
            except Exception as e:
                st.error(f"Irrigation prediction failed: {str(e)}")
