from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import numpy as np

app = FastAPI(
    title="Nigeria Economic Predictor",
    description="Predicts GDP based on multiple economic indicators",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionInput(BaseModel):
    year: int = Field(..., ge=2024, le=2050)
    population_growth: float = Field(..., ge=-5, le=10)
    agricultural_land_percent: float = Field(..., ge=0, le=100)
    literacy_rate: float = Field(..., ge=0, le=100)
    oil_price: float = Field(..., ge=0, le=200)

@app.get("/")
def read_root():
    return {"message": "Welcome to Nigeria Economic Predictor API"}

@app.post('/predict')
def predict(data: PredictionInput):
    try:
        # Temporary mock prediction
        mock_gdp = 2500 + (data.year - 2024) * 100
        return {
            "predicted_gdp": mock_gdp,
            "input_data": data.dict(),
            "note": "This is a mock prediction for testing"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
