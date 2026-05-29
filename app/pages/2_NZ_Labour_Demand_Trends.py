import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="NZ Labour Demand Trends", layout="wide")

st.title("NZ Labour Demand Trends")

st.write(
    """
This page presents the overall pattern of online labour demand in New Zealand using the monthly Jobs Online series.
It focuses on the long-run hiring-demand trend, recent changes over time, and the contrast between skilled and unskilled demand.
"""
)

DATA_PATH = os.path.join("data", "integrated", "jobs_online_monthly.csv")

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

try:
    df = load_data(DATA_PATH)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

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
df = df.dropna(subset=[date_col]).sort_values(date_col).reset_index(drop=True)

st.header("Controls")

min_date = df[date_col].min().date()
max_date = df[date_col].max().date()

date_range = st.slider(
    "Select date range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

skill_view = st.radio(
    "Skilled vs Unskilled view",
    ["Both", "Skilled only", "Unskilled only"],
    horizontal=True
)

start_date, end_date = date_range

df_filtered = df[
    (df[date_col].dt.date >= start_date) &
    (df[date_col].dt.date <= end_date)
].copy()

if df_filtered.empty:
    st.warning("No data available for the selected date range.")
    st.stop()

st.header("Market Overview")
st.write(f"Selected period: **{start_date.strftime('%d %b %Y')}** to **{end_date.strftime('%d %b %Y')}**")

with st.expander("Show raw data preview"):
    st.dataframe(df_filtered.head(), use_container_width=True)

st.header("Summary Indicators")

latest_value = df_filtered[total_col].dropna().iloc[-1]
peak_value = df_filtered[total_col].max()
trough_value = df_filtered[total_col].min()

peak_date = df_filtered.loc[df_filtered[total_col].idxmax(), date_col]
trough_date = df_filtered.loc[df_filtered[total_col].idxmin(), date_col]
latest_date = df_filtered[date_col].dropna().iloc[-1]

if len(df_filtered[total_col].dropna()) >= 2:
    previous_value = df_filtered[total_col].dropna().iloc[-2]
    latest_delta = latest_value - previous_value
else:
    latest_delta = 0.0

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Latest hiring demand", f"{latest_value:.1f}", f"{latest_delta:+.1f}")
with col2:
    st.metric("Peak hiring demand", f"{peak_value:.1f}")
with col3:
    st.metric("Lowest hiring demand", f"{trough_value:.1f}")

st.write(f"Latest observation: {latest_date.strftime('%b %Y')}")
st.write(f"Peak observation: {peak_date.strftime('%b %Y')}")
st.write(f"Lowest observation: {trough_date.strftime('%b %Y')}")

st.header("Overall NZ Hiring Demand Trend")
fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(df_filtered[date_col], df_filtered[total_col], label="Total hiring demand")
ax1.set_title("Overall NZ Hiring Demand Trend")
ax1.set_xlabel("Date")
ax1.set_ylabel("Hiring demand")
ax1.grid(True, alpha=0.3)
ax1.legend()
st.pyplot(fig1)

st.write(
    """
The overall Jobs Online series shows that labour demand in New Zealand has not been stable over time.
Instead, the series moves through periods of contraction and recovery, suggesting that hiring activity responds
to broader economic and labour market conditions.
"""
)

st.header("Annual Change in Hiring Demand")
annual_df = df_filtered.copy()
annual_df["year"] = annual_df[date_col].dt.year
annual_avg = annual_df.groupby("year")[total_col].mean().reset_index()
annual_avg["annual_change_pct"] = annual_avg[total_col].pct_change() * 100

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.bar(annual_avg["year"].astype(str), annual_avg["annual_change_pct"])
ax2.axhline(0, linestyle="--")
ax2.set_title("Annual Percentage Change in Hiring Demand")
ax2.set_xlabel("Year")
ax2.set_ylabel("Percentage change (%)")
ax2.grid(True, axis="y", alpha=0.3)
st.pyplot(fig2)

st.write(
    """
The annual change chart highlights that labour demand growth has not followed a uniform path.
Some years show strong recovery, while others show clear contraction.
"""
)

st.header("Skilled vs Unskilled Hiring Demand")
fig3, ax3 = plt.subplots(figsize=(10, 5))

if skill_view in ["Both", "Skilled only"]:
    ax3.plot(df_filtered[date_col], df_filtered[skilled_col], label="Skilled")

if skill_view in ["Both", "Unskilled only"]:
    ax3.plot(df_filtered[date_col], df_filtered[unskilled_col], label="Unskilled")

ax3.set_title("Skilled vs Unskilled Hiring Demand")
ax3.set_xlabel("Date")
ax3.set_ylabel("Hiring demand")
ax3.legend()
ax3.grid(True, alpha=0.3)
st.pyplot(fig3)

st.write(
    """
The comparison between skill groups suggests that labour demand may not affect all parts of the workforce in the same way.
Differences between skilled and unskilled demand may reflect variation across different segments of the labour market.
"""
)

st.header("Key Takeaways")
long_run_avg = df_filtered[total_col].mean()

st.markdown(
    f"""
- The latest national hiring-demand reading in the selected period is **{latest_value:.1f}**.
- The highest observed reading is **{peak_value:.1f}**, recorded in **{peak_date.strftime('%b %Y')}**.
- The lowest observed reading is **{trough_value:.1f}**, recorded in **{trough_date.strftime('%b %Y')}**.
- The latest value is **{'above' if latest_value > long_run_avg else 'below'}** the average level for the selected period.
"""
)

st.subheader("Key takeaway")
st.write(
    "NZ hiring demand has moved through clear cycles of decline and recovery, which makes short-term monitoring important for workforce planning and market timing."
)

st.header("Download Data")
download_df = df_filtered[[date_col, total_col, skilled_col, unskilled_col]].copy()
csv_data = download_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download filtered national trend data as CSV",
    data=csv_data,
    file_name="nz_labour_demand_trends_filtered.csv",
    mime="text/csv"
)
