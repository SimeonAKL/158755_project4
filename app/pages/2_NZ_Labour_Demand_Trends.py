import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="NZ Labour Demand Trends", layout="wide")

st.title("NZ Labour Demand Trends")

st.write(
    """
This page presents the overall pattern of online labour demand in New Zealand using the monthly Jobs Online series.
It focuses on the long-run vacancy trend, recent changes over time, and the contrast between skilled and unskilled labour demand.
"""
)

# ============================================================
# Load data
# ============================================================
DATA_PATH = os.path.join("data", "integrated", "jobs_online_monthly.csv")

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

try:
    df = load_data(DATA_PATH)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ============================================================
# Basic preparation
# ============================================================
date_col = "date"
total_col = "totals"
skilled_col = "skilledindex"
unskilled_col = "unskilledindex"

required_cols = [date_col, total_col, skilled_col, unskilled_col]

missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    st.error(f"Missing required columns: {missing_cols}")
    st.write("Available columns:", list(df.columns))
    st.stop()

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df = df.sort_values(date_col).reset_index(drop=True)

# ============================================================
# Data overview
# ============================================================
st.header("Data Overview")
st.write(f"Dataset path: {DATA_PATH}")
st.write(f"Shape: {df.shape}")
st.dataframe(df.head())

# ============================================================
# Summary indicators
# ============================================================
st.header("Summary Indicators")

latest_value = df[total_col].dropna().iloc[-1]
peak_value = df[total_col].max()
trough_value = df[total_col].min()

peak_date = df.loc[df[total_col].idxmax(), date_col]
trough_date = df.loc[df[total_col].idxmin(), date_col]
latest_date = df[date_col].dropna().iloc[-1]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Latest vacancy index", f"{latest_value:.1f}")

with col2:
    st.metric("Peak vacancy index", f"{peak_value:.1f}")

with col3:
    st.metric("Lowest vacancy index", f"{trough_value:.1f}")

st.write(f"Latest observation: {latest_date.strftime('%b %Y')}")
st.write(f"Peak observation: {peak_date.strftime('%b %Y')}")
st.write(f"Lowest observation: {trough_date.strftime('%b %Y')}")

# ============================================================
# Overall NZ Vacancy Trend
# ============================================================
st.header("Overall NZ Vacancy Trend (2007–2026)")

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(df[date_col], df[total_col])
ax1.set_title("Overall NZ Vacancy Trend")
ax1.set_xlabel("Date")
ax1.set_ylabel("Vacancy Index")
ax1.grid(True, alpha=0.3)
st.pyplot(fig1)

st.write(
    """
The overall Jobs Online series shows that labour demand in New Zealand has not been stable over time.
Instead, the series moves through periods of contraction and recovery, suggesting that vacancy activity responds
to broader economic and labour market conditions. This pattern is important because it confirms that the series
contains meaningful short-term variation and is therefore relevant for later forecasting.
"""
)

# ============================================================
# Annual Change in Labour Demand
# ============================================================
st.header("Annual Change in Labour Demand")

df["year"] = df[date_col].dt.year
annual_avg = df.groupby("year")[total_col].mean().reset_index()
annual_avg["annual_change_pct"] = annual_avg[total_col].pct_change() * 100

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.bar(annual_avg["year"].astype(str), annual_avg["annual_change_pct"])
ax2.set_title("Annual Percentage Change in Vacancy Index")
ax2.set_xlabel("Year")
ax2.set_ylabel("Percentage Change (%)")
ax2.grid(True, axis="y", alpha=0.3)
st.pyplot(fig2)

st.write(
    """
The annual change chart highlights that labour demand growth has not followed a uniform path. Some years show strong
recovery, while others show clear contraction. This reinforces the view that labour demand is sensitive to changing
economic conditions and should be interpreted as a dynamic rather than stable series.
"""
)

# ============================================================
# Skilled vs Unskilled Labour Demand
# ============================================================
st.header("Skilled vs Unskilled Labour Demand")

fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.plot(df[date_col], df[skilled_col], label="Skilled")
ax3.plot(df[date_col], df[unskilled_col], label="Unskilled")
ax3.set_title("Skilled vs Unskilled Labour Demand")
ax3.set_xlabel("Date")
ax3.set_ylabel("Vacancy Index")
ax3.legend()
ax3.grid(True, alpha=0.3)
st.pyplot(fig3)

st.write(
    """
The comparison between skill groups suggests that labour demand may not affect all parts of the workforce in the same way.
Differences between skilled and unskilled vacancy trends may reflect variation in job structure, hiring difficulty, or employer
demand across different segments of the labour market. This is relevant for forecasting because it indicates that labour demand
is not evenly distributed across workforce categories.
"""
)

# ============================================================
# Key Takeaways
# ============================================================
st.header("Key Takeaways")

st.markdown(
    f"""
- The latest national vacancy index is **{latest_value:.1f}**.
- The highest observed vacancy index is **{peak_value:.1f}**, recorded in **{peak_date.strftime('%b %Y')}**.
- The lowest observed vacancy index is **{trough_value:.1f}**, recorded in **{trough_date.strftime('%b %Y')}**.
- The national series shows clear periods of decline and recovery, which supports its use in short-term forecasting.
"""
)