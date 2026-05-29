import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Custom Explorer", layout="wide")

st.title("Custom Explorer")

st.write(
    """
This page allows users to explore hiring demand across regions, industries, occupations, and skill groups in a flexible way.
It is designed for users who want to investigate a specific part of the job market rather than follow fixed dashboard views.
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
if date_col not in df.columns:
    st.error("The required 'date' column was not found in jobs_online_monthly.csv")
    st.write("Available columns:", list(df.columns))
    st.stop()

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df = df.sort_values(date_col).reset_index(drop=True)

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
    "Technicians & Trades": "technicians_and_trades_workers",
    "Community & Personal Services": "community_and_personal_service_workers",
    "Clerical & Admin": "clerical_and_administrative_workers",
    "Sales Workers": "sales_workers",
    "Machinery Operators & Drivers": "machinery_operators_and_drivers",
    "Labourers": "labourers"
}

skill_options = {
    "Highly Skilled": "highly_skilled",
    "Skilled": "skilled",
    "Semi-Skilled": "semi_skilled",
    "Low-Skilled": "low_skilled",
    "Unskilled": "unskilled"
}

st.header("Explorer Controls")

series_group = st.selectbox("Select data group", ["Region", "Industry", "Occupation", "Skill Group"])

if series_group == "Region":
    options_dict = region_options
elif series_group == "Industry":
    options_dict = industry_options
elif series_group == "Occupation":
    options_dict = occupation_options
else:
    options_dict = skill_options

available_labels = [label for label, col in options_dict.items() if col in df.columns]

selected_labels = st.multiselect(
    f"Select {series_group.lower()} series",
    available_labels,
    default=available_labels[:2] if len(available_labels) >= 2 else available_labels
)

if not selected_labels:
    st.warning("Please select at least one series.")
    st.stop()

min_date = df[date_col].min().date()
max_date = df[date_col].max().date()

date_range = st.slider(
    "Select date range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

normalize = st.checkbox("Show indexed comparison (base = 100)")

start_date, end_date = date_range

selected_cols = [options_dict[label] for label in selected_labels]

df_plot = df[
    (df[date_col].dt.date >= start_date) &
    (df[date_col].dt.date <= end_date)
][[date_col] + selected_cols].dropna()

if df_plot.empty:
    st.warning("No data available for the selected combination.")
    st.stop()

plot_df = df_plot.copy()

if normalize:
    for col in selected_cols:
        base_value = plot_df[col].iloc[0]
        if base_value != 0:
            plot_df[col] = plot_df[col] / base_value * 100

st.header("Selected Series Trend")
fig, ax = plt.subplots(figsize=(10, 5))
for label in selected_labels:
    col = options_dict[label]
    ax.plot(plot_df[date_col], plot_df[col], label=label)

ax.set_title(f"{series_group} Hiring Demand Trend")
ax.set_xlabel("Date")
ax.set_ylabel("Indexed value" if normalize else "Hiring demand")
ax.legend()
ax.grid(True, alpha=0.3)
st.pyplot(fig)

st.header("Summary Metrics")
summary_rows = []
for label in selected_labels:
    col = options_dict[label]
    summary_rows.append({
        "Series": label,
        "Latest value": df_plot[col].iloc[-1],
        "Average value": df_plot[col].mean(),
        "Peak value": df_plot[col].max(),
        "Lowest value": df_plot[col].min()
    })

summary_df = pd.DataFrame(summary_rows)
st.dataframe(summary_df, use_container_width=True)

st.write(
    """
This interactive view allows users to inspect how different labour-demand series change over time rather than relying only on fixed charts.
"""
)

st.header("Filtered Data Table")
display_df = df_plot.rename(columns={options_dict[label]: label for label in selected_labels}).reset_index(drop=True)
st.dataframe(display_df, use_container_width=True)

csv_data = display_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download filtered data as CSV",
    data=csv_data,
    file_name="custom_explorer_selection.csv",
    mime="text/csv"
)

st.subheader("Key takeaway")
st.write(
    "Interactive exploration makes it easier to identify where hiring demand matters most for a specific sector, region, occupation, or skill group."
)
