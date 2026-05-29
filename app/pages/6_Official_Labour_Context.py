import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Official Labour Context", layout="wide")

st.title("Official Labour Context")

st.write(
    """
This page places hiring demand in a broader labour market context using official indicators from Stats NZ.
It helps users judge whether vacancy movement is supported by wider employment and labour market conditions.
"""
)

MONTHLY_PATH = os.path.join("data", "integrated", "monthly_labour_market_master.csv")
QUARTERLY_PATH = os.path.join("data", "integrated", "quarterly_labour_force_master.csv")
JOBS_PATH = os.path.join("data", "integrated", "jobs_online_monthly.csv")

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

def find_first_match(columns, candidates):
    for c in candidates:
        if c in columns:
            return c
    return None

def get_numeric_columns(df):
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

jobs_date_col = find_first_match(df_jobs.columns, ["date", "month", "Date"])
monthly_date_col = find_first_match(df_monthly.columns, ["date", "month", "Date"])
quarterly_date_col = find_first_match(df_quarterly.columns, ["date", "quarter", "Date"])

df_jobs[jobs_date_col] = pd.to_datetime(df_jobs[jobs_date_col], errors="coerce")
df_monthly[monthly_date_col] = pd.to_datetime(df_monthly[monthly_date_col], errors="coerce")
df_quarterly[quarterly_date_col] = pd.to_datetime(df_quarterly[quarterly_date_col], errors="coerce")

jobs_total_col = "totals"

indicator_labels = {
    "male_paid_employee": "Male employment",
    "female_paid_employee": "Female employment",
    "unemployment_rate": "Unemployment rate",
    "underutilisation_rate": "Underutilisation rate",
    "filled_jobs": "Filled jobs",
    "employment_total": "Total employment"
}

st.header("Indicator Selection")

source_type = st.selectbox("Select official data source", ["Monthly Official Indicators", "Quarterly Official Indicators"])

if source_type == "Monthly Official Indicators":
    df_context = df_monthly.copy()
    context_date_col = monthly_date_col
else:
    df_context = df_quarterly.copy()
    context_date_col = quarterly_date_col

numeric_cols = get_numeric_columns(df_context)

preferred_indicators = [
    "Unemployment rate",
    "Underutilisation rate",
    "Male employment",
    "Female employment",
    "Filled jobs"
]

display_to_actual = {}
for col in numeric_cols:
    display_name = indicator_labels.get(col, col.replace("_", " ").title())
    display_to_actual[display_name] = col

preferred_available = [name for name in preferred_indicators if name in display_to_actual]
other_available = [name for name in display_to_actual.keys() if name not in preferred_available]

selected_display = st.selectbox(
    "Select official labour market indicator",
    preferred_available if preferred_available else list(display_to_actual.keys())
)

with st.expander("Show more indicator options"):
    if other_available:
        extra_display = st.selectbox(
            "Other available indicators",
            ["None"] + other_available,
            key="extra_indicator_select"
        )
        if extra_display != "None":
            selected_display = extra_display
    else:
        st.write("No additional indicators available.")

st.caption(f"Currently viewing: **{selected_display}**")

selected_indicator = display_to_actual[selected_display]

st.header("Official Labour Market Indicator")
df_indicator = df_context[[context_date_col, selected_indicator]].dropna().sort_values(context_date_col)

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(df_indicator[context_date_col], df_indicator[selected_indicator], marker="o")
ax1.set_title(f"{selected_display} over Time")
ax1.set_xlabel("Date")
ax1.set_ylabel(selected_display)
ax1.grid(True, alpha=0.3)
st.pyplot(fig1)

latest_value = df_indicator[selected_indicator].iloc[-1]
latest_date = df_indicator[context_date_col].iloc[-1]

st.write(
    f"""
The selected official indicator is **{selected_display}**. The latest available value in this series is
**{latest_value:.2f}** for **{latest_date.strftime('%b %Y')}**.
"""
)

st.header("Comparison with Jobs Online")
df_jobs_plot = df_jobs[[jobs_date_col, jobs_total_col]].dropna().sort_values(jobs_date_col)
df_context_plot = df_context[[context_date_col, selected_indicator]].dropna().sort_values(context_date_col)

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(df_jobs_plot[jobs_date_col], df_jobs_plot[jobs_total_col], label="Jobs Online hiring demand")
ax2.plot(df_context_plot[context_date_col], df_context_plot[selected_indicator], label=selected_display)
ax2.set_title("Hiring Demand vs Official Labour Market Indicator")
ax2.set_xlabel("Date")
ax2.set_ylabel("Value")
ax2.grid(True, alpha=0.3)
ax2.legend()
st.pyplot(fig2)

st.write(
    """
Official labour market indicators provide broader context for interpreting Jobs Online.
While vacancy data captures changes in job advertising activity, official indicators reflect wider labour market
conditions such as employment levels and labour market pressure.
"""
)

st.header("Latest Available Values")
latest_jobs_value = df_jobs_plot[jobs_total_col].iloc[-1]
latest_jobs_date = df_jobs_plot[jobs_date_col].iloc[-1]

summary_df = pd.DataFrame({
    "Series": ["Jobs Online hiring demand", selected_display],
    "Latest Value": [latest_jobs_value, latest_value],
    "Latest Date": [latest_jobs_date.strftime("%b %Y"), latest_date.strftime("%b %Y")]
})

st.dataframe(summary_df, use_container_width=True)

st.subheader("Key takeaway")
st.write(
    "Official labour market indicators help show whether changes in hiring demand are part of a broader market shift or just a short-term movement in job advertising."
)

with st.expander("Show selected official data preview"):
    st.dataframe(df_indicator.head(), use_container_width=True)
