import streamlit as st

st.set_page_config(page_title="Project Overview", layout="wide")

st.title("Project Overview")

st.write(
    """
This project examines short-term labour demand trends in New Zealand using Jobs Online data and official labour market data from Stats NZ. 
The project focuses on how online labour demand has changed over time, how it differs across regions, industries, and occupations, 
and whether recent vacancy patterns can support short-term forecasting over the next 3–6 months.
"""
)

st.header("Project Background")

st.write(
    """
Understanding labour demand is important for interpreting recent changes in the New Zealand job market. 
Changes in online job advertisements can reflect shifts in hiring activity, employer confidence, and sector-level demand. 
In recent years, labour demand in New Zealand has not moved evenly over time. Periods such as the global financial crisis, 
COVID-19 disruption, and the post-pandemic recovery have all been associated with noticeable changes in vacancy activity. 
For this reason, vacancy-based data provides a useful way to examine short-term labour market movement.
"""
)

st.write(
    """
This project focuses on Jobs Online, a regular New Zealand data source that tracks changes in online job advertisements. 
Jobs Online is useful because it provides timely labour demand information and includes breakdowns by region, industry, 
occupation, and skill group. These features make it suitable for both trend analysis and short-term forecasting. 
However, vacancy data alone does not provide a complete picture of the labour market. To strengthen interpretation, 
this project also uses official labour market data from Stats NZ, including employment indicators, unemployment, 
and underutilisation-related measures. These datasets help place vacancy trends within a broader labour market context 
and support interpretation of the forecasting results.
"""
)

st.header("Main Objectives")

st.markdown(
    """
- analyse overall online labour demand trends in New Zealand  
- compare labour-demand patterns across regions, industries, and occupations  
- develop short-term forecasting models for labour demand over the next 3–6 months  
- use official labour market data to strengthen interpretation and validation of the forecast results  
"""
)

st.header("Research Questions")

st.markdown(
    """
1. **How has overall online labour demand changed over time in New Zealand?**  
2. **How do labour-demand patterns differ across regions, industries, and occupations?**  
3. **Can Jobs Online data be used to forecast labour demand over the next 3–6 months?**  
4. **How can official labour-market data strengthen the interpretation and validation of the forecast results?**  
"""
)

st.write(
    """
These questions guide the structure of the project. The first two questions are addressed through exploratory analysis 
of overall and subgroup labour-demand patterns. The third question is addressed through short-term forecasting at the 
national, industry, and regional levels. The fourth question is addressed by using official labour market indicators 
from Stats NZ to support interpretation and validation of the vacancy-based results.
"""
)

st.header("Data Sources")

col1, col2 = st.columns(2)

with col1:
    st.subheader("MBIE Jobs Online")
    st.write(
        """
The MBIE Jobs Online datasets are the main source for this project. They provide information on changes in online job 
advertisements over time and include breakdowns by region, industry, occupation, and skill group. In this project, 
the monthly Jobs Online series is used as the main dataset for trend analysis and short-term forecasting, while the 
subgroup Jobs Online files are used to compare labour-demand patterns across different categories.
"""
    )

with col2:
    st.subheader("Stats NZ Labour Market Data")
    st.write(
        """
The Stats NZ datasets are used to provide official labour market context. These include employment indicators by 
industry and region, as well as unemployment and underutilisation rates. Unlike Jobs Online, which reflects vacancy 
activity, Stats NZ data captures broader labour market conditions. This makes it useful for interpreting and validating 
the forecast results rather than replacing the vacancy-based analysis.
"""
    )

st.write(
    """
Together, these two sources provide a more balanced view of labour demand in New Zealand. Jobs Online supplies the 
main forecasting signal, while Stats NZ helps place those patterns in a wider labour market context and supports 
interpretation of the forecast results.
"""
)

st.header("Workflow Overview")

st.write("The project follows four main stages:")

st.markdown(
    """
**1. Data acquisition and cleaning**  
Raw Jobs Online and Stats NZ datasets are collected, cleaned, and standardised.

**2. Data integration and preparation**  
The cleaned datasets are reshaped and combined into cleaned and integrated tables for analysis.

**3. Exploratory data analysis**  
Labour demand trends are explored across time, regions, industries, occupations, and skills.

**4. Forecasting and interpretation**  
Short-term forecasting models are applied, and the results are interpreted together with official labour market indicators.
"""
)

st.header("How to Use This Dashboard")

st.write(
    """
Use the navigation menu on the left to move through the main parts of the project:

- **NZ Labour Demand Trends** shows the overall trend in labour demand over time  
- **Region Comparison** compares labour-demand patterns across different regions  
- **Industry Occupation Comparison** explores subgroup differences  
- **Forecast Page** presents short-term forecasting results  
- **Official Labour Context** provides supporting interpretation using Stats NZ data  
"""
)
