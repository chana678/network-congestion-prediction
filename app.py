from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

# Load model
model = joblib.load("model.pkl")

# Define feature order (VERY IMPORTANT)
FEATURES = [
    'total_bytes', 'total_packets', 'num_flows',
    'bytes_per_sec', 'packets_per_sec', 'flows_per_sec',
    'avg_packet_size', 'bytes_rolling_mean', 'bytes_rolling_std'
]

@app.get("/")
def home():
    return {"message": "Network Congestion Prediction API"}

@app.post("/predict")
def predict(data: dict):
    try:
        # Extract features in correct order
        input_data = [data[feature] for feature in FEATURES]
        
        prediction = model.predict([input_data])[0]
        
        return {
            "congestion": int(prediction)
        }
    
    except Exception as e:
        return {"error": str(e)}