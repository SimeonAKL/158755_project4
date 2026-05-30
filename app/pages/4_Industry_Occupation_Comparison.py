import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Industry & Occupation Comparison", layout="wide")

from utils.theme import (
    inject_css, page_hero, section_header, takeaway_card,
    plotly_layout, line_trace,
    CHART_COLORS, PALETTE,
)

inject_css()
C = PALETTE

page_hero(
    title="Industry & Occupation Comparison",
    subtitle=(
        "Identifying which industries and occupations are seeing the strongest or "
        "weakest hiring demand — a more targeted view than national averages alone."
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

date_col = "date"
if date_col not in df.columns:
    st.error("The required 'date' column was not found.")
    st.stop()

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df = df.sort_values(date_col).reset_index(drop=True)

industry_options = {
    "Business Services":"business_services", "Construction":"construction",
    "Education":"education", "Health Care":"health_care", "Hospitality":"hospitality",
    "IT":"it", "Manufacturing":"manufacturing", "Primary":"primary",
    "Sales":"sales", "Other":"other",
}
occupation_options = {
    "Managers":"managers", "Professionals":"professionals",
    "Technicians & Trades":"technicians_and_trades_workers",
    "Community & Personal Services":"community_and_personal_service_workers",
    "Clerical & Admin":"clerical_and_administrative_workers",
    "Sales Workers":"sales_workers",
    "Machinery Operators & Drivers":"machinery_operators_and_drivers",
    "Labourers":"labourers",
}

section_header("Chart Controls")
with st.container(border=True):
    ca, cb = st.columns([1, 2])
    with ca:
        comparison_type = st.selectbox("Comparison type", ["Industry", "Occupation"])

    options_dict     = industry_options if comparison_type == "Industry" else occupation_options
    available_labels = [lbl for lbl, col in options_dict.items() if col in df.columns]

    if not available_labels:
        st.error(f"No columns found for {comparison_type.lower()} comparison.")
        st.stop()

    with cb:
        default_sel     = available_labels[:3] if len(available_labels) >= 3 else available_labels
        selected_labels = st.multiselect(
            f"Select {comparison_type.lower()} groups",
            options=available_labels, default=default_sel,
        )

    min_date = df[date_col].min().date()
    max_date = df[date_col].max().date()
    date_range = st.slider("Date range", min_value=min_date, max_value=max_date,
                           value=(min_date, max_date))

if not selected_labels:
    st.warning("Please select at least one category.")
    st.stop()

start_date, end_date = date_range
selected_cols = [options_dict[lbl] for lbl in selected_labels]
df_plot = df[
    (df[date_col].dt.date >= start_date) &
    (df[date_col].dt.date <= end_date)
][[date_col] + selected_cols].copy()

# ── Trend chart ───────────────────────────────────────────────────────────────
section_header(f"{comparison_type} Demand Trends",
               f"{start_date.strftime('%b %Y')} → {end_date.strftime('%b %Y')}")

fig1 = go.Figure()
for i, label in enumerate(selected_labels):
    fig1.add_trace(
        line_trace(df_plot[date_col], df_plot[options_dict[label]],
                   name=label, color=CHART_COLORS[i % len(CHART_COLORS)], width=2)
    )
fig1.update_layout(**plotly_layout(
    f"{comparison_type} Hiring Demand Trends", x_label="", y_label="Hiring Demand Index"))
st.plotly_chart(fig1, use_container_width=True)

st.write(
    "Industry-level trends show that hiring demand has not moved uniformly across "
    "sectors. Some industries appear more resilient or recover more quickly, while "
    "others show weaker or less stable activity."
    if comparison_type == "Industry" else
    "Occupation-level patterns show that demand differs meaningfully across job "
    "groups. Some occupations maintain stronger demand over time, while others "
    "show greater sensitivity to economic cycles."
)

# ── Snapshot horizontal bar ───────────────────────────────────────────────────
latest_row  = df_plot.dropna(subset=[date_col]).iloc[-1]
latest_date = latest_row[date_col]

section_header(f"Current {comparison_type} Standing",
               f"latest reading — {latest_date.strftime('%b %Y')}")

latest_vals = {lbl: latest_row[options_dict[lbl]] for lbl in selected_labels}
lat_df = (
    pd.DataFrame({"Group": list(latest_vals.keys()),
                  "Hiring Demand Index": list(latest_vals.values())})
    .sort_values("Hiring Demand Index", ascending=True)
)

fig2 = go.Figure(go.Bar(
    x=lat_df["Hiring Demand Index"], y=lat_df["Group"], orientation="h",
    marker=dict(
        color=[CHART_COLORS[i % len(CHART_COLORS)] for i in range(len(lat_df))],
        line=dict(width=0),
    ),
    hovertemplate="<b>%{y}</b>: %{x:.1f}<extra></extra>",
))
layout = plotly_layout(
    f"{comparison_type} Hiring Demand — {latest_date.strftime('%b %Y')}",
    x_label="Hiring Demand Index", y_label="",
    legend=False, height=max(300, 60 * len(lat_df)),
)
layout["xaxis"]["showgrid"] = True
layout["xaxis"]["gridcolor"] = C["border_light"]
layout["yaxis"]["showgrid"]  = False
layout["yaxis"]["showline"]  = False
fig2.update_layout(**layout)
st.plotly_chart(fig2, use_container_width=True)

section_header(f"{comparison_type} Rankings")
rank_df = lat_df.sort_values("Hiring Demand Index", ascending=False).reset_index(drop=True)
rank_df.index += 1
rank_df["Hiring Demand Index"] = rank_df["Hiring Demand Index"].round(1)
st.dataframe(rank_df.rename(columns={"Group": comparison_type}), use_container_width=True)

section_header("Period Summary")
top    = rank_df.iloc[0]
bottom = rank_df.iloc[-1]
c1, c2, c3 = st.columns(3)
with c1: st.metric(f"Leading {comparison_type}", top["Group"],    f"{top['Hiring Demand Index']:.1f}")
with c2: st.metric(f"Weakest {comparison_type}", bottom["Group"], f"{bottom['Hiring Demand Index']:.1f}")
with c3: st.metric("Demand Spread", f"{top['Hiring Demand Index'] - bottom['Hiring Demand Index']:.1f}")

st.write(
    f"In **{latest_date.strftime('%b %Y')}**, the highest hiring demand among selected "
    f"{comparison_type.lower()} groups is **{top['Group']}** at "
    f"**{top['Hiring Demand Index']:.1f}**, while the lowest is **{bottom['Group']}** "
    f"at **{bottom['Hiring Demand Index']:.1f}**."
)

takeaway_card(
    "Hiring demand is moving unevenly across sectors and occupations. "
    "Better decisions come from understanding where demand is actually concentrated "
    "rather than relying on national averages alone."
)

with st.expander("View filtered data"):
    st.dataframe(
        df_plot.rename(
            columns={**{date_col: "Date"}, **{options_dict[lbl]: lbl for lbl in selected_labels}}
        ).head(20),
        use_container_width=True
    )