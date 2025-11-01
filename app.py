import streamlit as st
import pandas as pd
import os
from anomaly_detection import detect_anomalies
from optimizer import compute_surplus_deficit, propose_transfers

st.set_page_config(page_title="Warehouse Optimization Tool", layout="wide")
st.title("Warehouse Optimization — Rebalancing & Transfer Suggestions")

# Sidebar input for data folder
st.sidebar.header("Data source")
base = st.sidebar.text_input(
    "Data folder",
    value="/Users/vaibhavsimhaj/Downloads/Case study internship data"
)

# ---- Load inventory ----
@st.cache_data
def load_inventory(base):
    return pd.read_csv(os.path.join(base, "warehouse_inventory.csv"))

inv = load_inventory(base)

st.header("Inventory Preview")
st.write(inv.head(10))

# ---- Surplus / Deficit summary ----
st.header("Surplus / Deficit by Warehouse & Category")
summary = compute_surplus_deficit(inv)
st.dataframe(summary)

# ---- Transfer proposals ----
st.header("Propose Transfers (Heuristic)")
tc = st.number_input(
    "Transfer cost per km per unit (INR)",
    value=0.01,
    step=0.01
)
mf = st.slider(
    "Max fraction of surplus available for transfer",
    min_value=0.0,
    max_value=1.0,
    value=0.5
)

if st.button("Create transfer proposals"):
    proposals = propose_transfers(
        inv,
        transfer_cost_per_km_per_unit=tc,
        max_transfer_fraction=mf
    )
    if proposals.empty:
        st.info("No feasible transfers found (all warehouses at or below reorder levels).")
    else:
        st.write(f"{len(proposals)} proposed transfers")
        st.dataframe(proposals)
        csv = proposals.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download proposals CSV",
            data=csv,
            file_name="transfer_proposals.csv",
            mime="text/csv"
        )

# ---- AI Insights: Anomaly Detection ----
st.header("AI Insights — Inventory Anomaly Detection")
st.write(
    "Detect unusual inventory patterns "
    "(potential miscounts, theft, bad data, or sudden demand shifts)."
)

contam = st.slider(
    "Anomaly rate (fraction of records to flag)",
    min_value=0.01,
    max_value=0.2,
    value=0.05,
    step=0.01
)

if st.button("Run anomaly detection"):
    try:
        full_df, anomalies_df, meta = detect_anomalies(inv, cost_df=None, contamination=contam)
        st.success(f"Anomaly detection complete — flagged {len(anomalies_df)} records.")

        if anomalies_df.empty:
            st.info("No anomalies found with the selected contamination level.")
        else:
            anomalies_df = anomalies_df.loc[:, ~anomalies_df.columns.duplicated()]

            display_cols = [
                c for c in [
                    meta.get('warehouse_col'),
                    meta.get('location_col'),
                    meta.get('product_col'),
                    'Current_Stock_Units',
                    'Reorder_Level',
                    'storage_cost_per_unit',
                    'days_since_restock',
                    'anomaly_magnitude'
                ] if c and c in anomalies_df.columns
            ]

            view_df = (
                anomalies_df
                .drop_duplicates(subset=display_cols, keep="first")
                .sort_values('anomaly_magnitude', ascending=False)
                .head(50)
            )

            st.dataframe(view_df)

            csv = anomalies_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download anomalies CSV",
                data=csv,
                file_name="warehouse_anomalies.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Anomaly detection failed: {e}")