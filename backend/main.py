from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Load model and scaler
model = joblib.load("heart_model.pkl")
scaler = joblib.load("heart_scaler.pkl")

# Define input schema
class PatientData(BaseModel):
    age: float
    sex: int
    cp: int
    trestbps: float
    chol: float
    fbs: int
    restecg: int
    thalach: float
    exang: int
    oldpeak: float
    slope: int
    ca: float
    thal: int

@app.post("/predict")
def predict(data: PatientData):
    # Convert input data to array
    features = np.array([[data.age, data.sex, data.cp, data.trestbps, data.chol,
                          data.fbs, data.restecg, data.thalach, data.exang,
                          data.oldpeak, data.slope, data.ca, data.thal]])
    
    # Scale features
    scaled = scaler.transform(features)
    
    # Predict probability
    prob = model.predict_proba(scaled)[0][1]
    prediction = int(prob > 0.5)

    return {
        "risk_score_percent": round(prob * 100, 2),
        "prediction": "High Risk" if prediction == 1 else "Low Risk"
    }
