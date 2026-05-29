import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Official Labour Context", layout="wide")

st.title("Official Labour Context")

st.write(
    """
This page provides official labour market context for interpreting the Jobs Online vacancy trend.
It combines Jobs Online with selected Stats NZ labour market indicators to support a broader understanding
of labour demand conditions in New Zealand.
"""
)

# ============================================================
# File paths
# ============================================================
MONTHLY_PATH = os.path.join("data", "integrated", "monthly_labour_market_master.csv")
QUARTERLY_PATH = os.path.join("data", "integrated", "quarterly_labour_force_master.csv")
JOBS_PATH = os.path.join("data", "integrated", "jobs_online_monthly.csv")

# ============================================================
# Load data
# ============================================================
@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

try:
    df_monthly = load_csv(MONTHLY_PATH)
    df_quarterly = load_csv(QUARTERLY_PATH)
    df_jobs = load_csv(JOBS_PATH)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ============================================================
# Helper functions
# ============================================================
def find_first_match(columns, candidates):
    for c in candidates:
        if c in columns:
            return c
    return None

def get_numeric_columns(df):
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

# ============================================================
# Date preparation
# ============================================================
jobs_date_col = find_first_match(df_jobs.columns, ["date", "month", "Date"])
monthly_date_col = find_first_match(df_monthly.columns, ["date", "month", "Date"])
quarterly_date_col = find_first_match(df_quarterly.columns, ["date", "quarter", "Date"])

if jobs_date_col is None:
    st.error("Could not find a date column in jobs_online_monthly.csv")
    st.write("Available columns:", list(df_jobs.columns))
    st.stop()

if monthly_date_col is None:
    st.warning("Could not find a date column in monthly_labour_market_master.csv")
if quarterly_date_col is None:
    st.warning("Could not find a date column in quarterly_labour_force_master.csv")

df_jobs[jobs_date_col] = pd.to_datetime(df_jobs[jobs_date_col], errors="coerce")

if monthly_date_col:
    df_monthly[monthly_date_col] = pd.to_datetime(df_monthly[monthly_date_col], errors="coerce")

if quarterly_date_col:
    df_quarterly[quarterly_date_col] = pd.to_datetime(df_quarterly[quarterly_date_col], errors="coerce")

# ============================================================
# Jobs Online total column
# ============================================================
jobs_total_col = "totals" if "totals" in df_jobs.columns else None
if jobs_total_col is None:
    st.error("Could not find 'totals' column in jobs_online_monthly.csv")
    st.write("Available columns:", list(df_jobs.columns))
    st.stop()

# ============================================================
# Overview
# ============================================================
st.header("Data Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("Jobs Online shape:", df_jobs.shape)

with col2:
    st.write("Monthly official data shape:", df_monthly.shape)

with col3:
    st.write("Quarterly official data shape:", df_quarterly.shape)

# ============================================================
# Source selector
# ============================================================
st.header("Indicator Selection")

source_type = st.selectbox(
    "Select official data source",
    ["Monthly Official Indicators", "Quarterly Official Indicators"]
)

if source_type == "Monthly Official Indicators":
    df_context = df_monthly.copy()
    context_date_col = monthly_date_col
else:
    df_context = df_quarterly.copy()
    context_date_col = quarterly_date_col

if context_date_col is None:
    st.error("The selected dataset does not contain a valid date column.")
    st.stop()

numeric_cols = get_numeric_columns(df_context)

if not numeric_cols:
    st.error("No numeric indicator columns found in the selected dataset.")
    st.write("Available columns:", list(df_context.columns))
    st.stop()

selected_indicator = st.selectbox(
    "Select official labour market indicator",
    numeric_cols
)

# ============================================================
# Official indicator chart
# ============================================================
st.header("Official Labour Market Indicator")

df_indicator = df_context[[context_date_col, selected_indicator]].dropna().sort_values(context_date_col)

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(df_indicator[context_date_col], df_indicator[selected_indicator], marker="o")
ax1.set_title(f"{selected_indicator} over Time")
ax1.set_xlabel("Date")
ax1.set_ylabel(selected_indicator)
ax1.grid(True, alpha=0.3)

st.pyplot(fig1)

latest_value = df_indicator[selected_indicator].iloc[-1]
latest_date = df_indicator[context_date_col].iloc[-1]

st.write(
    f"""
The selected official indicator is **{selected_indicator}**. The latest available value in this series is
**{latest_value:.2f}** for **{latest_date.strftime('%b %Y')}**.
This indicator provides official labour market context that can be used to support interpretation of vacancy trends.
"""
)

# ============================================================
# Comparison with Jobs Online
# ============================================================
st.header("Comparison with Jobs Online")

df_jobs_plot = df_jobs[[jobs_date_col, jobs_total_col]].dropna().sort_values(jobs_date_col)
df_context_plot = df_context[[context_date_col, selected_indicator]].dropna().sort_values(context_date_col)

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(df_jobs_plot[jobs_date_col], df_jobs_plot[jobs_total_col], label="Jobs Online Totals")
ax2.plot(df_context_plot[context_date_col], df_context_plot[selected_indicator], label=selected_indicator)
ax2.set_title("Jobs Online vs Official Labour Market Indicator")
ax2.set_xlabel("Date")
ax2.set_ylabel("Value")
ax2.grid(True, alpha=0.3)
ax2.legend()

st.pyplot(fig2)

st.write(
    """
The official labour market indicators from Stats NZ provide a broader context for interpreting the Jobs Online series.
While vacancy data captures changes in online job advertisement activity, official indicators reflect wider labour market
conditions such as employment levels and labour market pressure. Looking at both together makes it easier to assess
whether vacancy movement is broadly consistent with the wider labour market rather than interpreting Jobs Online in isolation.
"""
)

# ============================================================
# Latest values table
# ============================================================
st.header("Latest Available Values")

latest_jobs_value = df_jobs_plot[jobs_total_col].iloc[-1]
latest_jobs_date = df_jobs_plot[jobs_date_col].iloc[-1]

summary_df = pd.DataFrame({
    "Series": ["Jobs Online Totals", selected_indicator],
    "Latest Value": [latest_jobs_value, latest_value],
    "Latest Date": [latest_jobs_date.strftime("%b %Y"), latest_date.strftime("%b %Y")]
})

st.dataframe(summary_df, use_container_width=True)

# ============================================================
# Optional raw data preview
# ============================================================
with st.expander("Show selected official data preview"):
    st.dataframe(df_indicator.head(), use_container_width=True)