# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="RFM Customer Segmentation", layout="wide")
st.title("E-commerce Customer Segmentation (RFM Analysis)")

@st.cache_data
def load_rfm(path="RFM_Segments.csv"):
    df = pd.read_csv(path)
    return df

# Sidebar filters
st.sidebar.header("Filters")
path = st.sidebar.text_input("RFM CSV path", value="RFM_Segments.csv")
min_monetary = st.sidebar.number_input("Min Monetary", value=0.0)

# Load data
try:
    rfm = load_rfm(path)
except FileNotFoundError:
    st.error(f"File not found: {path}. Run rfm_analysis.py first or adjust path.")
    st.stop()

# Segment list for multiselect
all_segments = sorted(rfm["Segment"].unique())
segment_select = st.sidebar.multiselect("Segments", options=all_segments, default=all_segments)

# apply filters
df = rfm[rfm["Monetary"] >= min_monetary]
df = df[df["Segment"].isin(segment_select)]

# Top KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Customers", len(df))
col2.metric("Avg Monetary", f"{df['Monetary'].mean():.2f}")
col3.metric("Avg Frequency", f"{df['Frequency'].mean():.2f}")
col4.metric("Avg Recency (days)", f"{df['Recency'].mean():.1f}")

st.markdown("---")

# Segment distribution bar chart
st.subheader("Customer Segments")
seg_counts = df["Segment"].value_counts().reset_index()
seg_counts.columns = ["Segment", "Count"]
fig_seg = px.bar(seg_counts, x="Segment", y="Count", text="Count")
fig_seg.update_layout(xaxis_title="", yaxis_title="Customers", height=400)
st.plotly_chart(fig_seg, width="stretch")

# RFM scatter
st.subheader("RFM scatter: Monetary vs Frequency")
fig = px.scatter(df,
                 x="Frequency",
                 y="Monetary",
                 size="Recency",
                 color="Segment",
                 hover_data=["CustomerID", "RFM_Score", "R_Score", "F_Score", "M_Score"])
fig.update_layout(height=500)
st.plotly_chart(fig, width="stretch")

# Heatmap
st.subheader("RFM Score distribution (R_Score x F_Score)")
heat = df.groupby(["R_Score", "F_Score"]).size().reset_index(name="Count")
heat_pivot = heat.pivot(index="R_Score", columns="F_Score", values="Count").fillna(0)

st.dataframe(
    heat_pivot.style.background_gradient(cmap="Blues"),
    width="stretch"
)

st.markdown("---")
st.subheader("Customer Table (drill-down)")
st.write("Filter, sort, and download the table below.")
st.dataframe(df.sort_values("Monetary", ascending=False).reset_index(drop=True), width="stretch")

# CSV download
def to_excel(df_in):
    output = BytesIO()
    df_in.to_excel(output, index=False, engine="openpyxl")
    return output.getvalue()

st.download_button(
    label="Download selected customers as Excel",
    data=to_excel(df),
    file_name="rfm_customers.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
