# Import required libraries
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel, Field
import pickle
import numpy as np
from typing import Dict

# Create FastAPI instance
app = FastAPI(
    title="Nigeria Economic Predictor",
    description="Predicts GDP based on multiple economic indicators",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the models we saved in Task 1
try:
    with open('models/nigeria_gdp_rf_enhanced_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('models/nigeria_gdp_X_scaler.pkl', 'rb') as f:
        X_scaler = pickle.load(f)
    with open('models/nigeria_gdp_y_scaler.pkl', 'rb') as f:
        y_scaler = pickle.load(f)
    print("Models loaded successfully!")
except FileNotFoundError:
    print("Error")
except Exception as e:
    print(f"Error loading models: {str(e)}")

class PredictionInput(BaseModel):
    year: int = Field(..., ge=2024, le=2050)
    population_growth: float = Field(..., ge=-5, le=10)
    agricultural_land_percent: float = Field(..., ge=0, le=100)
    literacy_rate: float = Field(..., ge=0, le=100)
    oil_price: float = Field(..., ge=0, le=200)

    class Config:
        schema_extra = {
            "example": {
                "year": 2024,
                "population_growth": 2.5,
                "agricultural_land_percent": 78.0,
                "literacy_rate": 62.0,
                "oil_price": 75.0
            }
        }

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Nigeria Economic Predictor API",
        "documentation": "/docs",
        "developer": "Your Name",
        "version": "1.0.0"
    }

@app.post('/predict')
def predict(data: PredictionInput) -> Dict:
    try:
        # Prepare input features
        features = np.array([[
            data.year,
            data.population_growth,
            data.agricultural_land_percent,
            data.literacy_rate,
            data.oil_price
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)
        
        return {
            "status": "success",
            "predicted_gdp": float(prediction[0]),
            "input_data": data.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
