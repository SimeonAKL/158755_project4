import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Region Comparison", layout="wide")

st.title("Region Comparison")

st.write(
    """
This page compares labour-demand patterns across major regions in New Zealand using the monthly Jobs Online series.
Use it to identify which regional job markets are currently stronger, weaker, or more volatile.
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
region_cols = ["auckland", "wellington", "north_island_other", "canterbury", "south_island_other"]

required_cols = [date_col] + region_cols
missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    st.error(f"Missing required columns: {missing_cols}")
    st.write("Available columns:", list(df.columns))
    st.stop()

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df = df.sort_values(date_col).reset_index(drop=True)

st.header("Controls")

selected_regions = st.multiselect(
    "Select regions to compare",
    options=region_cols,
    default=["auckland", "wellington", "canterbury"]
)

if not selected_regions:
    st.warning("Please select at least one region.")
    st.stop()

latest_date = df[date_col].dropna().iloc[-1]

st.header("Regional Trend Comparison")
fig1, ax1 = plt.subplots(figsize=(10, 5))

for region in selected_regions:
    ax1.plot(df[date_col], df[region], label=region.replace("_", " ").title())

ax1.set_title("Regional Hiring Demand Trends")
ax1.set_xlabel("Date")
ax1.set_ylabel("Hiring demand")
ax1.legend()
ax1.grid(True, alpha=0.3)
st.pyplot(fig1)

st.write(
    """
Regional patterns are clearly uneven, which suggests that labour demand is influenced by local economic structure and
the concentration of different industries. Some regions show stronger or more sustained hiring growth, while others appear more volatile.
"""
)

st.header("Latest Regional Snapshot")
latest_row = df.loc[df[date_col] == latest_date, [date_col] + region_cols].copy()
latest_values = latest_row.iloc[0][selected_regions].sort_values(ascending=False)

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.bar([r.replace("_", " ").title() for r in latest_values.index], latest_values.values)
ax2.set_title(f"Regional Hiring Demand ({latest_date.strftime('%b %Y')})")
ax2.set_xlabel("Region")
ax2.set_ylabel("Hiring demand")
ax2.grid(True, axis="y", alpha=0.3)
st.pyplot(fig2)

st.header("Regional Ranking Table")
ranking_df = pd.DataFrame({
    "Region": [r.replace("_", " ").title() for r in latest_values.index],
    "Latest Hiring Demand": latest_values.values
})
ranking_df["Rank"] = range(1, len(ranking_df) + 1)
ranking_df = ranking_df[["Rank", "Region", "Latest Hiring Demand"]]
st.dataframe(ranking_df, use_container_width=True)

st.header("Summary")
top_region = ranking_df.iloc[0]
bottom_region = ranking_df.iloc[-1]

col1, col2 = st.columns(2)

with col1:
    st.metric("Top region", top_region["Region"], f"{top_region['Latest Hiring Demand']:.1f}")
with col2:
    st.metric("Lowest region", bottom_region["Region"], f"{bottom_region['Latest Hiring Demand']:.1f}")

st.write(
    f"In the latest month ({latest_date.strftime('%b %Y')}), the strongest hiring-demand reading among the selected regions is **{top_region['Region']}** at **{top_region['Latest Hiring Demand']:.1f}**, while the weakest is **{bottom_region['Region']}** at **{bottom_region['Latest Hiring Demand']:.1f}**."
)

st.subheader("Key takeaway")
st.write(
    "Hiring demand is not evenly distributed across New Zealand, so national averages can hide important regional opportunities and risks."
)

with st.expander("Show regional data preview"):
    st.dataframe(df[[date_col] + selected_regions].head(), use_container_width=True)
