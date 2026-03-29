# Network Traffic Congestion Prediction 🚦

## Summary
This project predicts future network congestion using machine learning on aggregated network traffic flow data. The solution transforms flow-level data into time-based network-level features and applies a Random Forest model for prediction.

---

## Problem Statement
Telecommunication networks often experience high traffic loads due to increasing data usage, streaming services, and IoT devices. Predicting congestion in advance helps in proactive bandwidth management and maintaining service quality.

The goal of this project is to predict whether the network will be **congested in the next time window**.

---

## Approach

### 1. Data Understanding
The dataset contains **flow-level network traffic data**, where each row represents a single network flow.

However, congestion is a **network-level phenomenon**, not a flow-level one.

---

### 2. Data Transformation (Key Insight)
To address this:
- Flow-level data was aggregated into **1-minute time windows**
- Each window represents the **overall state of the network**

---

### 3. Feature Engineering

#### Traffic Features
- `total_bytes`
- `total_packets`
- `num_flows`

#### Rate-based Features
- `bytes_per_sec`
- `packets_per_sec`
- `flows_per_sec`

#### Statistical Features
- `avg_packet_size`

#### Temporal Features
- `bytes_rolling_mean`
- `bytes_rolling_std`

These features capture **traffic intensity and temporal behavior**.

---

### 4. Label Creation
Since the dataset does not contain explicit congestion labels:

- Congestion is defined as the **top 10% of traffic windows** based on `total_bytes`
- This ensures a **data-driven definition**

---

### 5. Modeling Strategy

#### Baseline Model
- Predicted congestion in the same time window
- Achieved ~99% accuracy
- However, this was due to **label leakage**

---

#### Final Model (Improved)
- Reformulated problem to predict:
  
Features at time t → Congestion at time t+1


- This makes the model **predictive and realistic**

---

### 6. Model Used
- Random Forest Classifier
- Time-based train-test split
- Class weighting to handle imbalance

---

## Results

### Final Model Performance (Future Prediction)

- **Accuracy:** ~94–95%
- **Precision (Congestion):** 0.50
- **Recall (Congestion):** 0.38
- **F1-score (Congestion):** 0.43

---

## Key Insights

- Temporal features (rolling statistics) are highly important
- Flow-based features (`num_flows`, `flows_per_sec`) contribute significantly
- Instantaneous traffic features become less dominant in future prediction
- Congestion events are rare and harder to predict

---

## Challenges & Limitations

- No real congestion labels (used proxy definition)
- Congestion events are rare (~10%)
- Sudden traffic spikes reduce predictability
- Limited temporal context

---

## Improvements & Future Work

- Use longer temporal context (LSTM, time-series models)
- Incorporate real congestion signals (latency, packet loss)
- Tune threshold to improve recall
- Deploy streaming pipeline for real-time inference

---

## API: Real-Time Prediction

A simple FastAPI endpoint is provided to simulate real-time congestion prediction.

---

### How to Run the API

1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Start the API:
```bash
uvicorn app:app --reload
```
3. Open Swagger UI:
```bash
http://127.0.0.1:8000/docs
```

Endpoint
```bash
POST /predict
```

Sample Input(JSON)
Use this as a sample input in Swagger UI

{
  "total_bytes": 500000,
  "total_packets": 1000,
  "num_flows": 200,
  "bytes_per_sec": 8000,
  "packets_per_sec": 20,
  "flows_per_sec": 5,
  "avg_packet_size": 500,
  "bytes_rolling_mean": 450000,
  "bytes_rolling_std": 20000
}
Sample Output
{
  "congestion": 0,
  "message": "Not Congested"
}
or
{
  "congestion": 1,
  "message": "Congested"
}

### Project Structure

network-congestion-prediction/
│
├── notebook.ipynb        # Full ML pipeline
├── app.py                # FastAPI application
├── model.pkl             # Trained model
├── requirements.txt      # Dependencies
├── README.md             # Documentation

### How to run the project

1. Clone the repository

2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Open and run:
```bash
notebook.ipynb
```

#### Dataset
Dataset used:
Kaggle: IP Network Traffic Flows Dataset

#### Conclusion
This project demonstrates how flow-level network data can be transformed into a network-level representation to model congestion. While predicting future congestion is inherently challenging, the model captures meaningful temporal patterns and provides actionable insights.