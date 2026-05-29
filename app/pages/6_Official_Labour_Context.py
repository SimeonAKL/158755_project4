import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Official Labour Context", layout="wide")

from utils.theme import (
    inject_css, page_hero, section_header, info_card, takeaway_card,
    plotly_layout, line_trace,
    CHART_COLORS, HISTORICAL_COLOR, PALETTE,
)

inject_css()
C = PALETTE

page_hero(
    title="Official Labour Context",
    subtitle=(
        "Placing vacancy trends alongside Stats NZ indicators to judge whether "
        "demand signals are supported by wider employment conditions."
    ),
)

MONTHLY_PATH   = os.path.join("data", "integrated", "monthly_labour_market_master.csv")
QUARTERLY_PATH = os.path.join("data", "integrated", "quarterly_labour_force_master.csv")
JOBS_PATH      = os.path.join("data", "integrated", "jobs_online_monthly.csv")

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

try:
    df_monthly   = load_csv(MONTHLY_PATH)
    df_quarterly = load_csv(QUARTERLY_PATH)
    df_jobs      = load_csv(JOBS_PATH)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

def first_match(columns, candidates):
    return next((c for c in candidates if c in columns), None)

def numeric_cols(df):
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

jobs_date_col      = first_match(df_jobs.columns,     ["date","month","Date"])
monthly_date_col   = first_match(df_monthly.columns,  ["date","month","Date"])
quarterly_date_col = first_match(df_quarterly.columns,["date","quarter","Date"])

for df_, col_ in [(df_jobs, jobs_date_col), (df_monthly, monthly_date_col),
                  (df_quarterly, quarterly_date_col)]:
    df_[col_] = pd.to_datetime(df_[col_], errors="coerce")

INDICATOR_LABELS = {
    "male_paid_employee":    "Male Paid Employment",
    "female_paid_employee":  "Female Paid Employment",
    "unemployment_rate":     "Unemployment Rate",
    "underutilisation_rate": "Underutilisation Rate",
    "filled_jobs":           "Filled Jobs",
    "employment_total":      "Total Employment",
}

section_header("Indicator Selection")
st.markdown('<div class="m-controls">', unsafe_allow_html=True)
ca, cb = st.columns(2)
with ca:
    source_type = st.selectbox("Official data frequency",
                               ["Monthly Indicators", "Quarterly Indicators"])
with cb:
    df_ctx  = df_monthly.copy() if source_type == "Monthly Indicators" else df_quarterly.copy()
    ctx_dc  = monthly_date_col if source_type == "Monthly Indicators" else quarterly_date_col
    d2a     = {INDICATOR_LABELS.get(c, c.replace("_"," ").title()): c for c in numeric_cols(df_ctx)}
    pref    = ["Unemployment Rate","Underutilisation Rate",
               "Male Paid Employment","Female Paid Employment","Filled Jobs"]
    ordered = [n for n in pref if n in d2a] + [n for n in d2a if n not in pref]
    sel_disp = st.selectbox("Select official indicator", ordered)
    sel_ind  = d2a[sel_disp]
st.markdown("</div>", unsafe_allow_html=True)

# ── Official indicator chart ──────────────────────────────────────────────────
section_header(f"{sel_disp}", "Stats NZ official labour market series")

df_ind = df_ctx[[ctx_dc, sel_ind]].dropna().sort_values(ctx_dc)
fig1 = go.Figure()
fig1.add_trace(
    line_trace(df_ind[ctx_dc], df_ind[sel_ind],
               name=sel_disp, color=CHART_COLORS[1], width=2, show_markers=True)
)
fig1.update_layout(**plotly_layout(f"{sel_disp} Over Time", x_label="", y_label=sel_disp))
st.plotly_chart(fig1, use_container_width=True)

latest_val  = df_ind[sel_ind].iloc[-1]
latest_date = df_ind[ctx_dc].iloc[-1]
st.write(
    f"The latest available reading for **{sel_disp}** is "
    f"**{latest_val:.2f}** in **{latest_date.strftime('%b %Y')}**."
)

# ── Dual-axis comparison ──────────────────────────────────────────────────────
section_header("Demand vs Official Context",
               "Jobs Online hiring demand alongside the selected official indicator")

df_jp = df_jobs[[jobs_date_col, "totals"]].dropna().sort_values(jobs_date_col)
df_cp = df_ctx[[ctx_dc, sel_ind]].dropna().sort_values(ctx_dc)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=df_jp[jobs_date_col], y=df_jp["totals"],
    name="Jobs Online Hiring Demand", mode="lines",
    line=dict(color=HISTORICAL_COLOR, width=2),
    hovertemplate="<b>Hiring Demand</b>: %{y:.1f}<extra></extra>", yaxis="y1",
))
fig2.add_trace(go.Scatter(
    x=df_cp[ctx_dc], y=df_cp[sel_ind],
    name=sel_disp, mode="lines",
    line=dict(color=CHART_COLORS[1], width=2, dash="dot"),
    hovertemplate=f"<b>{sel_disp}</b>: %{{y:.2f}}<extra></extra>", yaxis="y2",
))
layout = plotly_layout("Hiring Demand vs Official Labour Market Indicator",
                       x_label="", y_label="Hiring Demand Index")
layout["yaxis2"] = dict(
    title=dict(text=sel_disp,
               font=dict(family="Inter, sans-serif", size=11, color=C["text_light"])),
    tickfont=dict(family="Inter, sans-serif", size=11, color=C["text_secondary"]),
    overlaying="y", side="right", showgrid=False, zeroline=False,
)
fig2.update_layout(**layout)
st.plotly_chart(fig2, use_container_width=True)

info_card(
    "How to Read This Chart",
    "The solid line (left axis) shows Jobs Online hiring demand. The dashed line "
    "(right axis) shows the selected Stats NZ indicator. The two series use different "
    "scales — look for directional alignment or divergence, not exact numerical comparisons.",
    "ℹ️",
)

st.write(
    "Official labour market indicators provide broader context for interpreting "
    "Jobs Online. While vacancy data captures changes in job advertising activity, "
    "official indicators reflect wider conditions — employment levels, labour market "
    "slack, and structural shifts — that can help validate or qualify the vacancy signal."
)

section_header("Latest Values Summary")
lat_jobs = df_jp["totals"].iloc[-1]
lat_dt   = df_jp[jobs_date_col].iloc[-1]
summary_df = pd.DataFrame({
    "Series":       ["Jobs Online Hiring Demand", sel_disp],
    "Latest Value": [round(lat_jobs, 2), round(latest_val, 2)],
    "As of":        [lat_dt.strftime("%b %Y"), latest_date.strftime("%b %Y")],
    "Source":       ["MBIE Jobs Online", "Stats NZ"],
})
st.dataframe(summary_df.set_index("Series"), use_container_width=True)

takeaway_card(
    "Official labour market indicators help distinguish between a genuine shift in "
    "market conditions and a short-term movement in job advertising. When hiring "
    "demand and official employment indicators move in the same direction, "
    "the signal is more reliable."
)

with st.expander("View official indicator data"):
    st.dataframe(
        df_ind.rename(columns={ctx_dc: "Date", sel_ind: sel_disp}).head(20),
        use_container_width=True
    )