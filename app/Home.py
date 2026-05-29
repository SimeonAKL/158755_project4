import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="NZ Labour Demand Forecaster",
    page_icon="🌊",
    layout="wide",
)

from utils.theme import (
    inject_css, section_header, info_card, takeaway_card,
    plotly_layout, line_trace, forecast_band_trace,
    CHART_COLORS, HISTORICAL_COLOR, FORECAST_COLOR, PALETTE,
)

inject_css()

# ── Page header ──────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div style="
        background: linear-gradient(135deg, {PALETTE['deep_blue']} 0%, {PALETTE['ocean_blue']} 60%, {PALETTE['teal']} 100%);
        border-radius: 12px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        color: white;
    ">
        <div style="font-size:0.78rem; font-weight:700; text-transform:uppercase;
                    letter-spacing:0.18em; color:rgba(255,255,255,0.85); margin-bottom:0.65rem;">
            New Zealand · Labour Market Intelligence
        </div>
        <h1 style="font-family:'DM Serif Display',serif; font-size:3rem; font-weight:400;
                   color:#ffffff; border:none; margin:0 0 1rem 0; padding:0; line-height:1.15;">
            NZ Labour Demand Forecaster
        </h1>
        <p style="font-size:1.1rem; color:#ffffff; margin:0; max-width:680px; line-height:1.7;">
            A decision-support view of short-term hiring demand across New Zealand —
            tracking where hiring is rising, softening, or holding steady across regions,
            sectors, and occupations.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Data loading ─────────────────────────────────────────────────────────────
JOBS_PATH             = os.path.join("data", "integrated", "jobs_online_monthly.csv")
TOTALS_FORECAST_PATH  = os.path.join("data", "forecast", "totals_forecast_results.csv")
INDUSTRY_FORECAST_PATH = os.path.join("data", "forecast", "industries_forecast_results.csv")
REGION_FORECAST_PATH  = os.path.join("data", "forecast", "regional_forecast_results.csv")

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

try:
    df_jobs      = load_csv(JOBS_PATH)
    df_totals_fc = load_csv(TOTALS_FORECAST_PATH)
    df_ind_fc    = load_csv(INDUSTRY_FORECAST_PATH)
    df_reg_fc    = load_csv(REGION_FORECAST_PATH)
except Exception as e:
    st.error(f"Unable to load dashboard data: {e}")
    st.stop()

# Validate & parse
for col in ["date", "totals"]:
    if col not in df_jobs.columns:
        st.error(f"jobs_online_monthly.csv is missing the '{col}' column.")
        st.stop()

df_jobs["date"] = pd.to_datetime(df_jobs["date"], errors="coerce")
df_jobs = df_jobs.sort_values("date").dropna(subset=["date", "totals"]).reset_index(drop=True)

df_totals_fc["date"] = pd.to_datetime(df_totals_fc["date"], errors="coerce")
df_totals_fc = df_totals_fc.sort_values("date").dropna(subset=["date", "forecast"]).reset_index(drop=True)

# ── Summary metrics ───────────────────────────────────────────────────────────
latest_jobs_value  = df_jobs["totals"].iloc[-1]
latest_jobs_date   = df_jobs["date"].iloc[-1]
peak_jobs_value    = df_jobs["totals"].max()
peak_jobs_date     = df_jobs.loc[df_jobs["totals"].idxmax(), "date"]
trough_jobs_value  = df_jobs["totals"].min()
trough_jobs_date   = df_jobs.loc[df_jobs["totals"].idxmin(), "date"]

latest_fc_value    = df_totals_fc["forecast"].iloc[-1]
latest_fc_date     = df_totals_fc["date"].iloc[-1]
fc_change          = (
    latest_fc_value - df_totals_fc["forecast"].iloc[-2]
    if len(df_totals_fc) >= 2 else 0.0
)

section_header("Market Snapshot", "latest available readings")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Current Hiring Demand", f"{latest_jobs_value:.1f}",
              latest_jobs_date.strftime("%b %Y"))
with col2:
    st.metric("Historical Peak", f"{peak_jobs_value:.1f}",
              peak_jobs_date.strftime("%b %Y"))
with col3:
    st.metric("Historical Trough", f"{trough_jobs_value:.1f}",
              trough_jobs_date.strftime("%b %Y"))
with col4:
    st.metric("Near-Term Forecast", f"{latest_fc_value:.2f}",
              f"{fc_change:+.2f} vs prior period")

st.info("📌 Short-term hiring demand is active overall, but the outlook is uneven across sectors and regions.")

# ── Main trend chart ──────────────────────────────────────────────────────────
section_header("National Hiring Demand", "Jobs Online monthly index — full history")

fig1 = go.Figure()
fig1.add_trace(
    line_trace(df_jobs["date"], df_jobs["totals"],
               name="Hiring Demand Index",
               color=HISTORICAL_COLOR, width=2)
)
fig1.update_layout(**plotly_layout(
    "Overall NZ Hiring Demand Trend",
    x_label="", y_label="Hiring Demand Index"
))
st.plotly_chart(fig1, use_container_width=True)

st.markdown(
    "<p style='font-size:1rem; color:#0D1F2D; line-height:1.75;'>"
    "New Zealand hiring demand has moved through clear cycles of contraction and recovery. "
    "The series responds to broad economic conditions, making timely monitoring valuable for "
    "workforce planning and market positioning."
    "</p>",
    unsafe_allow_html=True,
)

# ── Forecast preview ──────────────────────────────────────────────────────────
section_header("Near-Term National Forecast", "projected hiring demand — latest 6 periods")

df_fc_plot = df_totals_fc.tail(6).copy()

fig2 = go.Figure()

if "lower_bound" in df_fc_plot.columns and "upper_bound" in df_fc_plot.columns:
    fig2.add_trace(
        forecast_band_trace(df_fc_plot["date"],
                            df_fc_plot["lower_bound"],
                            df_fc_plot["upper_bound"])
    )

fig2.add_trace(
    line_trace(df_fc_plot["date"], df_fc_plot["forecast"],
               name="Forecast", color=FORECAST_COLOR,
               width=2.5, show_markers=True)
)
fig2.update_layout(**plotly_layout(
    "National Forecast — Latest Periods",
    x_label="", y_label="Forecast Level"
))
st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    f"<p style='font-size:1rem; color:#0D1F2D; line-height:1.75;'>"
    f"The most recent national forecast reading is <strong>{latest_fc_value:.2f}</strong> for "
    f"<strong>{latest_fc_date.strftime('%b %Y')}</strong>. This is a short-term directional signal, "
    "not a long-run projection — designed to help identify whether hiring momentum is "
    "building, holding, or easing."
    "</p>",
    unsafe_allow_html=True,
)

# ── Industry & Regional snapshot tables ───────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    section_header("Industry Outlook", "latest forecast by sector")
    industry_map = {
        "IT":           "it_forecast",
        "Health Care":  "health_care_forecast",
        "Construction": "construction_forecast",
        "Education":    "education_forecast",
        "Hospitality":  "hospitality_forecast",
        "Sales":        "sales_forecast",
    }
    industry_latest = {}
    for label, col in industry_map.items():
        if col in df_ind_fc.columns:
            series = df_ind_fc[col].dropna()
            if not series.empty:
                industry_latest[label] = series.iloc[-1]

    if industry_latest:
        ind_df = (
            pd.DataFrame({"Sector": list(industry_latest.keys()),
                          "Forecast Index": list(industry_latest.values())})
            .sort_values("Forecast Index", ascending=False)
            .reset_index(drop=True)
        )
        ind_df.index += 1
        st.dataframe(ind_df, use_container_width=True)
        top_ind = ind_df.iloc[0]
        st.caption(
            f"**{top_ind['Sector']}** leads the sector forecasts at **{top_ind['Forecast Index']:.2f}**."
        )

with col_right:
    section_header("Regional Outlook", "latest forecast by region")
    region_map = {
        "Auckland":   "auckland_forecast",
        "Wellington": "wellington_forecast",
        "Canterbury": "canterbury_forecast",
    }
    region_latest = {}
    for label, col in region_map.items():
        if col in df_reg_fc.columns:
            series = df_reg_fc[col].dropna()
            if not series.empty:
                region_latest[label] = series.iloc[-1]

    if region_latest:
        reg_df = (
            pd.DataFrame({"Region": list(region_latest.keys()),
                          "Forecast Index": list(region_latest.values())})
            .sort_values("Forecast Index", ascending=False)
            .reset_index(drop=True)
        )
        reg_df.index += 1
        st.dataframe(reg_df, use_container_width=True)
        top_reg = reg_df.iloc[0]
        st.caption(
            f"**{top_reg['Region']}** records the highest regional forecast at **{top_reg['Forecast Index']:.2f}**."
        )

# ── Why it matters ────────────────────────────────────────────────────────────
section_header("About This Dashboard")

c1, c2, c3 = st.columns(3)
with c1:
    info_card(
        "Who It's For",
        "HR leaders, recruiters, economists, and policy makers who need a fast, "
        "evidence-based view of where New Zealand hiring conditions are heading.",
        "👥"
    )
with c2:
    info_card(
        "What It Shows",
        "National trends, regional contrasts, sector-level patterns, and short-term "
        "forecasts — all drawn from MBIE Jobs Online data and Stats NZ official indicators.",
        "📊"
    )
with c3:
    info_card(
        "How To Use It",
        "Navigate using the left-hand menu. Each page focuses on a different lens: "
        "time trends, geography, industry, occupation, forecast, and official context.",
        "🧭"
    )

takeaway_card(
    "New Zealand hiring demand does not move uniformly. National averages can mask "
    "important regional and sector-level divergence — and the near-term forecast signal "
    "can differ meaningfully from current conditions."
)