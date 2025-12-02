# rfm_analysis.py
import pandas as pd
import numpy as np
from datetime import datetime
import argparse

def load_data(path="ecommerce_data.csv"):
    df = pd.read_csv(path, parse_dates=["InvoiceDate"])
    return df

def clean_data(df):
    # Drop rows with missing CustomerID or InvoiceDate
    df = df.dropna(subset=["CustomerID", "InvoiceDate"]).copy()
    # Ensure numeric columns
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce").fillna(0.0)
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
    # Remove negative/zero totals (if any)
    df = df[df["TotalPrice"] > 0]
    return df

def compute_rfm(df, snapshot_date=None):
    if snapshot_date is None:
        snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    else:
        snapshot_date = pd.to_datetime(snapshot_date)

    rfm = df.groupby("CustomerID").agg({
        "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
        "InvoiceNo": "nunique",
        "TotalPrice": "sum"
    }).reset_index()

    rfm.columns = ["CustomerID", "Recency", "Frequency", "Monetary"]
    return rfm, snapshot_date

def rfm_score(df):
    # We want higher scores for better customers
    df["R_Score"] = pd.qcut(df["Recency"], 5, labels=[5,4,3,2,1]).astype(int)  # lesser recency => higher score
    df["F_Score"] = pd.qcut(df["Frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
    df["M_Score"] = pd.qcut(df["Monetary"], 5, labels=[1,2,3,4,5]).astype(int)
    df["RFM_Score"] = df["R_Score"].astype(str) + df["F_Score"].astype(str) + df["M_Score"].astype(str)
    df["RFM_Sum"] = df[["R_Score","F_Score","M_Score"]].sum(axis=1)
    return df

def assign_segment(df):
    # Simple segment rules based on RFM_Sum or R,S,F,M thresholds
    def segment(row):
        if row["R_Score"] >= 4 and row["F_Score"] >= 4 and row["M_Score"] >= 4:
            return "Champions"
        if row["R_Score"] >= 3 and row["F_Score"] >= 3 and row["M_Score"] >= 3:
            return "Loyal / Valuable"
        if row["R_Score"] >= 4 and (row["F_Score"] >= 2 or row["M_Score"] >=2):
            return "Recent Big Spenders"
        if row["R_Score"] <= 2 and row["F_Score"] >= 4:
            return "Frequent but Not Recent"
        if row["R_Score"] <= 2 and row["F_Score"] <= 2 and row["M_Score"] <= 2:
            return "At Risk / Churn"
        if row["R_Score"] >= 4 and row["F_Score"] <=2:
            return "New / Potential"
        return "Other"

    df["Segment"] = df.apply(segment, axis=1)
    return df

def main(path="ecommerce_data.csv", out="RFM_Segments.csv", snapshot_date=None):
    df = load_data(path)
    df = clean_data(df)
    rfm, snapshot = compute_rfm(df, snapshot_date)
    rfm = rfm_score(rfm)
    rfm = assign_segment(rfm)
    # Add some summary columns
    rfm = rfm.sort_values(["RFM_Sum", "Monetary"], ascending=[False, False])
    rfm.to_csv(out, index=False)
    print(f"RFM saved to {out} (snapshot_date={snapshot.date()})")
    # Print quick summary
    print(rfm.groupby("Segment").size().sort_values(ascending=False).head(10))
    return rfm

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="ecommerce_data.csv")
    parser.add_argument("--output", default="RFM_Segments.csv")
    parser.add_argument("--snapshot", default=None, help="Snapshot date (YYYY-MM-DD) to calculate recency. Default is max(InvoiceDate)+1 day")
    args = parser.parse_args()
    main(path=args.input, out=args.output, snapshot_date=args.snapshot)
