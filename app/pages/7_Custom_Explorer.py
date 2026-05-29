import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Custom Explorer", layout="wide")

st.title("Custom Explorer")

st.write(
    """
This page allows users to explore selected labour-demand series interactively.
Users can choose a region, industry, occupation, or skill-related series and display the selected trend over a chosen time range.
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
# Required date column
# ============================================================
date_col = "date"
if date_col not in df.columns:
    st.error("The required 'date' column was not found in jobs_online_monthly.csv")
    st.write("Available columns:", list(df.columns))
    st.stop()

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df = df.sort_values(date_col).reset_index(drop=True)

# ============================================================
# Groups of selectable series
# ============================================================
region_options = {
    "Auckland": "auckland",
    "Wellington": "wellington",
    "North Island Other": "north_island_other",
    "Canterbury": "canterbury",
    "South Island Other": "south_island_other"
}

industry_options = {
    "Business Services": "business_services",
    "Construction": "construction",
    "Education": "education",
    "Health Care": "health_care",
    "Hospitality": "hospitality",
    "IT": "it",
    "Manufacturing": "manufacturing",
    "Primary": "primary",
    "Sales": "sales",
    "Other": "other"
}

occupation_options = {
    "Managers": "managers",
    "Professionals": "professionals",
    "Technicians and Trades Workers": "technicians_and_trades_workers",
    "Community and Personal Service Workers": "community_and_personal_service_workers",
    "Clerical and Administrative Workers": "clerical_and_administrative_workers",
    "Sales Workers": "sales_workers",
    "Machinery Operators and Drivers": "machinery_operators_and_drivers",
    "Labourers": "labourers"
}

skill_options = {
    "Highly Skilled": "highly_skilled",
    "Skilled": "skilled",
    "Semi-Skilled": "semi_skilled",
    "Low-Skilled": "low_skilled",
    "Unskilled": "unskilled"
}

# ============================================================
# Check available columns
# ============================================================
all_needed = (
    list(region_options.values()) +
    list(industry_options.values()) +
    list(occupation_options.values()) +
    list(skill_options.values())
)

missing_cols = [c for c in all_needed if c not in df.columns]

if missing_cols:
    st.warning("Some expected columns are missing from the dataset.")
    st.write("Missing columns:", missing_cols)

# ============================================================
# Controls
# ============================================================
st.header("Explorer Controls")

series_group = st.selectbox(
    "Select data group",
    ["Region", "Industry", "Occupation", "Skill Group"]
)

if series_group == "Region":
    options_dict = region_options
elif series_group == "Industry":
    options_dict = industry_options
elif series_group == "Occupation":
    options_dict = occupation_options
else:
    options_dict = skill_options

available_labels = [label for label, col in options_dict.items() if col in df.columns]

if not available_labels:
    st.error(f"No available columns found for {series_group}.")
    st.stop()

selected_label = st.selectbox(
    f"Select {series_group.lower()}",
    available_labels
)

selected_col = options_dict[selected_label]

min_date = df[date_col].min().date()
max_date = df[date_col].max().date()

date_range = st.slider(
    "Select date range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# ============================================================
# Filter data
# ============================================================
start_date, end_date = date_range

df_plot = df[
    (df[date_col].dt.date >= start_date) &
    (df[date_col].dt.date <= end_date)
][[date_col, selected_col]].dropna()

if df_plot.empty:
    st.warning("No data available for the selected combination.")
    st.stop()

# ============================================================
# Plot
# ============================================================
st.header("Selected Series Trend")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_plot[date_col], df_plot[selected_col], marker="o")
ax.set_title(f"{selected_label} Labour Demand Trend")
ax.set_xlabel("Date")
ax.set_ylabel("Vacancy Index")
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# ============================================================
# Summary metrics
# ============================================================
st.header("Summary Metrics")

latest_value = df_plot[selected_col].iloc[-1]
latest_date = df_plot[date_col].iloc[-1]
peak_value = df_plot[selected_col].max()
trough_value = df_plot[selected_col].min()
avg_value = df_plot[selected_col].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Latest value", f"{latest_value:.1f}")

with col2:
    st.metric("Average value", f"{avg_value:.1f}")

with col3:
    st.metric("Peak value", f"{peak_value:.1f}")

with col4:
    st.metric("Lowest value", f"{trough_value:.1f}")

st.write(
    f"""
The selected series is **{selected_label}** under the **{series_group}** group.
The latest observed value is **{latest_value:.1f}** in **{latest_date.strftime('%b %Y')}**.
This interactive view allows users to inspect how different labour-demand series change over time rather than relying only on fixed charts.
"""
)

# ============================================================
# Table view
# ============================================================
st.header("Filtered Data Table")

display_df = df_plot.rename(columns={selected_col: "value"}).reset_index(drop=True)
st.dataframe(display_df, use_container_width=True)

# ============================================================
# Download button
# ============================================================
csv_data = display_df.to_csv(index=False).encode("utf-8")
safe_name = selected_label.lower().replace(" ", "_").replace("-", "_")

st.download_button(
    label="Download filtered data as CSV",
    data=csv_data,
    file_name=f"{safe_name}_custom_explorer.csv",
    mime="text/csv"
)