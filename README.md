# OFI_SERVICES

## WOAS — Warehouse Optimization & Anomaly System

### Overview

WOAS (Warehouse Optimization & Anomaly System) is an AI-driven logistics tool built to analyze warehouse inventory and detect inefficiencies before they escalate.
It helps operations teams balance stock levels, propose transfers, and identify unusual inventory behaviors using unsupervised machine learning (Isolation Forest).

⸻

### Features

	•	AI Insights (Anomaly Detection):
Detects abnormal inventory behavior such as sudden stock drops, delayed restocks, or high storage costs.
	•	Warehouse Optimization:
Calculates surplus and deficit per warehouse and proposes efficient transfer strategies.
	•	Data Preview:
Displays a quick look at current inventory to verify correctness.
	•	Interactive Streamlit Dashboard:
Run, analyze, and download results in an easy-to-use interface.

____

### Project Structure

warehouse_optimizer/
│
├── app.py                      # Streamlit dashboard (main entry point)
├── anomaly_detection.py         # AI module for unsupervised anomaly detection
├── optimizer.py                 # Business logic for surplus/deficit and transfers
├── requirements.txt             # Dependencies
├── README.md                    # Project documentation
└── data/
    ├── warehouse_inventory.csv
    ├── cost_breakdown.csv
    ├── delivery_performance.csv
    ├── routes_distance.csv
    └── vehicle_fleet.csv

### How It Works

	1.	Loads warehouse data (e.g., stock, reorder level, and storage cost).
	2.	Computes surplus and deficit across warehouses.
	3.	Generates transfer proposals to rebalance inventory efficiently.
	4.	Runs Isolation Forest (unsupervised ML) to detect anomalies in stock, cost, or restock timing.
	5.	Displays results interactively with options to export findings.


  ### Tech Stack
  
	•	Python 3.12+
	•	Streamlit — Interactive UI
	•	Pandas, NumPy — Data wrangling
	•	Scikit-Learn (Isolation Forest) — ML-based anomaly detection
	•	ReportLab — (optional) For generating PDF briefs


### Author

Name: Vaibhav Simhaj
Role: AI & Data Engineering Intern
Organization: NexGen Logistics Pvt. Ltd.
Project: Warehouse Optimization & AI Insights System
