import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Forecast Explorer", layout="wide")

from utils.theme import (
    inject_css, page_hero, section_header, info_card, takeaway_card,
    plotly_layout, line_trace, forecast_band_trace,
    FORECAST_COLOR, PALETTE,
)

inject_css()
C = PALETTE

page_hero(
    title="Forecast Explorer",
    subtitle=(
        "Short-term hiring demand forecasts projected 3–6 months ahead — "
        "national, sector, and regional views."
    ),
)

TOTALS_PATH     = os.path.join("data", "forecast", "totals_forecast_results.csv")
INDUSTRIES_PATH = os.path.join("data", "forecast", "industries_forecast_results.csv")
REGIONS_PATH    = os.path.join("data", "forecast", "regional_forecast_results.csv")

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

try:
    df_totals     = load_csv(TOTALS_PATH)
    df_industries = load_csv(INDUSTRIES_PATH)
    df_regions    = load_csv(REGIONS_PATH)
except Exception as e:
    st.error(f"Error loading forecast data: {e}")
    st.stop()

for dframe in [df_totals, df_industries, df_regions]:
    dframe["date"] = pd.to_datetime(dframe["date"], errors="coerce")

section_header("Forecast Selection")
with st.container(border=True):
    ca, cb, _ = st.columns(3)
    with ca:
        forecast_type = st.selectbox("Forecast scope", ["National", "Industry", "Region"])
    with cb:
        horizon = st.selectbox("Periods to display", [3, 6], index=1)

def render_forecast(df_plot, label, fc_col, lo_col, hi_col):
    df_plot = df_plot.dropna(subset=[fc_col]).sort_values("date").tail(horizon)
    if df_plot.empty:
        st.warning("No forecast data available.")
        return

    latest_fc   = df_plot[fc_col].iloc[-1]
    latest_date = df_plot["date"].iloc[-1]
    lo_val      = df_plot[lo_col].iloc[-1]
    hi_val      = df_plot[hi_col].iloc[-1]

    direction_label = "Stable"
    direction_color = C["text_secondary"]
    if len(df_plot) >= 2:
        prev = df_plot[fc_col].iloc[-2]
        if latest_fc > prev:
            direction_label, direction_color = "↑ Strengthening", C["positive"]
        elif latest_fc < prev:
            direction_label, direction_color = "↓ Softening",     C["negative"]

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Latest Forecast", f"{latest_fc:.2f}", latest_date.strftime("%b %Y"))
    with c2: st.metric("Lower Bound",     f"{lo_val:.2f}")
    with c3: st.metric("Upper Bound",     f"{hi_val:.2f}")
    with c4:
        st.markdown(
            f"""<div class="m-status-card">
                <div class="m-status-label">Near-Term Direction</div>
                <div class="m-status-value" style="color:{direction_color};">
                    {direction_label}</div>
            </div>""",
            unsafe_allow_html=True,
        )

    fig = go.Figure()
    fig.add_trace(forecast_band_trace(df_plot["date"], df_plot[lo_col], df_plot[hi_col]))
    fig.add_trace(
        line_trace(df_plot["date"], df_plot[fc_col],
                   name=label, color=FORECAST_COLOR, width=2.5, show_markers=True)
    )
    fig.update_layout(**plotly_layout(
        f"{label} — Short-Term Hiring Demand Forecast",
        x_label="", y_label="Forecast Level"))
    st.plotly_chart(fig, use_container_width=True)

    st.write(
        f"The latest forecast for **{label}** is **{latest_fc:.2f}** in "
        f"**{latest_date.strftime('%b %Y')}**. The shaded band represents the forecast "
        "confidence interval — a wider band indicates more uncertainty in the projection."
    )

    disp = df_plot.rename(columns={fc_col: "Forecast", lo_col: "Lower Bound", hi_col: "Upper Bound"})
    disp = disp[["date", "Forecast", "Lower Bound", "Upper Bound"]].reset_index(drop=True)
    disp["date"] = disp["date"].dt.strftime("%b %Y")
    disp = disp.rename(columns={"date": "Period"})
    st.dataframe(disp, use_container_width=True)

    st.download_button(
        label="Download forecast data as CSV",
        data=disp.to_csv(index=False).encode("utf-8"),
        file_name=f"{label.lower().replace(' ', '_')}_forecast.csv",
        mime="text/csv",
    )

if forecast_type == "National":
    section_header("National Forecast", "projected aggregate hiring demand for New Zealand")
    render_forecast(df_totals.copy(), "National", "forecast", "lower_bound", "upper_bound")
    takeaway_card(
        "Short-term national forecast signals can help decision-makers see whether "
        "aggregate hiring demand is stable, strengthening, or softening in the near term "
        "before those shifts show up in official employment statistics."
    )

elif forecast_type == "Industry":
    ind_opts = {
        "IT":           ("it_forecast",           "it_lower",           "it_upper"),
        "Health Care":  ("health_care_forecast",  "health_care_lower",  "health_care_upper"),
        "Construction": ("construction_forecast", "construction_lower", "construction_upper"),
        "Education":    ("education_forecast",    "education_lower",    "education_upper"),
        "Hospitality":  ("hospitality_forecast",  "hospitality_lower",  "hospitality_upper"),
        "Sales":        ("sales_forecast",        "sales_lower",        "sales_upper"),
    }
    with st.container(border=True):
        sel_ind = st.selectbox("Select sector", list(ind_opts.keys()))

    fc_col, lo_col, hi_col = ind_opts[sel_ind]
    section_header(f"{sel_ind} Forecast", "projected hiring demand — sector level")
    render_forecast(df_industries[["date", fc_col, lo_col, hi_col]].copy(),
                    sel_ind, fc_col, lo_col, hi_col)
    takeaway_card(
        f"Sector-level forecasts highlight whether **{sel_ind}** hiring momentum is "
        "tracking differently from the national picture — valuable for sector-specific "
        "workforce planning and capacity decisions."
    )

elif forecast_type == "Region":
    reg_opts = {
        "Auckland":   ("auckland_forecast",   "auckland_lower",   "auckland_upper"),
        "Wellington": ("wellington_forecast", "wellington_lower", "wellington_upper"),
        "Canterbury": ("canterbury_forecast", "canterbury_lower", "canterbury_upper"),
    }
    with st.container(border=True):
        sel_reg = st.selectbox("Select region", list(reg_opts.keys()))

    fc_col, lo_col, hi_col = reg_opts[sel_reg]
    section_header(f"{sel_reg} Forecast", "projected hiring demand — regional level")
    render_forecast(df_regions[["date", fc_col, lo_col, hi_col]].copy(),
                    sel_reg, fc_col, lo_col, hi_col)
    takeaway_card(
        f"Regional forecast signals show whether **{sel_reg}** hiring demand is tracking "
        "above or below the national trend — important for location-specific workforce "
        "and resource planning."
    )

section_header("Reading These Forecasts")
c1, c2, c3 = st.columns(3)
with c1:
    info_card("Forecast Line",
              "The central line shows the model's best estimate of hiring demand "
              "for each projected period.", "📈")
with c2:
    info_card("Confidence Band",
              "The shaded area represents forecast uncertainty. A wider band means "
              "more variability — treat it as a range, not a single point.", "🎯")
with c3:
    info_card("Horizon",
              "These are short-term projections (3–6 months). They reflect near-term "
              "momentum, not long-run structural forecasts.", "📅")