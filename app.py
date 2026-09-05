import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="DA-02: Root-Cause Diagnostic Engine", layout="wide")

st.title("🚨 Application Funnel & Root-Cause Diagnostic Engine")
st.subheader("Identifying Silent Failures vs. User Friction")

# Mock Dataset Generation representing mixed causes
data = {
    'Stage': ['1. Job Description View', '2. Profile & Form Fill', '3. Document Upload', '4. Final Submission'],
    'Users Started': [1000, 750, 680, 200],
    'Users Completed': [750, 680, 200, 180],
    'Primary Root Cause': ['Trust / Scam Perception', 'Form Length Friction', 'Silent Technical Bug (Upload 500)', 'Timezone Deadline Bug']
}
df = pd.DataFrame(data)
df['Drop-off Count'] = df['Users Started'] - df['Users Completed']
df['Drop-off %'] = (df['Drop-off Count'] / df['Users Started']) * 100

# Top Summary Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Applicants Started", "1,000")
col2.metric("Final Applications Completed", "180", "-82% Overall Drop-off")
col3.metric("Critical Bottleneck", "Stage 3 (Upload)", "Silent Tech Failure")

st.markdown("---")

# Main Visuals
c1, c2 = st.columns([1, 1])

with c1:
    st.write("### Application Funnel Conversion")
    fig_funnel = px.funnel(df, x='Users Completed', y='Stage', color='Primary Root Cause')
    st.plotly_chart(fig_funnel, use_container_width=True)

with c2:
    st.write("### Stage Drop-off & Root Cause Breakdown")
    fig_bar = px.bar(df, x='Stage', y='Drop-off %', color='Primary Root Cause', text_auto='.1f')
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# Executive Action Matrix
st.write("### 🛠️ Recommended Sprint Action Matrix")
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.error("**Priority 1: Fix Technical Pipeline**")
    st.caption("Stage 3: Document Upload")
    st.write("• Resolve silently failing 500 API errors on document uploads.\n• **Impact:** Recovers ~480 lost applications instantly.")

with col_b:
    st.warning("**Priority 2: Fix Timezone Display**")
    st.caption("Stage 4: Submission Cutoff")
    st.write("• Align deadline timestamps explicitly to local IST vs. UTC.\n• **Impact:** Prevents early deadline lockout spikes.")

with col_c:
    st.info("**Priority 3: Copywriting / Trust**")
    st.caption("Stage 1: Job Description View")
    st.write("• Verify recruiter authenticity flags and refine JD phrasing.\n• **Impact:** Reduces bounce rate on initial views.")
