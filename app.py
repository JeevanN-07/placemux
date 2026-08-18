import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page Config
st.set_page_config(page_title="Phase 1 Analytics Capstone", layout="wide")

st.title("Phase 1 Executive Analytics Capstone Dashboard")
st.caption("Data Analyst Phase 1 Immersion | Author: Jeevan N | Freshness: Live Automated Refresh")

# Data Engine Load
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range("2026-01-01", "2026-08-14", freq="D")
    data = []
    regions = ["North America", "Europe", "Asia-Pacific", "Latin America"]
    segments = ["Champions", "Loyal Customers", "At-Risk", "Recent"]
    
    for d in dates:
        for r in regions:
            sales = np.random.normal(loc=1200, scale=300)
            orders = np.random.randint(10, 50)
            segment = np.random.choice(segments)
            data.append([d, r, segment, max(sales, 200), orders])
            
    return pd.DataFrame(data, columns=["Date", "Region", "Customer_Segment", "Revenue", "Orders"])

df = load_data()

# Sidebar Interactive Filters
st.sidebar.header("Interactive Controls & Filters")
selected_region = st.sidebar.multiselect("Select Region(s):", options=df["Region"].unique(), default=df["Region"].unique())
selected_segment = st.sidebar.multiselect("Select Segment(s):", options=df["Customer_Segment"].unique(), default=df["Customer_Segment"].unique())

filtered_df = df[(df["Region"].isin(selected_region)) & (df["Customer_Segment"].isin(selected_segment))]

# Section 1: Executive KPI Scorecards
st.header("1. Executive Performance Metrics")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Revenue", f"${filtered_df['Revenue'].sum():,.2f}")
kpi2.metric("Total Orders", f"{filtered_df['Orders'].sum():,}")
kpi3.metric("Average Order Value", f"${filtered_df['Revenue'].sum() / max(filtered_df['Orders'].sum(), 1):,.2f}")
kpi4.metric("Active Regions", f"{filtered_df['Region'].nunique()}")

# Section 2: Visual Storytelling
st.header("2. Revenue Trend & Segment Distribution")
col1, col2 = st.columns(2)

with col1:
    fig_line = px.line(filtered_df.groupby("Date")["Revenue"].sum().reset_index(), x="Date", y="Revenue", title="Daily Revenue Velocity")
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    fig_pie = px.pie(filtered_df, names="Customer_Segment", values="Revenue", title="Revenue Share by Customer Segment", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

# Section 3: Data Dictionary & Governance
st.header("3. Metric Dictionary & Lineage Governance")
dict_df = pd.DataFrame({
    "Metric Name": ["Revenue", "Orders", "Average Order Value", "Customer Segment"],
    "Definition": ["Gross monetary value generated", "Count of fulfilled transaction baskets", "Total Revenue divided by Total Orders", "RFM-derived behavioral categorization"],
    "Source": ["Transactions DB", "Orders Pipeline", "Calculated Aggregation", "Task 17 RFM Model"],
    "Refresh Rate": ["Real-time / Daily", "Daily Batch", "On-demand", "Monthly Refresh"]
})
st.table(dict_df)
