import streamlit as st

st.set_page_config(page_title="Project Overview", layout="wide")

st.title("Project Overview")

st.markdown(
    """
    This project examines short-term labour demand trends in New Zealand using 
    **Jobs Online** data and **official labour market data from Stats NZ**. 
    The project focuses on how online labour demand has changed over time, how it 
    differs across regions, industries, and occupations, and whether recent patterns 
    can support short-term forecasting over the next 3–6 months.
    """
)

st.subheader("Project Background")
st.write(
    "Online job advertisement data provides a useful way to monitor recent labour demand "
    "movement in New Zealand. Changes in vacancy activity can reflect shifts in employer "
    "confidence, hiring activity, and sector-level demand. However, vacancy data alone does "
    "not fully represent the wider labour market. For this reason, this project combines "
    "Jobs Online with official labour market data from Stats NZ to provide both a vacancy-based "
    "view and a broader labour market context."
)

st.subheader("Main Objectives")
st.markdown(
    """
    - analyse overall online labour demand trends in New Zealand  
    - compare labour-demand patterns across regions, industries, and occupations  
    - develop short-term forecasting models for labour demand over the next 3–6 months  
    - use official labour market data to strengthen interpretation and validation of the forecast results  
    """
)

st.subheader("Research Questions")
st.markdown(
    """
    1. **How has overall online labour demand changed over time in New Zealand?**  
    2. **How do labour-demand patterns differ across regions, industries, and occupations?**  
    3. **Can Jobs Online data be used to forecast labour demand over the next 3–6 months?**  
    4. **How can official labour-market data strengthen the interpretation and validation of the forecast results?**  
    """
)

st.subheader("Data Sources")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### MBIE Jobs Online")
    st.write(
        "Jobs Online is the main data source used for labour demand analysis and forecasting. "
        "It provides regular measures of online job advertisement activity in New Zealand, "
        "including breakdowns by region, industry, occupation, and skill group."
    )

with col2:
    st.markdown("### Stats NZ Labour Market Data")
    st.write(
        "Stats NZ data is used to provide official labour market context. In this project, "
        "it includes employment indicators by industry and region, as well as unemployment "
        "and underutilisation-related measures. These datasets support interpretation and "
        "validation rather than replacing the vacancy-based analysis."
    )

st.subheader("Workflow Overview")
st.markdown(
    """
    The project follows four main stages:

    **1. Data acquisition and cleaning**  
    Raw Jobs Online and Stats NZ datasets are collected, cleaned, and standardised.

    **2. Data integration and preparation**  
    The cleaned datasets are reshaped and combined into cleaned and integrated tables for analysis.

    **3. Exploratory data analysis**  
    Labour demand trends are explored across time, regions, industries, occupations, and skills.

    **4. Forecasting and interpretation**  
    Short-term forecasting models are applied to Jobs Online data, while official labour market data is used to support interpretation and validation.
    """
)

st.info(
    "This page introduces the project background, research questions, data sources, and overall analytical workflow."
)
