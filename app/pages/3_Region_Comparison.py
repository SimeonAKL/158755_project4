import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Region Comparison", layout="wide")

from utils.theme import (
    inject_css, section_header, takeaway_card,
    plotly_layout, line_trace, bar_trace,
    CHART_COLORS, PALETTE,
)

inject_css()

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("Region Comparison")
st.write(
    "Hiring demand is not distributed evenly across New Zealand. This page compares "
    "monthly Jobs Online activity across major regional labour markets — helping "
    "identify which regions are currently stronger, weaker, or more volatile."
)

# ── Data ──────────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join("data", "integrated", "jobs_online_monthly.csv")

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

try:
    df = load_data(DATA_PATH)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

date_col    = "date"
region_cols = ["auckland", "wellington", "north_island_other", "canterbury", "south_island_other"]
REGION_LABELS = {
    "auckland":            "Auckland",
    "wellington":          "Wellington",
    "north_island_other":  "North Island Other",
    "canterbury":          "Canterbury",
    "south_island_other":  "South Island Other",
}

required_cols = [date_col] + region_cols
missing_cols  = [c for c in required_cols if c not in df.columns]
if missing_cols:
    st.error(f"Missing required columns: {missing_cols}")
    st.stop()

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df = df.sort_values(date_col).reset_index(drop=True)

# ── Controls ──────────────────────────────────────────────────────────────────
section_header("Chart Controls")

with st.container():
    st.markdown('<div class="nz-controls-panel">', unsafe_allow_html=True)
    selected_regions = st.multiselect(
        "Select regions to compare",
        options=region_cols,
        default=["auckland", "wellington", "canterbury"],
        format_func=lambda x: REGION_LABELS.get(x, x),
    )
    st.markdown("</div>", unsafe_allow_html=True)

if not selected_regions:
    st.warning("Please select at least one region.")
    st.stop()

latest_date = df[date_col].dropna().iloc[-1]

# ── Trend comparison ──────────────────────────────────────────────────────────
section_header("Regional Trend Comparison", "monthly hiring demand index by region")

fig1 = go.Figure()
for i, region in enumerate(selected_regions):
    fig1.add_trace(
        line_trace(
            df[date_col], df[region],
            name=REGION_LABELS.get(region, region),
            color=CHART_COLORS[i % len(CHART_COLORS)],
            width=2,
        )
    )
fig1.update_layout(**plotly_layout(
    "Regional Hiring Demand Trends",
    x_label="", y_label="Hiring Demand Index"
))
st.plotly_chart(fig1, use_container_width=True)

st.write(
    "Regional patterns are clearly uneven, reflecting the local economic structure "
    "and sector composition of each region. Some labour markets show stronger or "
    "more sustained hiring activity; others are more sensitive to economic cycles."
)

# ── Latest snapshot bar ───────────────────────────────────────────────────────
section_header("Current Regional Standing",
               f"latest available reading — {latest_date.strftime('%b %Y')}")

latest_row    = df.loc[df[date_col] == latest_date, [date_col] + region_cols].copy()
latest_values = latest_row.iloc[0][selected_regions].sort_values(ascending=False)

bar_colors = [CHART_COLORS[i % len(CHART_COLORS)] for i in range(len(latest_values))]

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=[REGION_LABELS.get(r, r) for r in latest_values.index],
    y=latest_values.values,
    marker=dict(color=bar_colors, line=dict(width=0)),
    hovertemplate="<b>%{x}</b>: %{y:.1f}<extra></extra>",
))
fig2.update_layout(**plotly_layout(
    f"Regional Hiring Demand — {latest_date.strftime('%b %Y')}",
    x_label="Region", y_label="Hiring Demand Index",
    legend=False,
))
st.plotly_chart(fig2, use_container_width=True)

# ── Ranking table ─────────────────────────────────────────────────────────────
section_header("Regional Rankings")

ranking_df = pd.DataFrame({
    "Rank":                 range(1, len(latest_values) + 1),
    "Region":              [REGION_LABELS.get(r, r) for r in latest_values.index],
    "Hiring Demand Index": latest_values.values.round(1),
})
st.dataframe(ranking_df.set_index("Rank"), use_container_width=True)

# ── Summary metrics ───────────────────────────────────────────────────────────
section_header("Period Summary")

top_region    = ranking_df.iloc[0]
bottom_region = ranking_df.iloc[-1]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Strongest Region", top_region["Region"],
              f"{top_region['Hiring Demand Index']:.1f}")
with col2:
    st.metric("Weakest Region", bottom_region["Region"],
              f"{bottom_region['Hiring Demand Index']:.1f}")
with col3:
    spread = top_region["Hiring Demand Index"] - bottom_region["Hiring Demand Index"]
    st.metric("Demand Spread (top vs bottom)", f"{spread:.1f}")

st.write(
    f"In {latest_date.strftime('%b %Y')}, **{top_region['Region']}** leads with a hiring "
    f"demand index of **{top_region['Hiring Demand Index']:.1f}**, while "
    f"**{bottom_region['Region']}** records the lowest at "
    f"**{bottom_region['Hiring Demand Index']:.1f}**."
)

takeaway_card(
    "Hiring demand is not evenly distributed across New Zealand. National averages "
    "can hide important regional opportunities and risks — making regional-level "
    "monitoring essential for geographically informed workforce decisions."
)

with st.expander("View underlying regional data"):
    st.dataframe(df[[date_col] + selected_regions].rename(
        columns={**{date_col: "Date"}, **REGION_LABELS}
    ).head(20), use_container_width=True)
