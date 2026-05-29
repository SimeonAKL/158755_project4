import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Industry Occupation Comparison", layout="wide")

st.title("Industry Occupation Comparison")

st.write(
    """
This page shows where hiring demand is stronger or weaker across key industries and occupations.
It is designed to help users quickly spot uneven demand patterns rather than relying on national trends alone.
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

st.header("Controls")

comparison_type = st.selectbox("Select comparison type", ["Industry", "Occupation"])

if comparison_type == "Industry":
    options_dict = industry_options
else:
    options_dict = occupation_options

available_labels = [label for label, col in options_dict.items() if col in df.columns]

if not available_labels:
    st.error(f"No available columns found for {comparison_type.lower()} comparison.")
    st.stop()

default_selection = available_labels[:3] if len(available_labels) >= 3 else available_labels

selected_labels = st.multiselect(
    f"Select {comparison_type.lower()} groups to compare",
    options=available_labels,
    default=default_selection
)

if not selected_labels:
    st.warning("Please select at least one category.")
    st.stop()

min_date = df[date_col].min().date()
max_date = df[date_col].max().date()

date_range = st.slider(
    "Select date range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

start_date, end_date = date_range
selected_cols = [options_dict[label] for label in selected_labels]

df_plot = df[
    (df[date_col].dt.date >= start_date) &
    (df[date_col].dt.date <= end_date)
][[date_col] + selected_cols].copy()

st.header(f"{comparison_type} Trend Comparison")
fig1, ax1 = plt.subplots(figsize=(10, 5))

for label in selected_labels:
    col = options_dict[label]
    ax1.plot(df_plot[date_col], df_plot[col], label=label)

ax1.set_title(f"{comparison_type} Hiring Demand Trends")
ax1.set_xlabel("Date")
ax1.set_ylabel("Hiring demand")
ax1.grid(True, alpha=0.3)
ax1.legend()
st.pyplot(fig1)

if comparison_type == "Industry":
    st.write(
        """
Industry-level trends show that hiring demand has not moved uniformly across sectors. Some industries appear more resilient
or recover more quickly, while others show weaker or less stable activity.
"""
    )
else:
    st.write(
        """
The occupation analysis shows that labour demand differs across job groups. Some occupation groups maintain stronger demand over time,
while others show greater fluctuation.
"""
    )

st.header(f"Latest {comparison_type} Snapshot")
latest_row = df_plot.dropna(subset=[date_col]).iloc[-1]
latest_date = latest_row[date_col]

latest_values = {}
for label in selected_labels:
    col = options_dict[label]
    latest_values[label] = latest_row[col]

latest_df = pd.DataFrame({
    comparison_type: list(latest_values.keys()),
    "Latest Hiring Demand": list(latest_values.values())
}).sort_values("Latest Hiring Demand", ascending=False)

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.bar(latest_df[comparison_type], latest_df["Latest Hiring Demand"])
ax2.set_title(f"Latest {comparison_type} Hiring Snapshot ({latest_date.strftime('%b %Y')})")
ax2.set_xlabel(comparison_type)
ax2.set_ylabel("Hiring demand")
ax2.grid(True, axis="y", alpha=0.3)
st.pyplot(fig2)

st.header(f"{comparison_type} Ranking Table")
latest_df = latest_df.reset_index(drop=True)
latest_df["Rank"] = latest_df.index + 1
latest_df = latest_df[["Rank", comparison_type, "Latest Hiring Demand"]]
st.dataframe(latest_df, use_container_width=True)

st.header("Summary")
top_group = latest_df.iloc[0]
bottom_group = latest_df.iloc[-1]

col1, col2 = st.columns(2)

with col1:
    st.metric(f"Top {comparison_type.lower()}", top_group[comparison_type], f"{top_group['Latest Hiring Demand']:.1f}")
with col2:
    st.metric(f"Lowest {comparison_type.lower()}", bottom_group[comparison_type], f"{bottom_group['Latest Hiring Demand']:.1f}")

st.write(
    f"""
In the latest available month (**{latest_date.strftime('%b %Y')}**), the highest hiring-demand level among the selected
{comparison_type.lower()} groups is observed in **{top_group[comparison_type]}** at **{top_group['Latest Hiring Demand']:.1f}**,
while the lowest is observed in **{bottom_group[comparison_type]}** at **{bottom_group['Latest Hiring Demand']:.1f}**.
"""
)

st.subheader("Key takeaway")
st.write(
    "Hiring demand is moving unevenly across sectors and occupations, so better decisions come from looking at where demand is actually concentrated rather than relying on national averages alone."
)

with st.expander("Show filtered data preview"):
    preview_df = df_plot.rename(columns={options_dict[label]: label for label in selected_labels})
    st.dataframe(preview_df.head(), use_container_width=True)
