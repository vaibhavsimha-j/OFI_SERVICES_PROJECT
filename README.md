# OFI_SERVICES

## WOAS — Warehouse Optimization & Anomaly System

### Overview

WOAS (Warehouse Optimization & Anomaly System) is an AI-driven logistics tool built to analyze warehouse inventory and detect inefficiencies before they escalate.
It helps operations teams balance stock levels, propose transfers, and identify unusual inventory behaviors using unsupervised machine learning (Isolation Forest).

⸻

### Features
	
• **AI Insights (Anomaly Detection):**  
Detects abnormal inventory behavior such as sudden stock drops, delayed restocks, or high storage costs.

• **Warehouse Optimization:**  
Calculates surplus and deficit per warehouse and proposes efficient transfer strategies.

• **Data Preview:**  
Displays a quick look at current inventory to verify correctness.

• **Interactive Streamlit Dashboard:**  
Run, analyze, and download results in an easy-to-use interface.

____

### Project Structure

| Folder / File Path                         | Description |
|--------------------------------------------|-------------|
| `warehouse_optimizer/`                     | Root project directory |
| `WOAS-Innovation Brief.pdf`              |Detailed explanation of the project’s concept, innovation, and business value|
|  `app.py`                               | Main Streamlit application script |
| `anomaly_detection.py`                 | Contains ML-based anomaly detection logic |
| `optimizer.py`                         | Handles surplus/deficit analysis and transfer proposal logic |
|  `requirements.txt`                     | Python dependencies for the project |
|  `README.md`                            | Project documentation and usage guide |
|  `data/`                                | Folder containing dataset CSV files |
|   `warehouse_inventory.csv`            | Warehouse-level inventory data |
| `vehicle_fleet.csv`                  | Vehicle specifications and efficiency data |
|  `orders.csv`                         | Orders and delivery information |
|  `routes_distance.csv`                | Distance and route mapping data |
|  `cost_breakdown.csv`                 | Operational cost data |
|  `customer_feedback.csv`              | Feedback and sentiment data |
|  `delivery_performance.csv`           | Delivery performance metrics |
| `outputs/`                             | Generated output files (transfer proposals, anomalies) |
|  `transfer_proposals.csv`             | Recommended inter-warehouse transfers |
| `warehouse_anomalies.csv`            | Flagged anomalies in inventory data |
|  `venv/`                                | Virtual environment folder (optional, for isolated dependencies) |

### How It Works 

The tool uses warehouse inventory data to identify imbalances across locations and detect unusual stock patterns.
	•	Inventory Preview: Displays current stock information for validation.
	•	Warehouse Optimization: Calculates surplus and deficit levels, proposing efficient transfer routes.
	•	AI Insights (Anomaly Detection): Uses unsupervised machine learning to detect abnormal behavior such as sudden drops, delayed restocks, or excess stock.
All features are accessible through an interactive Streamlit dashboard for ease of analysis and visualization.
____

### Setup Instruction


To set up and run the Warehouse Optimization Tool: <br>
	1.	Clone or download the repository. <br>
Example: git clone https://github.com/<your-username>/warehouse_optimizer.git <br>
	2.	Navigate into the project directory. <br>
Command: cd warehouse_optimizer <br>
	3.	Create a virtual environment. <br>
Command: python3 -m venv venv <br>
	4.	Activate the virtual environment. <br>
macOS/Linux: source venv/bin/activate <br>
Windows: venv\Scripts\activate <br>
	5.	Install all required dependencies. <br>
Command: pip install -r requirements.txt <br>
	6.	Place all dataset CSV files inside the /data folder. <br>
Ensure warehouse_inventory.csv is present. <br>
	7.	Run the Streamlit application. <br>
Command: streamlit run app.py <br>
	8.	Open the local URL (usually http://localhost:8501) in your browser. <br>


____

  ### Tech Stack
  ‎
  ‎ 
	•	Python 3.12+
	•	Streamlit — Interactive UI
	•	Pandas, NumPy — Data wrangling
	•	Scikit-Learn (Isolation Forest) — ML-based anomaly detection

____

### Author

**Name:** Vaibhav Simhaj
**Role:** AI Intern
**Organization:** OFI Services
**Project:** Warehouse Optimization & AI Insights System
