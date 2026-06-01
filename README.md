# NZ Labour Demand Forecaster

**Repository:** https://github.com/SimeonAKL/158755_project4

## Project Structure

This project is organised into two main parts:

- **Notebook**: contains the main analysis, forecasting workflow, interpretation, and report content
- **App**: contains the Streamlit dashboard used to present the project results interactively

---

## Notebook Structure

The notebook is the main analytical document for the project.  
It follows the structure below:

### 1. Project Overview
Introduces the topic, project purpose, and overall analytical direction.

### 2. Background and Research Questions
Explains the labour market context and defines the main research questions.

### 3. Data Sources
Describes the two main data sources used in the project:
- MBIE Jobs Online
- Stats NZ labour market data

### 4. Data Acquisition and Preparation
Covers data loading, cleaning, reshaping, and integration.

### 5. Exploratory Data Analysis
Examines labour demand patterns across:
- time
- regions
- industries
- occupations
- skill groups

### 6. Forecasting Models
Presents the short-term forecasting analysis, including:
- model design
- lagged features and alignment
- national forecast
- industry forecast
- regional forecast
- model evaluation

### 7. Results and Interpretation
Summarises the main findings and links them back to the research questions.

### 8. Limitations and Conclusion
Explains the key limitations and provides the overall conclusion.

### 9. References
Lists the main academic and data-source references used in the project.

---

## App Structure

The Streamlit app is a presentation-focused version of the project.  
It is designed to help users explore the main results more easily.

### Home
Provides a dashboard summary of the project, including the latest national demand snapshot and forecast preview.

### Project Overview
Explains the project background, objectives, research questions, data sources, and workflow.

### NZ Labour Demand Trends
Shows national hiring demand trends over time, year-on-year change, and skilled vs unskilled demand.

### Region Comparison
Compares hiring demand across major New Zealand regions.

### Industry & Occupation Comparison
Compares hiring demand across selected industries or occupation groups.

### Forecast Explorer
Displays short-term forecast results for:
- national demand
- industry demand
- regional demand

### Official Labour Context
Compares Jobs Online demand with official Stats NZ labour market indicators.

### Custom Explorer
Allows flexible exploration of selected regions, industries, occupations, or skill groups.

---

## File Structure

```text
158755_project4/
├── app/
│   ├── Home.py
│   ├── utils/
│   │   └── theme.py
│   └── pages/
│       ├── 1_Project_Overview.py
│       ├── 2_NZ_Labour_Demand_Trends.py
│       ├── 3_Region_Comparison.py
│       ├── 4_Industry_Occupation_Comparison.py
│       ├── 5_Forecast_Explorer.py
│       ├── 6_Official_Labour_Context.py
│       └── 7_Custom_Explorer.py
├── data/
│   ├── raw/
│   │   ├── jobs-online-all-unadjusted-quarterly-data-consolidated-march-2026.csv
│   │   ├── jobs-online-monthly-unadjusted-series-from-may-2007-april-2026.csv
│   │   ├── jobs-online-vacancies-by-industry-unadjusted-quarterly-march-2026.xlsx
│   │   ├── jobs-online-vacancies-by-occupation-unadjusted-quarterly-march-2026.xlsx
│   │   ├── jobs-online-vacancies-by-skills-unadjusted-quarterly-march-2026.xlsx
│   │   ├── statsnz_employment_indicators_industry_by_variable_monthly.csv
│   │   ├── statsnz_employment_indicators_region_by_variable_monthly.csv
│   │   ├── statsnz_persons_employed_by_sex_by_employment_status_qtrly.csv
│   │   ├── statsnz_persons_underemployed_by_sex_qtrly_marjunsepdec.csv
│   │   └── statsnz_unemployment_underutilisation_quarterly.csv
│   ├── cleaned/
│   │   ├── employment_industry_monthly.csv
│   │   ├── employment_region_monthly.csv
│   │   ├── jobs_online_monthly.csv
│   │   ├── jobs_online_quarterly.csv
│   │   ├── persons_employed_by_sex.csv
│   │   ├── persons_underemployed_by_sex.csv
│   │   ├── unemployment_underutilisation.csv
│   │   ├── vacancies_by_industry.csv
│   │   ├── vacancies_by_occupation.csv
│   │   └── vacancies_by_skill.csv
│   ├── integrated/
│   │   ├── employment_industry_long.csv
│   │   ├── employment_region_long.csv
│   │   ├── jobs_online_monthly.csv
│   │   ├── jobs_online_quarterly.csv
│   │   ├── monthly_labour_market_master.csv
│   │   ├── quarterly_labour_force_master.csv
│   │   └── vacancy_master.csv
│   └── forecast/
│       ├── industries_forecast_results.csv
│       ├── regional_forecast_results.csv
│       └── totals_forecast_results.csv
├── figures/
├── notebooks/
│   └── MasseyUniversity_158755_Project4_Group1.ipynb
├── MasseyUniversity_158755_Project4_Group1.html
├── requirements.txt
├── README.md
└── .devcontainer/
    └── devcontainer.json