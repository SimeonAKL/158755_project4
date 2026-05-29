import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Forecast Explorer", layout="wide")

from utils.theme import (
    inject_css, section_header, info_card, takeaway_card,
    plotly_layout, line_trace, forecast_band_trace,
    FORECAST_COLOR, PALETTE,
)

inject_css()

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("Forecast Explorer")
st.write(
    "Short-term forecasts of NZ labour demand, projected 3–6 months ahead. "
    "Switch between national, industry, and regional views to explore where "
    "hiring momentum is building, holding, or softening."
)

# ── Data ──────────────────────────────────────────────────────────────────────
TOTALS_PATH    = os.path.join("data", "forecast", "totals_forecast_results.csv")
INDUSTRIES_PATH = os.path.join("data", "forecast", "industries_forecast_results.csv")
REGIONS_PATH   = os.path.join("data", "forecast", "regional_forecast_results.csv")

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

# ── Controls ──────────────────────────────────────────────────────────────────
section_header("Forecast Selection")

with st.container():
    st.markdown('<div class="nz-controls-panel">', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        forecast_type = st.selectbox("Forecast scope", ["National", "Industry", "Region"])
    with col_b:
        horizon = st.selectbox("Periods to display", [3, 6], index=1,
                               help="Number of forecast periods shown in the chart and table.")
    with col_c:
        st.markdown("")  # spacer
    st.markdown("</div>", unsafe_allow_html=True)

# ── Helper: render a forecast chart + metrics + table ─────────────────────────
def render_forecast(df_plot, label, forecast_col, lower_col, upper_col):
    df_plot = df_plot.dropna(subset=[forecast_col]).sort_values("date").tail(horizon)

    if df_plot.empty:
        st.warning("No forecast data available for the selected combination.")
        return

    latest_fc   = df_plot[forecast_col].iloc[-1]
    latest_date = df_plot["date"].iloc[-1]
    lower_val   = df_plot[lower_col].iloc[-1]
    upper_val   = df_plot[upper_col].iloc[-1]

    # Direction signal
    direction_label = "Stable"
    direction_color = PALETTE["text_secondary"]
    if len(df_plot) >= 2:
        prev = df_plot[forecast_col].iloc[-2]
        if latest_fc > prev:
            direction_label = "↑ Strengthening"
            direction_color = PALETTE["sage_green"]
        elif latest_fc < prev:
            direction_label = "↓ Softening"
            direction_color = PALETTE["danger"]

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Latest Forecast", f"{latest_fc:.2f}",
                  latest_date.strftime("%b %Y"))
    with col2:
        st.metric("Lower Bound", f"{lower_val:.2f}")
    with col3:
        st.metric("Upper Bound", f"{upper_val:.2f}")
    with col4:
        st.markdown(
            f"""
            <div style="
                background: {PALETTE['white']};
                border: 1px solid {PALETTE['border']};
                border-left: 4px solid {direction_color};
                border-radius: 8px;
                padding: 1rem 1.25rem;
                box-shadow: 0 1px 4px rgba(11,45,78,0.06);
            ">
                <div style="font-size:0.72rem; font-weight:600; text-transform:uppercase;
                            letter-spacing:0.07em; color:{PALETTE['text_light']}; margin-bottom:0.3rem;">
                    Near-Term Direction
                </div>
                <div style="font-size:1.2rem; font-weight:700; color:{direction_color};">
                    {direction_label}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Chart
    fig = go.Figure()
    fig.add_trace(
        forecast_band_trace(df_plot["date"], df_plot[lower_col], df_plot[upper_col])
    )
    fig.add_trace(
        line_trace(df_plot["date"], df_plot[forecast_col],
                   name=label, color=FORECAST_COLOR,
                   width=2.5, show_markers=True)
    )
    fig.update_layout(**plotly_layout(
        f"{label} — Short-Term Hiring Demand Forecast",
        x_label="", y_label="Forecast Level"
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.write(
        f"The latest forecast for **{label}** is **{latest_fc:.2f}** in "
        f"**{latest_date.strftime('%b %Y')}**. The shaded band represents the forecast "
        "confidence interval — a wider band indicates more uncertainty in the projection."
    )

    # Table
    display_df = df_plot.rename(columns={
        forecast_col: "Forecast",
        lower_col:    "Lower Bound",
        upper_col:    "Upper Bound",
    })[["date", "Forecast", "Lower Bound", "Upper Bound"]].reset_index(drop=True)
    display_df["date"] = display_df["date"].dt.strftime("%b %Y")
    display_df = display_df.rename(columns={"date": "Period"})
    st.dataframe(display_df, use_container_width=True)

    # Download
    csv_data  = display_df.to_csv(index=False).encode("utf-8")
    safe_name = label.lower().replace(" ", "_")
    st.download_button(
        label="Download forecast data as CSV",
        data=csv_data,
        file_name=f"{safe_name}_forecast.csv",
        mime="text/csv",
    )


# ── National ──────────────────────────────────────────────────────────────────
if forecast_type == "National":
    section_header("National Forecast", "projected aggregate hiring demand for New Zealand")
    render_forecast(
        df_totals.copy(), "National",
        "forecast", "lower_bound", "upper_bound"
    )
    takeaway_card(
        "Short-term national forecast signals can help decision-makers see whether "
        "aggregate hiring demand is stable, strengthening, or softening in the near term — "
        "before those shifts show up in official employment statistics."
    )

# ── Industry ──────────────────────────────────────────────────────────────────
elif forecast_type == "Industry":
    industry_options = {
        "IT":           ("it_forecast",           "it_lower",           "it_upper"),
        "Health Care":  ("health_care_forecast",  "health_care_lower",  "health_care_upper"),
        "Construction": ("construction_forecast", "construction_lower", "construction_upper"),
        "Education":    ("education_forecast",    "education_lower",    "education_upper"),
        "Hospitality":  ("hospitality_forecast",  "hospitality_lower",  "hospitality_upper"),
        "Sales":        ("sales_forecast",        "sales_lower",        "sales_upper"),
    }

    with st.container():
        st.markdown('<div class="nz-controls-panel">', unsafe_allow_html=True)
        selected_industry = st.selectbox("Select sector", list(industry_options.keys()))
        st.markdown("</div>", unsafe_allow_html=True)

    forecast_col, lower_col, upper_col = industry_options[selected_industry]
    section_header(f"{selected_industry} Forecast",
                   "projected hiring demand — sector level")
    render_forecast(
        df_industries[["date", forecast_col, lower_col, upper_col]].copy(),
        selected_industry, forecast_col, lower_col, upper_col
    )
    takeaway_card(
        f"Sector-level forecasts highlight whether **{selected_industry}** hiring "
        "momentum is tracking differently from the national picture — valuable for "
        "sector-specific workforce planning and capacity decisions."
    )

# ── Region ────────────────────────────────────────────────────────────────────
elif forecast_type == "Region":
    region_options = {
        "Auckland":   ("auckland_forecast",   "auckland_lower",   "auckland_upper"),
        "Wellington": ("wellington_forecast", "wellington_lower", "wellington_upper"),
        "Canterbury": ("canterbury_forecast", "canterbury_lower", "canterbury_upper"),
    }

    with st.container():
        st.markdown('<div class="nz-controls-panel">', unsafe_allow_html=True)
        selected_region = st.selectbox("Select region", list(region_options.keys()))
        st.markdown("</div>", unsafe_allow_html=True)

    forecast_col, lower_col, upper_col = region_options[selected_region]
    section_header(f"{selected_region} Forecast",
                   "projected hiring demand — regional level")
    render_forecast(
        df_regions[["date", forecast_col, lower_col, upper_col]].copy(),
        selected_region, forecast_col, lower_col, upper_col
    )
    takeaway_card(
        f"Regional forecast signals show whether **{selected_region}** hiring demand "
        "is tracking above or below the national trend — important for location-specific "
        "workforce and resource planning."
    )

# ── Guidance ──────────────────────────────────────────────────────────────────
section_header("Reading These Forecasts")

col1, col2, col3 = st.columns(3)
with col1:
    info_card(
        "Forecast Line",
        "The central line shows the model's best estimate of hiring demand for "
        "each projected period.",
        "📈"
    )
with col2:
    info_card(
        "Confidence Band",
        "The shaded area represents forecast uncertainty. A wider band means more "
        "variability in the projection — treat it as a range, not a single point.",
        "🎯"
    )
with col3:
    info_card(
        "Horizon",
        "These are short-term projections (3–6 months). They reflect near-term "
        "momentum, not long-run structural forecasts.",
        "📅"
    )
