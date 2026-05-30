import streamlit as st

st.set_page_config(page_title="Project Overview", layout="wide")

from utils.theme import (
    inject_css, page_hero, section_header, info_card, takeaway_card, PALETTE,
)

inject_css()

C = PALETTE

page_hero(
    title="Project Overview",
    subtitle=(
        "Background, objectives, research questions, data sources, and analytical "
        "workflow for the NZ Labour Demand Forecaster project."
    ),
)

st.write(
    "This dashboard explores short-term labour demand trends in New Zealand using "
    "Jobs Online data and official labour market indicators from Stats NZ. It covers "
    "how online hiring demand has changed over time, how patterns differ across regions, "
    "industries, and occupations, and whether recent demand trends can support "
    "short-term forecasting over the next 3–6 months."
)

# ── Background ────────────────────────────────────────────────────────────────
section_header("Project Background")

st.write(
    "Changes in online job advertisements reflect shifts in hiring activity, employer "
    "confidence, and sector-level demand. New Zealand labour demand has not moved evenly "
    "over time — periods such as the global financial crisis, COVID-19 disruption, and "
    "the post-pandemic recovery all produced noticeable changes in hiring activity. "
    "Jobs Online data provides a timely, high-frequency lens for tracking these movements."
)
st.write(
    "This project uses the Jobs Online series as its primary data source, with "
    "breakdowns by region, industry, occupation, and skill group. Official Stats NZ "
    "labour market data is incorporated to place vacancy trends in a broader context "
    "and to support interpretation of forecast results."
)

# ── Objectives ────────────────────────────────────────────────────────────────
section_header("Objectives")

col1, col2 = st.columns(2)
with col1:
    info_card("Trend Analysis",
              "Examine how overall online hiring demand has changed over time in New Zealand, "
              "identifying key turning points and structural shifts.", "📈")
    info_card("Forecasting",
              "Develop short-term models to project labour demand over the next 3–6 months "
              "at the national, industry, and regional levels.", "🔭")
with col2:
    info_card("Subgroup Comparisons",
              "Compare demand patterns across regions, industries, occupations, and skill "
              "groups to identify where the market is diverging.", "🗺️")
    info_card("Official Context",
              "Use Stats NZ employment and labour force indicators to strengthen interpretation "
              "and validate the vacancy-based forecast results.", "🏛️")

# ── Research questions ────────────────────────────────────────────────────────
section_header("Research Questions")

questions = [
    ("How has overall online labour demand changed over time in New Zealand?",
     "Addressed through national trend analysis using the full Jobs Online monthly series."),
    ("How do demand patterns differ across regions, industries, and occupations?",
     "Addressed through subgroup comparison and cross-sectional breakdowns."),
    ("Can Jobs Online data forecast labour demand over the next 3–6 months?",
     "Addressed through short-term forecasting models at national, industry, and regional levels."),
    ("How can official data strengthen forecast interpretation and validation?",
     "Addressed by incorporating Stats NZ employment and labour force indicators."),
]

def _render_question(i, q, a):
    st.markdown(
        f"""
        <div style="
            background:{C['card_bg']}; border:1px solid {C['border']};
            border-left:4px solid {C['gold']}; border-radius:6px;
            padding:1.1rem 1.4rem; margin-bottom:0.75rem;
            box-shadow:0 1px 4px rgba(0,59,92,0.05);
        ">
            <div style="font-family:'Inter',sans-serif; font-size:0.66rem;
                font-weight:700; text-transform:uppercase; letter-spacing:0.13em;
                color:{C['gold']}; margin-bottom:0.3rem;">Research Question {i}</div>
            <div style="font-family:'Inter',sans-serif; font-size:1rem; font-weight:600;
                color:{C['navy']}; margin-bottom:0.3rem; line-height:1.5;">{q}</div>
            <div style="font-family:'Inter',sans-serif; font-size:0.92rem;
                color:{C['text_secondary']}; line-height:1.6;">{a}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    _render_question(1, *questions[0])
with row1_col2:
    _render_question(2, *questions[1])

row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    _render_question(3, *questions[2])
with row2_col2:
    _render_question(4, *questions[3])

# ── Data sources ──────────────────────────────────────────────────────────────
section_header("Data Sources")

col1, col2 = st.columns(2)
with col1:
    info_card("MBIE Jobs Online",
              "The primary data source for this project. Provides monthly series on changes "
              "in online job advertisements, with breakdowns by region, industry, occupation, "
              "and skill group. Used for both trend analysis and short-term forecasting.", "📋")
with col2:
    info_card("Stats NZ Labour Market Data",
              "Official employment indicators by industry and region, plus unemployment and "
              "underutilisation rates. Used to provide broader market context and validate "
              "the vacancy-based results — not as a substitute for the Jobs Online signal.", "🏛️")

st.write(
    "Together these two sources provide a more complete picture of hiring conditions. "
    "Jobs Online supplies the primary forecasting signal; Stats NZ helps situate those "
    "patterns within a wider labour market context."
)

# ── Workflow ──────────────────────────────────────────────────────────────────
section_header("Analytical Workflow")

steps = [
    ("1", "Data Acquisition & Cleaning",
     "Raw Jobs Online and Stats NZ datasets are collected, cleaned, and standardised."),
    ("2", "Integration & Preparation",
     "Cleaned datasets are reshaped and combined into integrated tables for analysis."),
    ("3", "Exploratory Analysis",
     "Labour demand trends are explored across time, regions, industries, and occupations."),
    ("4", "Forecasting & Interpretation",
     "Short-term models are applied and results are interpreted with official indicators."),
]

cols = st.columns(4)
for col, (num, title, desc) in zip(cols, steps):
    with col:
        st.markdown(
            f"""
            <div style="background:{C['card_bg']}; border:1px solid {C['border']};
                border-top:3px solid {C['gold']}; border-radius:6px;
                padding:1.4rem 1.2rem; text-align:center; height:100%;
                box-shadow:0 1px 6px rgba(0,59,92,0.06);">
                <div style="width:36px; height:36px; border-radius:50%;
                    background:{C['navy']}; color:{C['gold']};
                    font-family:'Playfair Display',serif; font-size:1.1rem; font-weight:600;
                    display:flex; align-items:center; justify-content:center;
                    margin:0 auto 0.8rem auto;">{num}</div>
                <div style="font-family:'Inter',sans-serif; font-size:0.88rem;
                    font-weight:700; color:{C['navy']}; margin-bottom:0.45rem;">{title}</div>
                <div style="font-family:'Inter',sans-serif; font-size:0.86rem;
                    color:{C['text_secondary']}; line-height:1.6;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Navigation ────────────────────────────────────────────────────────────────
section_header("Dashboard Navigation")

nav_items = [
    ("NZ Labour Demand Trends",  "National trend in hiring demand over time with skill-group breakdown."),
    ("Region Comparison",        "Hiring demand across major NZ regions — identify where markets are stronger or weaker."),
    ("Industry & Occupation",    "Sector and occupation-level demand patterns — spot where hiring is concentrated."),
    ("Forecast Explorer",        "Short-term forecasts at national, industry, and regional levels with confidence intervals."),
    ("Official Labour Context",  "Stats NZ indicators alongside Jobs Online — validate demand signals with official data."),
    ("Custom Explorer",          "Flexible self-directed exploration of any region, industry, occupation, or skill group."),
]

for page, desc in nav_items:
    st.markdown(
        f"""
        <div style="display:flex; align-items:flex-start; gap:1.25rem;
            padding:0.75rem 0.5rem; border-bottom:1px solid {C['border_light']};">
            <span style="font-family:'Inter',sans-serif; font-size:0.9rem;
                font-weight:700; color:{C['navy']}; min-width:220px; padding-top:1px;">
                {page}</span>
            <span style="font-family:'Inter',sans-serif; font-size:0.9rem;
                color:{C['text_secondary']}; line-height:1.6;">{desc}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

takeaway_card(
    "This project treats hiring demand as a real-time economic signal. "
    "By combining a high-frequency vacancy measure with official labour market data, "
    "it aims to give decision-makers a clearer, faster view of where the New Zealand "
    "labour market is heading."
)