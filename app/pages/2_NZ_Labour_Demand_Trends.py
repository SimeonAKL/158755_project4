import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="NZ Labour Demand Trends", layout="wide")

from utils.theme import (
    inject_css, page_hero, section_header, takeaway_card,
    plotly_layout, line_trace,
    CHART_COLORS, HISTORICAL_COLOR, PALETTE,
)

inject_css()
C = PALETTE

page_hero(
    title="NZ Labour Demand Trends",
    subtitle=(
        "The national Jobs Online series — long-run trend, year-on-year changes, "
        "and the contrast between skilled and unskilled hiring demand."
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

date_col, total_col = "date", "totals"
skilled_col, unskilled_col = "skilledindex", "unskilledindex"

required = [date_col, total_col, skilled_col, unskilled_col]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Missing required columns: {missing}")
    st.stop()

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df = df.dropna(subset=[date_col]).sort_values(date_col).reset_index(drop=True)

# ── Controls ──────────────────────────────────────────────────────────────────
section_header("Chart Controls")

with st.container(border=True):
    min_date = df[date_col].min().date()
    max_date = df[date_col].max().date()

    date_range = st.slider(
        "Date range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
    )

start_date, end_date = date_range

df_f = df[
    (df[date_col].dt.date >= start_date) &
    (df[date_col].dt.date <= end_date)
].copy()

if df_f.empty:
    st.warning("No data available for the selected date range.")
    st.stop()

latest_val = df_f[total_col].dropna().iloc[-1]
peak_val = df_f[total_col].max()
trough_val = df_f[total_col].min()
peak_dt = df_f.loc[df_f[total_col].idxmax(), date_col]
trough_dt = df_f.loc[df_f[total_col].idxmin(), date_col]
latest_dt = df_f[date_col].dropna().iloc[-1]
avg_val = df_f[total_col].mean()

delta = (
    latest_val - df_f[total_col].dropna().iloc[-2]
    if len(df_f[total_col].dropna()) >= 2 else 0.0
)

section_header(
    "Period Summary",
    f"{start_date.strftime('%d %b %Y')} → {end_date.strftime('%d %b %Y')}"
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Current Demand",
        f"{latest_val:.1f}",
        f"{delta:+.1f} vs prior month"
    )

with c2:
    st.metric(
        "Period Peak",
        f"{peak_val:.1f}",
        peak_dt.strftime("%b %Y")
    )

with c3:
    st.metric(
        "Period Trough",
        f"{trough_val:.1f}",
        trough_dt.strftime("%b %Y")
    )

with c4:
    st.metric(
        "vs Period Average",
        f"{avg_val:.1f}",
        f"{latest_val - avg_val:+.1f}"
    )

# ── Overall trend ─────────────────────────────────────────────────────────────
section_header("Overall Hiring Demand Trend")

fig1 = go.Figure()

fig1.add_trace(
    line_trace(
        df_f[date_col],
        df_f[total_col],
        "Hiring Demand Index",
        color=HISTORICAL_COLOR,
        width=2,
    )
)

fig1.add_hline(
    y=avg_val,
    line_dash="dot",
    line_color=C["border"],
    line_width=1.5,
    annotation_text=f"Period avg: {avg_val:.1f}",
    annotation_position="bottom right",
    annotation_font=dict(size=10, color=C["text_secondary"]),
)

fig1.update_layout(
    **plotly_layout(
        "Overall NZ Hiring Demand Trend",
        x_label="",
        y_label="Hiring Demand Index",
    )
)

st.plotly_chart(fig1, use_container_width=True)

st.write(
    "The overall Jobs Online series shows that NZ labour demand has not been stable "
    "over time. The series moves through identifiable periods of contraction and "
    "recovery, suggesting hiring activity responds to broader economic conditions."
)

with st.expander("View raw data"):
    st.dataframe(
        df_f[[date_col, total_col]]
        .rename(columns={date_col: "Date", total_col: "Hiring Demand Index"}),
        use_container_width=True,
    )

# ── Annual change ─────────────────────────────────────────────────────────────
section_header("Year-on-Year Change", "average annual hiring demand, percentage change")

ann = df_f.copy()
ann["year"] = ann[date_col].dt.year

ann_avg = ann.groupby("year")[total_col].mean().reset_index()
ann_avg["pct"] = ann_avg[total_col].pct_change() * 100
ann_avg = ann_avg.dropna(subset=["pct"])

bar_colors = [C["positive"] if v >= 0 else C["negative"] for v in ann_avg["pct"]]

fig2 = go.Figure()

fig2.add_trace(
    go.Bar(
        x=ann_avg["year"].astype(str),
        y=ann_avg["pct"],
        marker=dict(color=bar_colors, line=dict(width=0)),
        hovertemplate="<b>%{x}</b>: %{y:.1f}%<extra></extra>",
        name="Annual Change (%)",
    )
)

fig2.add_hline(
    y=0,
    line_color=C["border"],
    line_width=1,
)

fig2.update_layout(
    **plotly_layout(
        "Annual Percentage Change in Hiring Demand",
        x_label="Year",
        y_label="Year-on-Year Change (%)",
    )
)

st.plotly_chart(fig2, use_container_width=True)

st.write(
    "Annual changes highlight that hiring growth has not followed a uniform path. "
    "Positive years signal recovery phases; negative years capture contractions."
)

# ── Skilled vs Unskilled ──────────────────────────────────────────────────────
section_header("Skilled vs Unskilled Demand", "comparing hiring demand by skill segment")

with st.container(border=True):
    skill_view = st.radio(
        "Skill view",
        ["Both", "Skilled only", "Unskilled only"],
        horizontal=True,
    )

fig3 = go.Figure()

if skill_view in ["Both", "Skilled only"]:
    fig3.add_trace(
        line_trace(
            df_f[date_col],
            df_f[skilled_col],
            "Skilled",
            color=CHART_COLORS[0],
            width=2,
        )
    )

if skill_view in ["Both", "Unskilled only"]:
    fig3.add_trace(
        line_trace(
            df_f[date_col],
            df_f[unskilled_col],
            "Unskilled",
            color=CHART_COLORS[1],
            width=2,
        )
    )

fig3.update_layout(
    **plotly_layout(
        "Skilled vs Unskilled Hiring Demand",
        x_label="",
        y_label="Hiring Demand Index",
    )
)

st.plotly_chart(fig3, use_container_width=True)

st.write(
    "The comparison between skill segments shows that labour demand does not affect "
    "all parts of the workforce equally. Divergence between skilled and unskilled "
    "demand reflects structural differences across sectors."
)

takeaway_card(
    f"The latest national hiring demand reading is <strong>{latest_val:.1f}</strong> "
    f"({latest_dt.strftime('%b %Y')}), which is "
    f"{'above' if latest_val > avg_val else 'below'} the period average of "
    f"<strong>{avg_val:.1f}</strong>. NZ hiring demand has moved through clear cycles "
    "of decline and recovery — making short-term monitoring important for workforce "
    "planning and market timing."
)

# ── Export ────────────────────────────────────────────────────────────────────
section_header("Export")

st.download_button(
    label="Download filtered data as CSV",
    data=df_f[[date_col, total_col, skilled_col, unskilled_col]]
    .to_csv(index=False)
    .encode("utf-8"),
    file_name="nz_labour_demand_trends_filtered.csv",
    mime="text/csv",
)