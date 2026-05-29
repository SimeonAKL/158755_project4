import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Region Comparison", layout="wide")

from utils.theme import (
    inject_css, page_hero, section_header, takeaway_card,
    plotly_layout, line_trace,
    CHART_COLORS, PALETTE,
)

inject_css()
C = PALETTE

page_hero(
    title="Region Comparison",
    subtitle=(
        "Comparing monthly Jobs Online activity across major regional labour markets — "
        "identifying which regions are currently stronger, weaker, or more volatile."
    ),
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

date_col    = "date"
region_cols = ["auckland", "wellington", "north_island_other", "canterbury", "south_island_other"]
LABELS      = {
    "auckland":           "Auckland",
    "wellington":         "Wellington",
    "north_island_other": "North Island Other",
    "canterbury":         "Canterbury",
    "south_island_other": "South Island Other",
}

missing = [c for c in [date_col] + region_cols if c not in df.columns]
if missing:
    st.error(f"Missing required columns: {missing}")
    st.stop()

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df = df.sort_values(date_col).reset_index(drop=True)

section_header("Chart Controls")
st.markdown('<div class="m-controls">', unsafe_allow_html=True)
selected = st.multiselect(
    "Select regions to compare",
    options=region_cols, default=["auckland", "wellington", "canterbury"],
    format_func=lambda x: LABELS.get(x, x),
)
st.markdown("</div>", unsafe_allow_html=True)

if not selected:
    st.warning("Please select at least one region.")
    st.stop()

latest_date = df[date_col].dropna().iloc[-1]

# ── Trend chart ───────────────────────────────────────────────────────────────
section_header("Regional Trend Comparison", "monthly hiring demand index by region")

fig1 = go.Figure()
for i, region in enumerate(selected):
    fig1.add_trace(
        line_trace(df[date_col], df[region],
                   name=LABELS.get(region, region),
                   color=CHART_COLORS[i % len(CHART_COLORS)], width=2)
    )
fig1.update_layout(**plotly_layout(
    "Regional Hiring Demand Trends", x_label="", y_label="Hiring Demand Index"))
st.plotly_chart(fig1, use_container_width=True)

st.write(
    "Regional patterns are clearly uneven, reflecting the local economic structure "
    "and sector composition of each region. Some labour markets show stronger or "
    "more sustained hiring activity; others are more sensitive to economic cycles."
)

# ── Snapshot bar ─────────────────────────────────────────────────────────────
section_header("Current Regional Standing",
               f"latest available reading — {latest_date.strftime('%b %Y')}")

latest_row = df.loc[df[date_col] == latest_date, [date_col] + region_cols].copy()
latest_vals = latest_row.iloc[0][selected].sort_values(ascending=False)

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=[LABELS.get(r, r) for r in latest_vals.index],
    y=latest_vals.values,
    marker=dict(
        color=[CHART_COLORS[i % len(CHART_COLORS)] for i in range(len(latest_vals))],
        line=dict(width=0),
    ),
    hovertemplate="<b>%{x}</b>: %{y:.1f}<extra></extra>",
))
fig2.update_layout(**plotly_layout(
    f"Regional Hiring Demand — {latest_date.strftime('%b %Y')}",
    x_label="Region", y_label="Hiring Demand Index", legend=False))
st.plotly_chart(fig2, use_container_width=True)

# ── Rankings ──────────────────────────────────────────────────────────────────
section_header("Regional Rankings")

ranking_df = pd.DataFrame({
    "Rank":                range(1, len(latest_vals) + 1),
    "Region":             [LABELS.get(r, r) for r in latest_vals.index],
    "Hiring Demand Index": latest_vals.values.round(1),
})
st.dataframe(ranking_df.set_index("Rank"), use_container_width=True)

section_header("Period Summary")
top    = ranking_df.iloc[0]
bottom = ranking_df.iloc[-1]
c1, c2, c3 = st.columns(3)
with c1: st.metric("Strongest Region", top["Region"], f"{top['Hiring Demand Index']:.1f}")
with c2: st.metric("Weakest Region",   bottom["Region"], f"{bottom['Hiring Demand Index']:.1f}")
with c3: st.metric("Demand Spread",    f"{top['Hiring Demand Index'] - bottom['Hiring Demand Index']:.1f}")

st.write(
    f"In {latest_date.strftime('%b %Y')}, **{top['Region']}** leads with a hiring "
    f"demand index of **{top['Hiring Demand Index']:.1f}**, while "
    f"**{bottom['Region']}** records the lowest at **{bottom['Hiring Demand Index']:.1f}**."
)

takeaway_card(
    "Hiring demand is not evenly distributed across New Zealand. National averages "
    "can hide important regional opportunities and risks — making regional-level "
    "monitoring essential for geographically informed workforce decisions."
)

with st.expander("View underlying regional data"):
    st.dataframe(
        df[[date_col] + selected].rename(columns={**{date_col: "Date"}, **LABELS}).head(20),
        use_container_width=True
    )