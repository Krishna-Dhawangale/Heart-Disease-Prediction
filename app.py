from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pickle
import numpy as np
import pandas as pd
import os

app = FastAPI()

# Mount static files (HTML, CSS)
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Load the model with robust path handling
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.pkl")

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    logger.info("Successfully loaded model")
except Exception as e:
    logger.error(f"Failed to load model from {model_path}: {str(e)}")
    model = None # Fallback or handle later

# Define the prediction input schema
class PredictionInput(BaseModel):
    age: int
    sex: int
    cp: int # chest pain type (0-3)
    trestbps: int # resting blood pressure
    chol: int # serum cholestoral
    fbs: int # fasting blood sugar > 120 (0/1)
    restecg: int # resting electrocardiographic results (0-2)
    thalach: int # max heart rate
    exang: int # exercise induced angina (0/1)
    oldpeak: float # ST depression
    slope: int # ST slope (0-2)
    ca: int # number of major vessels (0-4)
    thal: int # 0-3

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open(os.path.join(BASE_DIR, "static", "index.html"), "r") as f:
        return f.read()

@app.post("/predict")
async def predict(data: PredictionInput):
    if model is None:
        return {"error": "Model not loaded. Check logs for details."}, 500
    
    # Features as expected by the model (needs to be a DataFrame to avoid warnings)
    features_df = pd.DataFrame([{
        'age': data.age,
        'sex': data.sex,
        'cp': data.cp,
        'trestbps': data.trestbps,
        'chol': data.chol,
        'fbs': data.fbs,
        'restecg': data.restecg,
        'thalach': data.thalach,
        'exang': data.exang,
        'oldpeak': data.oldpeak,
        'slope': data.slope,
        'ca': data.ca,
        'thal': data.thal
    }])
    
    prediction = model.predict(features_df)
    probability = model.predict_proba(features_df)[0][1] # Probability of heart disease
    
    return {
        "prediction": int(prediction[0]),
        "probability": round(float(probability) * 100, 2)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)