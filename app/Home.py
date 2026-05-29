import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title="NZ Labour Demand Forecaster",
    page_icon="📊",
    layout="wide"
)

st.title("NZ Labour Demand Forecaster")
st.write(
    """
This dashboard presents an interactive view of short-term labour demand trends in New Zealand using Jobs Online data and official labour market data from Stats NZ. 
It summarises overall labour demand patterns, subgroup differences, short-term forecast results, and supporting official labour market context.
"""
)

# ============================================================
# File paths
# ============================================================
JOBS_PATH = os.path.join("data", "integrated", "jobs_online_monthly.csv")
TOTALS_FORECAST_PATH = os.path.join("data", "forecast", "totals_forecast_results.csv")
INDUSTRY_FORECAST_PATH = os.path.join("data", "forecast", "industries_forecast_results.csv")
REGION_FORECAST_PATH = os.path.join("data", "forecast", "regional_forecast_results.csv")

# ============================================================
# Load data
# ============================================================
@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

try:
    df_jobs = load_csv(JOBS_PATH)
    df_totals_fc = load_csv(TOTALS_FORECAST_PATH)
    df_ind_fc = load_csv(INDUSTRY_FORECAST_PATH)
    df_reg_fc = load_csv(REGION_FORECAST_PATH)
except Exception as e:
    st.error(f"Error loading dashboard data: {e}")
    st.stop()

# ============================================================
# Prepare jobs data
# ============================================================
if "date" not in df_jobs.columns or "totals" not in df_jobs.columns:
    st.error("jobs_online_monthly.csv must contain 'date' and 'totals' columns.")
    st.write("Available columns:", list(df_jobs.columns))
    st.stop()

df_jobs["date"] = pd.to_datetime(df_jobs["date"], errors="coerce")
df_jobs = df_jobs.sort_values("date").dropna(subset=["date", "totals"]).reset_index(drop=True)

latest_jobs_value = df_jobs["totals"].iloc[-1]
latest_jobs_date = df_jobs["date"].iloc[-1]
peak_jobs_value = df_jobs["totals"].max()
peak_jobs_date = df_jobs.loc[df_jobs["totals"].idxmax(), "date"]
trough_jobs_value = df_jobs["totals"].min()
trough_jobs_date = df_jobs.loc[df_jobs["totals"].idxmin(), "date"]

# ============================================================
# Prepare national forecast data
# ============================================================
if "date" not in df_totals_fc.columns or "forecast" not in df_totals_fc.columns:
    st.error("totals_forecast_results.csv must contain 'date' and 'forecast' columns.")
    st.write("Available columns:", list(df_totals_fc.columns))
    st.stop()

df_totals_fc["date"] = pd.to_datetime(df_totals_fc["date"], errors="coerce")
df_totals_fc = df_totals_fc.sort_values("date").dropna(subset=["date", "forecast"]).reset_index(drop=True)

latest_fc_value = df_totals_fc["forecast"].iloc[-1]
latest_fc_date = df_totals_fc["date"].iloc[-1]

# ============================================================
# Helper: last forecast change
# ============================================================
if len(df_totals_fc) >= 2:
    prev_fc_value = df_totals_fc["forecast"].iloc[-2]
    fc_change = latest_fc_value - prev_fc_value
else:
    fc_change = 0.0

# ============================================================
# Summary metrics
# ============================================================
st.header("National Labour Demand Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Latest vacancy index",
        f"{latest_jobs_value:.1f}",
        f"{latest_jobs_date.strftime('%b %Y')}"
    )

with col2:
    st.metric(
        "Peak vacancy index",
        f"{peak_jobs_value:.1f}",
        f"{peak_jobs_date.strftime('%b %Y')}"
    )

with col3:
    st.metric(
        "Lowest vacancy index",
        f"{trough_jobs_value:.1f}",
        f"{trough_jobs_date.strftime('%b %Y')}"
    )

with col4:
    st.metric(
        "Latest national forecast",
        f"{latest_fc_value:.2f}",
        f"{fc_change:+.2f}"
    )

# ============================================================
# National trend chart
# ============================================================
st.header("Overall NZ Vacancy Trend")

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(df_jobs["date"], df_jobs["totals"], label="Jobs Online Totals")
ax1.set_title("Overall NZ Vacancy Trend")
ax1.set_xlabel("Date")
ax1.set_ylabel("Vacancy Index")
ax1.grid(True, alpha=0.3)
ax1.legend()

st.pyplot(fig1)

st.write(
    f"""
The latest Jobs Online vacancy index is **{latest_jobs_value:.1f}** in **{latest_jobs_date.strftime('%b %Y')}**. 
The historical peak in this series is **{peak_jobs_value:.1f}** in **{peak_jobs_date.strftime('%b %Y')}**, while the lowest observed point is **{trough_jobs_value:.1f}** in **{trough_jobs_date.strftime('%b %Y')}**. 
This confirms that labour demand in New Zealand has moved through clear periods of contraction and recovery over time.
"""
)

# ============================================================
# National forecast preview
# ============================================================
st.header("National Forecast Preview")

df_fc_plot = df_totals_fc.tail(6).copy()

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(df_fc_plot["date"], df_fc_plot["forecast"], marker="o", label="Forecast")

if "lower_bound" in df_fc_plot.columns and "upper_bound" in df_fc_plot.columns:
    ax2.fill_between(
        df_fc_plot["date"],
        df_fc_plot["lower_bound"],
        df_fc_plot["upper_bound"],
        alpha=0.2,
        label="Forecast interval"
    )

ax2.set_title("National Forecast (Latest Periods)")
ax2.set_xlabel("Date")
ax2.set_ylabel("Forecast Index")
ax2.grid(True, alpha=0.3)
ax2.legend()

st.pyplot(fig2)

st.write(
    f"""
The most recent national forecast value is **{latest_fc_value:.2f}** for **{latest_fc_date.strftime('%b %Y')}**. 
This forecast is intended to support short-term interpretation of labour demand rather than long-run prediction.
"""
)

# ============================================================
# Top rising industries
# ============================================================
st.header("Top Industry Forecast Snapshot")

industry_map = {
    "IT": "it_forecast",
    "Health Care": "health_care_forecast",
    "Construction": "construction_forecast",
    "Education": "education_forecast",
    "Hospitality": "hospitality_forecast",
    "Sales": "sales_forecast"
}

industry_latest = {}
for label, col in industry_map.items():
    if col in df_ind_fc.columns:
        series = df_ind_fc[col].dropna()
        if not series.empty:
            industry_latest[label] = series.iloc[-1]

if industry_latest:
    industry_df = pd.DataFrame({
        "Industry": list(industry_latest.keys()),
        "Latest Forecast": list(industry_latest.values())
    }).sort_values("Latest Forecast", ascending=False)

    st.dataframe(industry_df.reset_index(drop=True), use_container_width=True)

    top_industry = industry_df.iloc[0]
    st.write(
        f"""
Based on the latest forecast values, **{top_industry['Industry']}** currently shows the strongest projected labour-demand level 
among the selected industries, with a forecast value of **{top_industry['Latest Forecast']:.2f}**.
"""
    )
else:
    st.info("Industry forecast columns were not found.")

# ============================================================
# Top regional forecast snapshot
# ============================================================
st.header("Top Regional Forecast Snapshot")

region_map = {
    "Auckland": "auckland_forecast",
    "Wellington": "wellington_forecast",
    "Canterbury": "canterbury_forecast"
}

region_latest = {}
for label, col in region_map.items():
    if col in df_reg_fc.columns:
        series = df_reg_fc[col].dropna()
        if not series.empty:
            region_latest[label] = series.iloc[-1]

if region_latest:
    region_df = pd.DataFrame({
        "Region": list(region_latest.keys()),
        "Latest Forecast": list(region_latest.values())
    }).sort_values("Latest Forecast", ascending=False)

    st.dataframe(region_df.reset_index(drop=True), use_container_width=True)

    top_region = region_df.iloc[0]
    st.write(
        f"""
Among the selected regional forecasts, **{top_region['Region']}** currently records the highest projected labour-demand level, 
with a forecast value of **{top_region['Latest Forecast']:.2f}**.
"""
    )
else:
    st.info("Regional forecast columns were not found.")

# ============================================================
# Navigation guide
# ============================================================
st.header("How to Use This Dashboard")

st.write(
    """
Use the navigation menu on the left to move through the main parts of the project:

- **Project Overview** explains the project background, research questions, data sources, and workflow  
- **NZ Labour Demand Trends** shows the overall trend in labour demand over time  
- **Region Comparison** compares labour-demand patterns across regions  
- **Industry Occupation Comparison** explores subgroup differences  
- **Forecast Explorer** presents short-term forecasting results in a more interactive form  
- **Official Labour Context** provides supporting interpretation using Stats NZ data  
- **Custom Explorer** allows users to explore selected labour-demand series by group and time range  
"""
)