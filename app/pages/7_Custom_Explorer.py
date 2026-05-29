import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Custom Explorer", layout="wide")

from utils.theme import (
    inject_css, section_header, info_card, takeaway_card,
    plotly_layout, line_trace,
    CHART_COLORS, PALETTE,
)

inject_css()

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("Custom Explorer")
st.write(
    "A flexible workspace for exploring hiring demand across any combination of "
    "regions, industries, occupations, and skill groups. Use this page to investigate "
    "a specific part of the labour market rather than following a fixed dashboard view."
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

date_col = "date"
if date_col not in df.columns:
    st.error("The required 'date' column was not found.")
    st.stop()

df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
df = df.sort_values(date_col).reset_index(drop=True)

region_options = {
    "Auckland":           "auckland",
    "Wellington":         "wellington",
    "North Island Other": "north_island_other",
    "Canterbury":         "canterbury",
    "South Island Other": "south_island_other",
}

industry_options = {
    "Business Services": "business_services",
    "Construction":      "construction",
    "Education":         "education",
    "Health Care":       "health_care",
    "Hospitality":       "hospitality",
    "IT":                "it",
    "Manufacturing":     "manufacturing",
    "Primary":           "primary",
    "Sales":             "sales",
    "Other":             "other",
}

occupation_options = {
    "Managers":                      "managers",
    "Professionals":                 "professionals",
    "Technicians & Trades":          "technicians_and_trades_workers",
    "Community & Personal Services": "community_and_personal_service_workers",
    "Clerical & Admin":              "clerical_and_administrative_workers",
    "Sales Workers":                 "sales_workers",
    "Machinery Operators & Drivers": "machinery_operators_and_drivers",
    "Labourers":                     "labourers",
}

skill_options = {
    "Highly Skilled": "highly_skilled",
    "Skilled":        "skilled",
    "Semi-Skilled":   "semi_skilled",
    "Low-Skilled":    "low_skilled",
    "Unskilled":      "unskilled",
}

GROUP_MAP = {
    "Region":      region_options,
    "Industry":    industry_options,
    "Occupation":  occupation_options,
    "Skill Group": skill_options,
}

# ── Controls ──────────────────────────────────────────────────────────────────
section_header("Explorer Controls")

with st.container():
    st.markdown('<div class="nz-controls-panel">', unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 2])
    with col_a:
        series_group = st.selectbox("Data group", list(GROUP_MAP.keys()))
    options_dict     = GROUP_MAP[series_group]
    available_labels = [lbl for lbl, col in options_dict.items() if col in df.columns]

    with col_b:
        selected_labels = st.multiselect(
            f"Select {series_group.lower()} series",
            available_labels,
            default=available_labels[:2] if len(available_labels) >= 2 else available_labels,
        )

    col_c, col_d = st.columns([3, 1])
    with col_c:
        min_date   = df[date_col].min().date()
        max_date   = df[date_col].max().date()
        date_range = st.slider(
            "Date range",
            min_value=min_date, max_value=max_date,
            value=(min_date, max_date),
        )
    with col_d:
        normalize = st.checkbox(
            "Index to 100",
            help="Rebase all series to 100 at the start of the selected period for relative comparison."
        )

    st.markdown("</div>", unsafe_allow_html=True)

if not selected_labels:
    st.warning("Please select at least one series.")
    st.stop()

start_date, end_date = date_range
selected_cols = [options_dict[lbl] for lbl in selected_labels]

df_plot = df[
    (df[date_col].dt.date >= start_date) &
    (df[date_col].dt.date <= end_date)
][[date_col] + selected_cols].dropna().copy()

if df_plot.empty:
    st.warning("No data available for the selected combination.")
    st.stop()

plot_df = df_plot.copy()
if normalize:
    for col in selected_cols:
        base = plot_df[col].iloc[0]
        if base != 0:
            plot_df[col] = plot_df[col] / base * 100

# ── Trend chart ───────────────────────────────────────────────────────────────
y_label = "Index (base = 100)" if normalize else "Hiring Demand Index"

section_header(
    f"{series_group} Demand Trend",
    f"{start_date.strftime('%b %Y')} → {end_date.strftime('%b %Y')}"
    + (" · indexed to 100" if normalize else "")
)

fig = go.Figure()
for i, label in enumerate(selected_labels):
    col = options_dict[label]
    fig.add_trace(
        line_trace(plot_df[date_col], plot_df[col],
                   name=label,
                   color=CHART_COLORS[i % len(CHART_COLORS)],
                   width=2)
    )

if normalize:
    fig.add_hline(
        y=100, line_dash="dot",
        line_color=PALETTE["text_light"], line_width=1,
        annotation_text="Base = 100",
        annotation_position="top left",
        annotation_font=dict(size=10, color=PALETTE["text_light"]),
    )

fig.update_layout(**plotly_layout(
    f"{series_group} Hiring Demand — Selected Series",
    x_label="", y_label=y_label
))
st.plotly_chart(fig, use_container_width=True)

if normalize:
    st.write(
        "The index view rebases each series to 100 at the start of the selected period, "
        "allowing proportional comparisons across groups with different absolute scales."
    )
else:
    st.write(
        "This view shows actual hiring demand index levels for each selected series, "
        "making it easy to compare current magnitudes directly."
    )

# ── Summary metrics table ─────────────────────────────────────────────────────
section_header("Series Summary", "key statistics over the selected period")

summary_rows = []
for label in selected_labels:
    col = options_dict[label]
    series = df_plot[col]
    summary_rows.append({
        "Series":        label,
        "Latest Value":  round(series.iloc[-1], 1),
        "Period Average": round(series.mean(), 1),
        "Period High":   round(series.max(), 1),
        "Period Low":    round(series.min(), 1),
        "Range":         round(series.max() - series.min(), 1),
    })

summary_df = pd.DataFrame(summary_rows).set_index("Series")
st.dataframe(summary_df, use_container_width=True)

# ── Data table ────────────────────────────────────────────────────────────────
section_header("Underlying Data")

display_df = df_plot.rename(
    columns={**{date_col: "Date"}, **{options_dict[lbl]: lbl for lbl in selected_labels}}
).reset_index(drop=True)

st.dataframe(display_df, use_container_width=True)

st.download_button(
    label="Download selected data as CSV",
    data=display_df.to_csv(index=False).encode("utf-8"),
    file_name="custom_explorer_selection.csv",
    mime="text/csv",
)

takeaway_card(
    "Interactive exploration makes it easier to identify where hiring demand matters "
    "most for a specific region, sector, occupation, or skill group — "
    "supporting more targeted and evidence-based workforce decisions."
)

# ── Usage tips ────────────────────────────────────────────────────────────────
section_header("Tips for Effective Exploration")

col1, col2, col3 = st.columns(3)
with col1:
    info_card(
        "Relative Comparisons",
        "Use the 'Index to 100' toggle when comparing groups with very different "
        "absolute levels. It reveals which series have grown faster, not just which "
        "is larger in absolute terms.",
        "📐"
    )
with col2:
    info_card(
        "Narrow the Date Range",
        "Zooming into a specific period (e.g. the post-COVID recovery) can reveal "
        "patterns that are masked in the full history view.",
        "🔍"
    )
with col3:
    info_card(
        "Compare Across Groups",
        "Try running the same date range across different group types (e.g. region "
        "then industry) to build a multi-dimensional picture of where demand is moving.",
        "🔄"
    )
