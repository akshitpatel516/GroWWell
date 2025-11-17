# backend/core/config.py

import os

# Folder for saved models
MODEL_PATHS = {
    "crop": os.path.join(os.path.dirname(__file__), "..", "models", "crop_best.pkl"),
    "fertilizer": os.path.join(os.path.dirname(__file__), "..", "models", "fertilizer_best_model.pkl"),
    "irrigation": os.path.join(os.path.dirname(__file__), "..", "models", "irrigation_best_model.pkl"),
}

# Unified input limits for validation (final, agreed values)
INPUT_LIMITS = {
    "n": [0, 200],            
    "p": [0, 200],            
    "k": [0, 250],            
    "ph": [3.5, 10.0],        
    "temperature": [0, 55],   
    "humidity": [0, 100],     
    "rainfall": [0, 500],     
    "soil_moisture": [0, 100],
    "farm_area": [0.1, 100.0]    
}

# Crop mapping (numeric prediction → name) — preserved exactly as you provided
CROP_MAPPING = [
    'apple', 'banana', 'blackgram', 'chickpea', 'coconut', 'coffee', 'cotton', 'grapes', 
    'jute', 'kidneybeans', 'lentil', 'maize', 'mango', 'mothbeans', 'mungbean', 'muskmelon', 
    'orange', 'papaya', 'pigeonpeas', 'pomegranate', 'rice', 'watermelon'
]

# Fertilizer mapping — preserved exactly as you provided
FERTILIZER_MAPPING = [
    'Urea', 'DAP', 'Potassium chloride', '17-17-17 ', '28-28', '20-20', '10-26-26', 
    'Superphosphate', '14-14-14', 'TSP'
]
