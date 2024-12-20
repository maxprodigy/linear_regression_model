from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
import pickle
import numpy as np

app = FastAPI(title="Nigeria GDP Predictor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_DIR = os.path.join(os.getcwd(), "models")

def load_models():
    try:
        models = {}
        models['linear'] = pickle.load(open(os.path.join(MODEL_DIR, 'nigeria_gdp_linear_model.pkl'), 'rb'))
        models['x_scaler'] = pickle.load(open(os.path.join(MODEL_DIR, 'nigeria_gdp_X_scaler.pkl'), 'rb'))
        models['y_scaler'] = pickle.load(open(os.path.join(MODEL_DIR, 'nigeria_gdp_y_scaler.pkl'), 'rb'))
        return models
    except Exception as e:
        print(f"Error loading models: {str(e)}")
        return None

MODELS = load_models()

class GDPPredictionInput(BaseModel):
    year: int = Field(..., ge=2024, le=2050)

@app.get("/")
def read_root():
    return {
        "message": "Nigeria GDP Prediction API",
        "models_loaded": MODELS is not None
    }

@app.post("/predict")
def predict(data: GDPPredictionInput):
    try:
        year = np.array([[data.year]])
        year_scaled = MODELS['x_scaler'].transform(year)
        prediction = MODELS['linear'].predict(year_scaled.reshape(1, -1))
        final_prediction = MODELS['y_scaler'].inverse_transform(prediction.reshape(-1, 1))
        
        return {
            "year": data.year,
            "predicted_gdp": float(final_prediction[0][0])
        }
    except Exception as e:
        # Fallback prediction
        base_gdp = 2000
        years_from_2024 = data.year - 2024
        return {
            "year": data.year,
            "predicted_gdp": base_gdp + (years_from_2024 * 100),
            "note": "Using fallback prediction due to error: " + str(e)
        }
