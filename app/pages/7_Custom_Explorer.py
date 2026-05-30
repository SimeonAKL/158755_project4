import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Custom Explorer", layout="wide")

from utils.theme import (
    inject_css, page_hero, section_header, info_card, takeaway_card,
    plotly_layout, line_trace,
    CHART_COLORS, PALETTE,
)

inject_css()
C = PALETTE

page_hero(
    title="Custom Explorer",
    subtitle=(
        "A flexible workspace for exploring hiring demand across any combination "
        "of regions, industries, occupations, and skill groups."
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

GROUP_MAP = {
    "Region": {
        "Auckland":"auckland", "Wellington":"wellington",
        "North Island Other":"north_island_other",
        "Canterbury":"canterbury", "South Island Other":"south_island_other",
    },
    "Industry": {
        "Business Services":"business_services", "Construction":"construction",
        "Education":"education", "Health Care":"health_care", "Hospitality":"hospitality",
        "IT":"it", "Manufacturing":"manufacturing", "Primary":"primary",
        "Sales":"sales", "Other":"other",
    },
    "Occupation": {
        "Managers":"managers", "Professionals":"professionals",
        "Technicians & Trades":"technicians_and_trades_workers",
        "Community & Personal Services":"community_and_personal_service_workers",
        "Clerical & Admin":"clerical_and_administrative_workers",
        "Sales Workers":"sales_workers",
        "Machinery Operators & Drivers":"machinery_operators_and_drivers",
        "Labourers":"labourers",
    },
    "Skill Group": {
        "Highly Skilled":"highly_skilled", "Skilled":"skilled",
        "Semi-Skilled":"semi_skilled", "Low-Skilled":"low_skilled",
        "Unskilled":"unskilled",
    },
}

section_header("Explorer Controls")
with st.container(border=True):
    ca, cb = st.columns([1, 2])
    with ca:
        series_group = st.selectbox("Data group", list(GROUP_MAP.keys()))
    opts     = GROUP_MAP[series_group]
    avail    = [lbl for lbl, col in opts.items() if col in df.columns]
    with cb:
        sel_lbls = st.multiselect(
            f"Select {series_group.lower()} series",
            avail, default=avail[:2] if len(avail) >= 2 else avail,
        )
    cc, cd = st.columns([3, 1])
    with cc:
        min_date   = df[date_col].min().date()
        max_date   = df[date_col].max().date()
        date_range = st.slider("Date range", min_value=min_date, max_value=max_date,
                               value=(min_date, max_date))
    with cd:
        normalize = st.checkbox("Index to 100",
                                help="Rebase all series to 100 at the start of the selected period.")

if not sel_lbls:
    st.warning("Please select at least one series.")
    st.stop()

start_date, end_date = date_range
sel_cols = [opts[lbl] for lbl in sel_lbls]
df_plot  = df[
    (df[date_col].dt.date >= start_date) &
    (df[date_col].dt.date <= end_date)
][[date_col] + sel_cols].dropna().copy()

if df_plot.empty:
    st.warning("No data available for the selected combination.")
    st.stop()

plot_df = df_plot.copy()
if normalize:
    for col in sel_cols:
        base = plot_df[col].iloc[0]
        if base != 0:
            plot_df[col] = plot_df[col] / base * 100

y_label = "Index (base = 100)" if normalize else "Hiring Demand Index"
section_header(f"{series_group} Demand Trend",
               f"{start_date.strftime('%b %Y')} → {end_date.strftime('%b %Y')}"
               + (" · indexed to 100" if normalize else ""))

fig = go.Figure()
for i, lbl in enumerate(sel_lbls):
    fig.add_trace(
        line_trace(plot_df[date_col], plot_df[opts[lbl]],
                   name=lbl, color=CHART_COLORS[i % len(CHART_COLORS)], width=2)
    )
if normalize:
    fig.add_hline(y=100, line_dash="dot", line_color=C["border"], line_width=1.5,
                  annotation_text="Base = 100", annotation_position="top left",
                  annotation_font=dict(size=10, color=C["text_secondary"]))

fig.update_layout(**plotly_layout(
    f"{series_group} Hiring Demand — Selected Series",
    x_label="", y_label=y_label))
st.plotly_chart(fig, use_container_width=True)

st.write(
    "The index view rebases each series to 100 at the start of the selected period, "
    "allowing proportional comparisons across groups with different absolute scales."
    if normalize else
    "This view shows actual hiring demand index levels for each selected series, "
    "making it easy to compare current magnitudes directly."
)

section_header("Series Summary", "key statistics over the selected period")
summary_rows = []
for lbl in sel_lbls:
    col = opts[lbl]
    s   = df_plot[col]
    summary_rows.append({
        "Series": lbl, "Latest": round(s.iloc[-1], 1),
        "Average": round(s.mean(), 1), "High": round(s.max(), 1),
        "Low": round(s.min(), 1), "Range": round(s.max() - s.min(), 1),
    })
st.dataframe(pd.DataFrame(summary_rows).set_index("Series"), use_container_width=True)

section_header("Underlying Data")
disp_df = df_plot.rename(
    columns={**{date_col: "Date"}, **{opts[lbl]: lbl for lbl in sel_lbls}}
).reset_index(drop=True)
st.dataframe(disp_df, use_container_width=True)

st.download_button(
    label="Download selected data as CSV",
    data=disp_df.to_csv(index=False).encode("utf-8"),
    file_name="custom_explorer_selection.csv",
    mime="text/csv",
)

takeaway_card(
    "Interactive exploration makes it easier to identify where hiring demand matters "
    "most for a specific region, sector, occupation, or skill group — supporting "
    "more targeted and evidence-based workforce decisions."
)

section_header("Tips for Effective Exploration")
c1, c2, c3 = st.columns(3)
with c1:
    info_card("Relative Comparisons",
              "Use 'Index to 100' when comparing groups with very different absolute "
              "levels. It reveals which series have grown faster, not just which is larger.", "📐")
with c2:
    info_card("Narrow the Date Range",
              "Zooming into a specific period (e.g. the post-COVID recovery) can reveal "
              "patterns that are masked in the full history view.", "🔍")
with c3:
    info_card("Compare Across Groups",
              "Try running the same date range across different group types to build a "
              "multi-dimensional picture of where demand is moving.", "🔄")