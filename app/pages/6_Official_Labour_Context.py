import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Official Labour Context", layout="wide")

from utils.theme import (
    inject_css, section_header, info_card, takeaway_card,
    plotly_layout, line_trace,
    CHART_COLORS, HISTORICAL_COLOR, PALETTE,
)

inject_css()

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("Official Labour Context")
st.write(
    "Jobs Online data captures changes in hiring advertising — but the broader labour "
    "market picture requires official data. This page places vacancy trends alongside "
    "Stats NZ indicators to help judge whether demand signals are supported by wider "
    "employment conditions."
)

# ── Data ──────────────────────────────────────────────────────────────────────
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

def find_first_match(columns, candidates):
    for c in candidates:
        if c in columns:
            return c
    return None

def get_numeric_columns(df):
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

jobs_date_col     = find_first_match(df_jobs.columns,     ["date", "month", "Date"])
monthly_date_col  = find_first_match(df_monthly.columns,  ["date", "month", "Date"])
quarterly_date_col = find_first_match(df_quarterly.columns, ["date", "quarter", "Date"])

df_jobs[jobs_date_col]         = pd.to_datetime(df_jobs[jobs_date_col], errors="coerce")
df_monthly[monthly_date_col]   = pd.to_datetime(df_monthly[monthly_date_col], errors="coerce")
df_quarterly[quarterly_date_col] = pd.to_datetime(df_quarterly[quarterly_date_col], errors="coerce")

jobs_total_col = "totals"

indicator_labels = {
    "male_paid_employee":   "Male Paid Employment",
    "female_paid_employee": "Female Paid Employment",
    "unemployment_rate":    "Unemployment Rate",
    "underutilisation_rate": "Underutilisation Rate",
    "filled_jobs":          "Filled Jobs",
    "employment_total":     "Total Employment",
}

# ── Controls ──────────────────────────────────────────────────────────────────
section_header("Indicator Selection")

with st.container():
    st.markdown('<div class="nz-controls-panel">', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        source_type = st.selectbox(
            "Official data frequency",
            ["Monthly Indicators", "Quarterly Indicators"]
        )
    with col_b:
        if source_type == "Monthly Indicators":
            df_context      = df_monthly.copy()
            context_date_col = monthly_date_col
        else:
            df_context      = df_quarterly.copy()
            context_date_col = quarterly_date_col

        numeric_cols = get_numeric_columns(df_context)
        display_to_actual = {
            indicator_labels.get(col, col.replace("_", " ").title()): col
            for col in numeric_cols
        }

        preferred = ["Unemployment Rate", "Underutilisation Rate",
                     "Male Paid Employment", "Female Paid Employment", "Filled Jobs"]
        ordered   = [n for n in preferred if n in display_to_actual] + \
                    [n for n in display_to_actual if n not in preferred]

        selected_display   = st.selectbox("Select official indicator", ordered)
        selected_indicator = display_to_actual[selected_display]

    st.markdown("</div>", unsafe_allow_html=True)

# ── Official indicator chart ──────────────────────────────────────────────────
section_header(f"{selected_display}", "Stats NZ official labour market series")

df_indicator = (
    df_context[[context_date_col, selected_indicator]]
    .dropna().sort_values(context_date_col)
)

fig1 = go.Figure()
fig1.add_trace(
    line_trace(df_indicator[context_date_col], df_indicator[selected_indicator],
               name=selected_display,
               color=CHART_COLORS[1], width=2, show_markers=True)
)
fig1.update_layout(**plotly_layout(
    f"{selected_display} Over Time",
    x_label="", y_label=selected_display
))
st.plotly_chart(fig1, use_container_width=True)

latest_value = df_indicator[selected_indicator].iloc[-1]
latest_date  = df_indicator[context_date_col].iloc[-1]

st.write(
    f"The latest available reading for **{selected_display}** is "
    f"**{latest_value:.2f}** in **{latest_date.strftime('%b %Y')}**."
)

# ── Dual-axis comparison ──────────────────────────────────────────────────────
section_header(
    "Demand vs Official Context",
    "Jobs Online hiring demand alongside the selected official indicator"
)

df_jobs_plot    = df_jobs[[jobs_date_col, jobs_total_col]].dropna().sort_values(jobs_date_col)
df_context_plot = df_context[[context_date_col, selected_indicator]].dropna().sort_values(context_date_col)

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=df_jobs_plot[jobs_date_col],
    y=df_jobs_plot[jobs_total_col],
    name="Jobs Online Hiring Demand",
    mode="lines",
    line=dict(color=HISTORICAL_COLOR, width=2),
    hovertemplate="<b>Hiring Demand</b>: %{y:.1f}<extra></extra>",
    yaxis="y1",
))

fig2.add_trace(go.Scatter(
    x=df_context_plot[context_date_col],
    y=df_context_plot[selected_indicator],
    name=selected_display,
    mode="lines",
    line=dict(color=CHART_COLORS[1], width=2, dash="dot"),
    hovertemplate=f"<b>{selected_display}</b>: %{{y:.2f}}<extra></extra>",
    yaxis="y2",
))

layout = plotly_layout(
    "Hiring Demand vs Official Labour Market Indicator",
    x_label="", y_label="Hiring Demand Index"
)
layout["yaxis2"] = dict(
    title=dict(text=selected_display,
               font=dict(size=11, color=PALETTE["text_light"])),
    tickfont=dict(size=10, color=PALETTE["text_secondary"]),
    overlaying="y",
    side="right",
    showgrid=False,
    zeroline=False,
)
fig2.update_layout(**layout)
st.plotly_chart(fig2, use_container_width=True)

info_card(
    "How to Read This Chart",
    "The solid line (left axis) shows Jobs Online hiring demand. The dashed line "
    "(right axis) shows the selected official Stats NZ indicator. The two series "
    "are on different scales — look for directional alignment or divergence, "
    "not precise numerical comparisons.",
    "ℹ️"
)

st.write(
    "Official labour market indicators provide broader context for interpreting "
    "Jobs Online. While vacancy data captures changes in job advertising activity, "
    "official indicators reflect wider conditions — employment levels, labour market "
    "slack, and structural shifts — that can help validate or qualify the vacancy signal."
)

# ── Summary table ─────────────────────────────────────────────────────────────
section_header("Latest Values Summary")

latest_jobs_value = df_jobs_plot[jobs_total_col].iloc[-1]
latest_jobs_date  = df_jobs_plot[jobs_date_col].iloc[-1]

summary_df = pd.DataFrame({
    "Series":       ["Jobs Online Hiring Demand", selected_display],
    "Latest Value": [round(latest_jobs_value, 2), round(latest_value, 2)],
    "As of":        [latest_jobs_date.strftime("%b %Y"), latest_date.strftime("%b %Y")],
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
    st.dataframe(df_indicator.rename(
        columns={context_date_col: "Date", selected_indicator: selected_display}
    ).head(20), use_container_width=True)
