from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pickle
import numpy as np

app = FastAPI(title="Nigeria GDP Predictor")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models with error handling
try:
    with open('models/nigeria_gdp_rf_enhanced_model.pkl', 'rb') as f:
        rf_model = pickle.load(f)
    with open('models/nigeria_gdp_linear_model.pkl', 'rb') as f:
        linear_model = pickle.load(f)
    with open('models/nigeria_gdp_X_scaler.pkl', 'rb') as f:
        X_scaler = pickle.load(f)
    with open('models/nigeria_gdp_y_scaler.pkl', 'rb') as f:
        y_scaler = pickle.load(f)
    print("Models loaded successfully!")
except Exception as e:
    print(f"Error loading models: {str(e)}")
    rf_model, linear_model, X_scaler, y_scaler = None, None, None, None

class GDPPredictionInput(BaseModel):
    year: int = Field(..., ge=2024, le=2050)

@app.get("/")
def read_root():
    return {"message": "Nigeria GDP Prediction API"}

@app.post("/predict")
def predict(data: GDPPredictionInput):
    if not all([rf_model, X_scaler, y_scaler]):
        raise HTTPException(status_code=500, detail="Models not properly loaded")
    
    try:
        year = np.array([[data.year]])
        year_scaled = X_scaler.transform(year)
        
        prediction = rf_model.predict(year_scaled)
        final_prediction = y_scaler.inverse_transform(prediction.reshape(-1, 1))
        
        return {
            "year": data.year,
            "predicted_gdp": float(final_prediction[0][0])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
