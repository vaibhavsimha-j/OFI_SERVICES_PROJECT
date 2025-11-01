# anomaly_detection.py
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime

# helper to normalize column names (lowercase, remove spaces/extra chars)
def _normalize_cols(df):
    mapping = {}
    cols = list(df.columns)
    for c in cols:
        key = c.strip().lower().replace(" ", "_").replace("-", "_")
        mapping[c] = key
    df = df.rename(columns=mapping)
    return df

def _coerce_dates(df, colname_candidates):
    for c in colname_candidates:
        if c in df.columns:
            try:
                df[c] = pd.to_datetime(df[c], errors='coerce')
            except Exception:
                df[c] = pd.to_datetime(df[c], infer_datetime_format=True, errors='coerce')
            return c
    return None

def build_feature_table(inv_df, cost_df=None, today=None):
    """
    inv_df: warehouse inventory dataframe (raw)
    cost_df: optional cost_breakdown to enrich (not required)
    returns: DataFrame with features for anomaly detection
    """
    df = inv_df.copy()
    df = _normalize_cols(df)

    # common name candidates (tolerant mapping)
    # warehouse id
    wh_keys = ['warehouse_id', 'warehouseid', 'warehouse']
    # location
    loc_keys = ['location', 'loc', 'city']
    # product category
    cat_keys = ['product_category','product_category','productcat','product_cat','productcategory']
    # numeric fields
    cs_keys = ['current_stock_units','current_stock','current_stock_units_']
    ro_keys = ['reorder_level','reorder','re_order_level']
    sc_keys = ['storage_cost_per_unit','storage_cost','storage_cost_per_unit_']
    date_candidates = ['last_restocked_date','last_restocked','last_restocked_datee','last_restocked_date']

    # find actual column names present after normalization
    def find_key(cands):
        for k in cands:
            if k in df.columns:
                return k
        return None

    wh_col = find_key(wh_keys)
    loc_col = find_key(loc_keys)
    cat_col = find_key(cat_keys)
    cs_col = find_key(cs_keys)
    ro_col = find_key(ro_keys)
    sc_col = find_key(sc_keys)
    date_col = _coerce_dates(df, date_candidates)

    # If important numeric columns are missing, try to fallback by guessing
    # Convert numeric columns to numeric
    for col in [cs_col, ro_col, sc_col]:
        if col and col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Feature engineering
    #  - stock_vs_reorder: difference between current and reorder
    df['stock_vs_reorder'] = np.nan
    if cs_col and ro_col:
        df['stock_vs_reorder'] = df[cs_col] - df[ro_col]
    elif cs_col:
        df['stock_vs_reorder'] = df[cs_col]  # best-effort

    #  - storage cost per unit (if available)
    df['storage_cost_per_unit'] = df[sc_col] if sc_col in df.columns else np.nan

    #  - days_since_restock
    if date_col:
        today = pd.to_datetime(today) if today is not None else pd.Timestamp.now()
        df['days_since_restock'] = (today - df[date_col]).dt.days
    else:
        df['days_since_restock'] = np.nan

    #  - relative_stock_ratio = current / (reorder+1)
    if cs_col and ro_col:
        df['relative_stock_ratio'] = df[cs_col] / (df[ro_col].replace({0: np.nan}) + 1)
    else:
        df['relative_stock_ratio'] = np.nan

    # Optionally merge cost_df to enrich features
    if cost_df is not None:
        cdf = cost_df.copy()
        cdf = _normalize_cols(cdf)
        # cost_df often keyed by Order_ID; but if it contains Warehouse references, merge heuristically
        # We'll try to merge on warehouse id if present in both
        c_wh_col = find_key(wh_keys)
        if c_wh_col and wh_col and c_wh_col in cdf.columns and wh_col in df.columns:
            merged = df.merge(cdf, left_on=wh_col, right_on=c_wh_col, how='left', suffixes=("","_cost"))
            df = merged

    # Select columns to be used as features (numeric)
    feature_cols = ['stock_vs_reorder', 'storage_cost_per_unit', 'days_since_restock', 'relative_stock_ratio']
    available_features = [c for c in feature_cols if c in df.columns]
    features = df[available_features].fillna(0.0)  # fillna for model stability

    return df, features, {
        'warehouse_col': wh_col,
        'location_col': loc_col,
        'product_col': cat_col,
        'metric_cols': available_features
    }

def run_isolation_forest(features_df, random_state=42, contamination=0.05):
    """
    features_df: numeric DataFrame
    contamination: fraction of expected outliers (tuneable)
    returns: array of anomaly scores and boolean mask (True = anomaly)
    """
    model = IsolationForest(n_estimators=200, contamination=contamination, random_state=random_state)
    model.fit(features_df)
    # anomaly score: lower => more anomalous in sklearn's decision_function sense, but we return a signed score
    scores = model.decision_function(features_df)  # higher = more normal, lower = anomalous
    preds = model.predict(features_df)  # -1 => anomaly, 1 => normal
    is_anom = (preds == -1)
    return scores, is_anom, model

def detect_anomalies(inv_df, cost_df=None, contamination=0.05, today=None):
    """
    Full pipeline: returns dataframe with anomaly scores and flags.
    """
    df, features, meta = build_feature_table(inv_df, cost_df, today=today)
    if features.shape[1] == 0:
        raise ValueError("No numeric features available for anomaly detection. Check your CSV columns.")
    scores, is_anom, model = run_isolation_forest(features, contamination=contamination)
    df = df.copy().reset_index(drop=True)
    df['_anomaly_score'] = scores
    df['_is_anomaly'] = is_anom
    # smaller decision_function -> more anomalous, so invert for a clear "anomaly_magnitude"
    df['anomaly_magnitude'] = -1.0 * df['_anomaly_score']
    # sort anomalies by magnitude
    anomalies = df[df['_is_anomaly']].sort_values('anomaly_magnitude', ascending=False)
    return df, anomalies, meta