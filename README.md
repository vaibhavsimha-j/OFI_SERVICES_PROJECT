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
‎ 
‎ 
	1.	Loads warehouse data (e.g., stock, reorder level, and storage cost).
	2.	Computes surplus and deficit across warehouses.
	3.	Generates transfer proposals to rebalance inventory efficiently.
	4.	Runs Isolation Forest (unsupervised ML) to detect anomalies in stock, cost, or restock timing.
	5.	Displays results interactively with options to export findings.

____

### Setup Instruction

‎ 
	1.	Clone or Download the Repository
	•	Download the project ZIP or clone it using:
git clone https://github.com/<your-username>/warehouse_optimizer.git
	2.	Navigate to the Project Folder
	•	Open a terminal and move into the directory:
cd warehouse_optimizer
	3.	Create a Virtual Environment
	•	Run the following command to create a virtual environment:
python3 -m venv venv
	4.	Activate the Virtual Environment
	•	On macOS/Linux:
source venv/bin/activate
	•	On Windows:
venv\Scripts\activate
	5.	Install Required Dependencies
	•	Install all project dependencies using pip:
pip install -r requirements.txt
	6.	Prepare the Data
	•	Place all the dataset CSV files into the /data folder.
	•	Make sure the following key file exists:
warehouse_inventory.csv
	7.	Run the Streamlit Application
	•	Start the dashboard with the command:
streamlit run app.py
	8.	Access the Web App
	•	Once Streamlit starts, open the provided local URL in your browser (usually http://localhost:8501).
	9.	Explore the Features
	•	View inventory data, detect anomalies, and generate transfer proposals interactively.


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

Name: Vaibhav Simhaj
Role: AI & Data Engineering Intern
Organization: NexGen Logistics Pvt. Ltd.
Project: Warehouse Optimization & AI Insights System
