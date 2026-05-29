import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="NZ Labour Demand Trends", layout="wide")

from utils.theme import (
    inject_css, section_header, takeaway_card,
    plotly_layout, line_trace, bar_trace,
    CHART_COLORS, HISTORICAL_COLOR, PALETTE,
)

inject_css()

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("NZ Labour Demand Trends")
st.write(
    "The national Jobs Online series captures how online hiring demand has moved over time "
    "in New Zealand. This page covers the long-run trend, year-on-year changes, and the "
    "contrast between skilled and unskilled demand."
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

date_col     = "date"
total_col    = "totals"
skilled_col  = "skilledindex"
unskilled_col = "unskilledindex"

required_cols = [date_col, total_col, skilled_col, unskilled_col]
missing_cols  = [c for c in required_cols if c not in df.columns]
if missing_cols:
    st.error(f"Missing required columns: {missing_cols}")
    st.stop()

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df = df.dropna(subset=[date_col]).sort_values(date_col).reset_index(drop=True)

# ── Controls ──────────────────────────────────────────────────────────────────
section_header("Chart Controls")

with st.container():
    st.markdown('<div class="nz-controls-panel">', unsafe_allow_html=True)
    min_date = df[date_col].min().date()
    max_date = df[date_col].max().date()

    col_a, col_b = st.columns([3, 1])
    with col_a:
        date_range = st.slider(
            "Date range",
            min_value=min_date, max_value=max_date,
            value=(min_date, max_date)
        )
    with col_b:
        skill_view = st.radio(
            "Skill view",
            ["Both", "Skilled only", "Unskilled only"],
        )
    st.markdown("</div>", unsafe_allow_html=True)

start_date, end_date = date_range
df_filtered = df[
    (df[date_col].dt.date >= start_date) &
    (df[date_col].dt.date <= end_date)
].copy()

if df_filtered.empty:
    st.warning("No data available for the selected date range.")
    st.stop()

# ── Summary metrics ───────────────────────────────────────────────────────────
section_header("Period Summary", f"{start_date.strftime('%d %b %Y')} → {end_date.strftime('%d %b %Y')}")

latest_value  = df_filtered[total_col].dropna().iloc[-1]
peak_value    = df_filtered[total_col].max()
trough_value  = df_filtered[total_col].min()
peak_date     = df_filtered.loc[df_filtered[total_col].idxmax(), date_col]
trough_date   = df_filtered.loc[df_filtered[total_col].idxmin(), date_col]
latest_date   = df_filtered[date_col].dropna().iloc[-1]
long_run_avg  = df_filtered[total_col].mean()
latest_delta  = (
    latest_value - df_filtered[total_col].dropna().iloc[-2]
    if len(df_filtered[total_col].dropna()) >= 2 else 0.0
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Current Demand", f"{latest_value:.1f}",
              f"{latest_delta:+.1f} vs prior month")
with col2:
    st.metric("Period Peak", f"{peak_value:.1f}",
              peak_date.strftime("%b %Y"))
with col3:
    st.metric("Period Trough", f"{trough_value:.1f}",
              trough_date.strftime("%b %Y"))
with col4:
    vs_avg = latest_value - long_run_avg
    st.metric("vs Period Average", f"{long_run_avg:.1f}",
              f"{vs_avg:+.1f}")

# ── Overall trend chart ───────────────────────────────────────────────────────
section_header("Overall Hiring Demand Trend")

fig1 = go.Figure()
fig1.add_trace(
    line_trace(df_filtered[date_col], df_filtered[total_col],
               "Hiring Demand Index", color=HISTORICAL_COLOR, width=2)
)
# Add a mean reference line
fig1.add_hline(
    y=long_run_avg,
    line_dash="dot", line_color=PALETTE["text_light"], line_width=1,
    annotation_text=f"Period avg: {long_run_avg:.1f}",
    annotation_position="bottom right",
    annotation_font=dict(size=10, color=PALETTE["text_light"]),
)
fig1.update_layout(**plotly_layout(
    "Overall NZ Hiring Demand Trend",
    x_label="", y_label="Hiring Demand Index"
))
st.plotly_chart(fig1, use_container_width=True)

st.write(
    "The overall Jobs Online series shows that NZ labour demand has not been stable over "
    "time. The series moves through identifiable periods of contraction and recovery, "
    "suggesting hiring activity responds to broader economic and labour market conditions."
)

with st.expander("View raw data"):
    st.dataframe(
        df_filtered[[date_col, total_col]].rename(columns={date_col: "Date", total_col: "Hiring Demand Index"}),
        use_container_width=True
    )

# ── Annual change chart ───────────────────────────────────────────────────────
section_header("Year-on-Year Change", "average annual hiring demand, percentage change")

annual_df  = df_filtered.copy()
annual_df["year"] = annual_df[date_col].dt.year
annual_avg = annual_df.groupby("year")[total_col].mean().reset_index()
annual_avg["pct_change"] = annual_avg[total_col].pct_change() * 100
annual_avg = annual_avg.dropna(subset=["pct_change"])

colors = [
    PALETTE["sage_green"] if v >= 0 else PALETTE["danger"]
    for v in annual_avg["pct_change"]
]

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=annual_avg["year"].astype(str),
    y=annual_avg["pct_change"],
    marker=dict(color=colors, line=dict(width=0)),
    hovertemplate="<b>%{x}</b>: %{y:.1f}%<extra></extra>",
    name="Annual Change (%)",
))
fig2.add_hline(y=0, line_color=PALETTE["border"], line_width=1)
fig2.update_layout(**plotly_layout(
    "Annual Percentage Change in Hiring Demand",
    x_label="Year", y_label="Year-on-Year Change (%)"
))
st.plotly_chart(fig2, use_container_width=True)

st.write(
    "Annual changes highlight that hiring growth has not followed a uniform path. "
    "Positive years (green) signal recovery phases; negative years (red) capture "
    "contractions. The magnitude of these swings reflects the sensitivity of the "
    "NZ labour market to economic cycles."
)

# ── Skilled vs Unskilled chart ────────────────────────────────────────────────
section_header("Skilled vs Unskilled Demand", "comparing hiring demand by skill segment")

fig3 = go.Figure()

if skill_view in ["Both", "Skilled only"]:
    fig3.add_trace(
        line_trace(df_filtered[date_col], df_filtered[skilled_col],
                   "Skilled", color=CHART_COLORS[0], width=2)
    )

if skill_view in ["Both", "Unskilled only"]:
    fig3.add_trace(
        line_trace(df_filtered[date_col], df_filtered[unskilled_col],
                   "Unskilled", color=CHART_COLORS[1], width=2)
    )

fig3.update_layout(**plotly_layout(
    "Skilled vs Unskilled Hiring Demand",
    x_label="", y_label="Hiring Demand Index"
))
st.plotly_chart(fig3, use_container_width=True)

st.write(
    "The comparison between skill segments shows that labour demand does not affect all "
    "parts of the workforce equally. Divergence between skilled and unskilled demand "
    "reflects structural differences across sectors and the composition of hiring activity "
    "at any given point."
)

# ── Key Takeaway ──────────────────────────────────────────────────────────────
takeaway_card(
    f"The latest national hiring demand reading is <strong>{latest_value:.1f}</strong> "
    f"({latest_date.strftime('%b %Y')}), which is "
    f"{'above' if latest_value > long_run_avg else 'below'} the period average of "
    f"<strong>{long_run_avg:.1f}</strong>. NZ hiring demand has moved through clear cycles "
    "of decline and recovery — making short-term monitoring important for workforce "
    "planning and market timing."
)

# ── Download ──────────────────────────────────────────────────────────────────
section_header("Export")

download_df = df_filtered[[date_col, total_col, skilled_col, unskilled_col]].copy()
st.download_button(
    label="Download filtered data as CSV",
    data=download_df.to_csv(index=False).encode("utf-8"),
    file_name="nz_labour_demand_trends_filtered.csv",
    mime="text/csv",
)
