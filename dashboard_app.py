import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Executive Dashboard", layout="wide", initial_sidebar_state="expanded")

# Load Data
@st.cache_data
def load_data():
    df_raw = pd.read_csv('data/realistic_student_data.csv')
    df_raw['score'] = pd.to_numeric(df_raw['score'], errors='coerce')
    df_raw['submission_date'] = pd.to_datetime(df_raw['submission_date'])
    df = df_raw.dropna(subset=['score']).copy()
    df['passed'] = df['score'].apply(lambda x: 'Pass' if x >= 60 else 'Fail')
    df['score_cohort'] = df['score'].apply(lambda x: 'High (>=70)' if x >= 70 else 'Low (<70)')
    return df

df = load_data()

# Header
st.title("📊 Student Performance Executive Dashboard")
st.caption(f"**Data Freshness:** Live Sync as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST | **Evaluated Records:** N={len(df)}")

# Sidebar Filters
st.sidebar.header("Filter & Slice Controls")
date_range = st.sidebar.date_input(
    "Submission Date Range",
    [df['submission_date'].min().date(), df['submission_date'].max().date()]
)

status_filter = st.sidebar.multiselect(
    "Pass/Fail Status",
    options=['Pass', 'Fail'],
    default=['Pass', 'Fail']
)

filtered_df = df[
    (df['submission_date'].dt.date >= date_range[0]) &
    (df['submission_date'].dt.date <= date_range[1]) &
    (df['passed'].isin(status_filter))
]

# Metrics
st.subheader("1. Key Metric Benchmarks")
col1, col2, col3, col4 = st.columns(4)

total_students = len(filtered_df)
avg_score = filtered_df['score'].mean() if total_students > 0 else 0
pass_rate = (filtered_df['passed'] == 'Pass').mean() * 100 if total_students > 0 else 0
high_cohort_pct = (filtered_df['score_cohort'] == 'High (>=70)').mean() * 100 if total_students > 0 else 0

col1.metric("Total Submissions", f"{total_students}", delta=f"N={len(df)} Raw Pool")
col2.metric("Mean Score", f"{avg_score:.1f}", delta=f"{avg_score - 60:.1f} vs Target (60)")
col3.metric("Pass Rate", f"{pass_rate:.1f}%", delta=f"{pass_rate - 75:.1f}% vs Target (75%)")
col4.metric("High Performers (>=70)", f"{high_cohort_pct:.1f}%")

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("2. Score Trend & Moving Average")
    trend_data = filtered_df.groupby('submission_date')['score'].mean().reset_index()
    trend_data['7D_MA'] = trend_data['score'].rolling(7, min_periods=1).mean()
    
    fig_trend = px.line(trend_data, x='submission_date', y=['score', '7D_MA'], 
                        labels={'value': 'Score', 'submission_date': 'Date', 'variable': 'Metric'},
                        color_discrete_map={'score': '#2b5c8f', '7D_MA': '#e74c3c'})
    fig_trend.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=350)
    st.plotly_chart(fig_trend, use_container_width=True)

with col_right:
    st.subheader("3. Cohort Distribution & Composition")
    fig_hist = px.histogram(filtered_df, x='score', color='passed', nbins=20,
                            color_discrete_map={'Pass': '#2ecc71', 'Fail': '#e74c3c'},
                            barmode='overlay')
    fig_hist.add_vline(x=60, line_dash="dash", line_color="black", annotation_text="Passing Cutoff (60)")
    fig_hist.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=350)
    st.plotly_chart(fig_hist, use_container_width=True)