import streamlit as st

st.set_page_config(
    page_title="NZ Labour Demand Forecaster",
    page_icon="📊",
    layout="wide"
)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        color: #1f2d3d;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #4f5b67;
        margin-bottom: 1.5rem;
    }
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
        color: #1f2d3d;
    }
    .card {
        padding: 1rem 1.2rem;
        border-radius: 12px;
        background-color: #f8f9fb;
        border: 1px solid #e6e9ef;
        margin-bottom: 1rem;
    }
    .small-card {
        padding: 0.9rem 1rem;
        border-radius: 10px;
        background-color: #ffffff;
        border: 1px solid #e6e9ef;
        height: 100%;
    }
    .rq-box {
        padding: 0.9rem 1rem;
        border-left: 4px solid #4c78a8;
        background-color: #f8fbff;
        border-radius: 8px;
        margin-bottom: 0.7rem;
    }
    .footer-note {
        color: #6b7280;
        font-size: 0.92rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Header
# ----------------------------
st.markdown('<div class="main-title">NZ Labour Demand Forecaster</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">A Streamlit dashboard for analysing and forecasting short-term labour demand trends in New Zealand</div>',
    unsafe_allow_html=True
)

# ----------------------------
# Intro
# ----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.write(
    """
This project examines short-term labour demand in New Zealand using **MBIE Jobs Online** data together with
**official labour market indicators from Stats NZ**. The dashboard is designed to present the main analytical
results from the project notebook in a more interactive form.

The app focuses on three main tasks:

1. summarising overall labour demand trends over time  
2. comparing labour demand across regions, industries, and occupations  
3. presenting short-term forecasting results and official labour market context
"""
)
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Main overview cards
# ----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="small-card">', unsafe_allow_html=True)
    st.markdown("### Project focus")
    st.write(
        """
- Online labour demand in New Zealand  
- Regional, industry, occupation, and skill differences  
- 3–6 month short-term forecasting
"""
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="small-card">', unsafe_allow_html=True)
    st.markdown("### Main data sources")
    st.write(
        """
- **MBIE Jobs Online**  
- **Stats NZ labour market data**  
- Monthly and quarterly labour-demand indicators
"""
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="small-card">', unsafe_allow_html=True)
    st.markdown("### Methods used")
    st.write(
        """
- Data cleaning and integration  
- Exploratory data analysis  
- Prophet and Random Forest forecasting
"""
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Research questions
# ----------------------------
st.markdown('<div class="section-title">Research Questions</div>', unsafe_allow_html=True)

rq_list = [
    "How has overall online labour demand changed over time in New Zealand?",
    "How do labour-demand patterns differ across regions, industries, and occupations?",
    "Can Jobs Online data be used to forecast labour demand over the next 3–6 months?",
    "How can official labour-market data strengthen the interpretation and validation of the forecast results?"
]

for i, rq in enumerate(rq_list, start=1):
    st.markdown(
        f'<div class="rq-box"><b>RQ{i}.</b> {rq}</div>',
        unsafe_allow_html=True
    )

# ----------------------------
# Page guide
# ----------------------------
st.markdown('<div class="section-title">Dashboard Pages</div>', unsafe_allow_html=True)

page_col1, page_col2 = st.columns(2)

with page_col1:
    st.markdown('<div class="small-card">', unsafe_allow_html=True)
    st.markdown("### Explore the dashboard")
    st.write(
        """
- **Project Overview**: project background, data sources, and workflow  
- **NZ Labour Demand Trends**: overall trend and summary indicators  
- **Region Comparison**: regional labour-demand patterns and ranking
"""
    )
    st.markdown('</div>', unsafe_allow_html=True)

with page_col2:
    st.markdown('<div class="small-card">', unsafe_allow_html=True)
    st.markdown("### Forecast and context")
    st.write(
        """
- **Industry Occupation Comparison**: subgroup trend comparison  
- **Forecast Page**: short-term forecast outputs  
- **Official Labour Context**: Stats NZ indicators for interpretation
"""
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Workflow
# ----------------------------
st.markdown('<div class="section-title">Project Workflow</div>', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.write(
    """
The project workflow follows a clear sequence. First, Jobs Online and Stats NZ datasets are collected,
cleaned, and standardised. Second, the cleaned datasets are integrated into analysis-ready tables for
trend comparison and subgroup analysis. Third, forecasting models are applied to the national series and
selected industries and regions. Finally, the results are presented in this dashboard to support interactive
exploration and interpretation.
"""
)
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Footer
# ----------------------------
st.markdown(
    '<div class="footer-note">Built for 158755 Project 4: NZ Labour Demand Forecaster</div>',
    unsafe_allow_html=True
)
