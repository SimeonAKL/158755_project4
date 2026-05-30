# NZ Labour Demand Forecaster

## Project Overview

**NZ Labour Demand Forecaster** is an interactive Streamlit dashboard developed for the **158755 Data Science: Making Sense of Data** project.  
The dashboard explores short-term labour demand patterns in New Zealand using **MBIE Jobs Online** data as the main vacancy signal and **Stats NZ labour market indicators** as supporting context.

The project is designed to help users understand:

- how national hiring demand has changed over time
- how labour demand differs across regions, industries, occupations, and skill groups
- whether short-term labour demand can be forecast over the next 3–6 months
- how official labour market indicators help interpret vacancy-based demand signals

The dashboard is aimed at **tech-savvy executives, recruiters, HR planners, analysts, and assessors** who want a clear and presentation-ready view of current labour market conditions.

---

## Project Objectives

The main objectives of the project are to:

1. analyse overall online labour demand trends in New Zealand
2. compare labour-demand patterns across regions, industries, occupations, and skill groups
3. build short-term forecasting views for national, regional, and industry-level hiring demand
4. place Jobs Online trends into a broader official labour market context using Stats NZ indicators
5. provide an interactive dashboard that is easier to explore than a static notebook alone

---

## Research Questions

This project is structured around four main research questions:

1. **How has overall online labour demand changed over time in New Zealand?**
2. **How do labour-demand patterns differ across regions, industries, and occupations?**
3. **Can Jobs Online data be used to forecast labour demand over the next 3–6 months?**
4. **How can official labour-market data strengthen the interpretation and validation of the forecast results?**

---

## Data Sources

### 1. MBIE Jobs Online
This is the main source used for labour demand analysis and forecasting.  
It provides hiring-demand signals based on online job advertisements and includes breakdowns by:

- total national demand
- region
- industry
- occupation
- skill group

### 2. Stats NZ Labour Market Data
This dataset is used as supporting context rather than the main forecasting signal.  
It helps interpret vacancy-based labour demand using official labour market indicators such as:

- unemployment
- underutilisation
- employment by region
- employment by industry
- related labour market series

---

## Notebook Content

The notebook contains the full analytical workflow behind the dashboard.  
It is structured as a project report and covers:

### 1. Project Overview
Introduces the project topic, motivation, and analytical direction.

### 2. Background and Research Questions
Explains the labour market context and defines the four research questions.

### 3. Data Sources
Describes the MBIE Jobs Online data and Stats NZ supporting datasets.

### 4. Data Acquisition and Preparation
Covers data loading, cleaning, restructuring, and integration.

### 5. Exploratory Data Analysis
Examines national, regional, industry, occupation, and skill-level hiring demand patterns.

### 6. Forecasting Models
Builds and compares short-term forecasting models for labour demand.

This section includes:
- forecasting model design
- temporal alignment and lagged features
- national forecast
- industry forecast
- regional forecast
- evaluation and interpretation

### 7. Results and Interpretation
Summarises the main findings for each research question.

### 8. Limitations and Conclusion
Discusses modelling limitations, interpretation cautions, and overall project value.

### 9. References
Lists the main academic and data-source references used in the project.

---

## Dashboard Page Guide

### 1. Home Page
The Home page gives users a quick overview of the whole dashboard. It introduces the project purpose, shows the latest national hiring demand snapshot, and provides a short forecast preview.

**Main functions**
- Shows the latest national hiring demand index
- Shows the historical peak and trough of hiring demand
- Displays the latest near-term national forecast
- Provides a national hiring demand trend chart
- Provides a short forecast preview chart
- Summarises the latest industry and regional forecast rankings
- Explains who the dashboard is for, what it shows, and how to use it

---

### 2. Project Overview Page
The Project Overview page explains the background, objectives, research questions, data sources, workflow, and navigation structure of the project.

**Main functions**
- Introduces the project background and motivation
- Lists the main project objectives
- Presents the four research questions
- Describes the two main data sources: MBIE Jobs Online and Stats NZ labour market data
- Explains the analytical workflow from data acquisition to forecasting
- Provides a navigation guide for each dashboard page
- Includes a key insight summarising the role of vacancy data as a labour market signal

---

### 3. NZ Labour Demand Trends Page
This page focuses on national-level hiring demand trends over time.

**Main functions**
- Allows users to select a date range
- Shows a period summary including current demand, peak, trough, and period average
- Displays the overall national hiring demand trend
- Shows year-on-year percentage change in hiring demand
- Compares skilled and unskilled hiring demand
- Allows users to switch the skill comparison view between:
  - Both
  - Skilled only
  - Unskilled only
- Provides a filtered data download button

This page answers the question: **how has overall online labour demand changed over time in New Zealand?**

---

### 4. Region Comparison Page
The Region Comparison page compares hiring demand across major New Zealand regions.

**Main functions**
- Allows users to select one or more regions for comparison
- Displays regional hiring demand trends over time
- Shows the latest regional standing using a bar chart
- Provides a regional ranking table
- Shows summary metrics for the strongest region, weakest region, and demand spread
- Provides a short explanation of regional differences
- Allows users to view the underlying regional data

---

### 5. Industry & Occupation Comparison Page
This page compares hiring demand by industry or occupation group.

**Main functions**
- Allows users to choose between industry comparison and occupation comparison
- Allows users to select specific groups to compare
- Provides a date range slider
- Displays trend charts for selected industries or occupations
- Shows the latest standing using a bar chart
- Provides ranking tables for selected groups
- Summarises the strongest and weakest group in the selected view

---

### 6. Forecast Explorer Page
The Forecast Explorer page presents short-term hiring demand forecasts.

**Main functions**
- Allows users to choose forecast scope:
  - National
  - Industry
  - Region
- Industry and regional views include a sub-selector for the specific sector or region
- Allows users to select the number of forecast periods to display
- Shows forecast values, lower bounds, and upper bounds
- Displays forecast charts with confidence intervals
- Shows near-term direction such as strengthening, softening, or stable
- Allows users to download forecast data as CSV

This page is mainly used to explore whether hiring demand may increase, decrease, or remain stable in the short term.

---

### 7. Official Labour Context Page
The Official Labour Context page compares Jobs Online hiring demand with official Stats NZ labour market indicators.

**Main functions**
- Allows users to select official data frequency:
  - Monthly indicators
  - Quarterly indicators
- Allows users to select an official labour market indicator
- Uses clearer display names instead of raw column names
- Displays the selected official indicator over time
- Compares Jobs Online hiring demand with the selected official indicator
- Explains how to interpret the relationship between vacancy-based demand and official labour market data
- Includes supporting interpretation cards and notes

---

### 8. Custom Explorer Page
The Custom Explorer page is a flexible exploration workspace.

**Main functions**
- Allows users to choose a data group:
  - Region
  - Industry
  - Occupation
  - Skill Group
- Allows users to select multiple series from the chosen group
- Provides a date range selector
- Allows users to normalise selected series to an index base of 100
- Displays selected series in a trend chart
- Provides a summary table with latest value, average, high, low, and range
- Shows the underlying filtered data
- Allows users to download the selected data

---

## App File Structure

```text
158755_project4/
├── app/
│   ├── Home.py
│   └── pages/
│       ├── 1_Project_Overview.py
│       ├── 2_NZ_Labour_Demand_Trends.py
│       ├── 3_Region_Comparison.py
│       ├── 4_Industry_Occupation_Comparison.py
│       ├── 5_Forecast_Explorer.py
│       ├── 6_Official_Labour_Context.py
│       └── 7_Custom_Explorer.py
├── data/
│   ├── forecast/
│   │   ├── industries_forecast_results.csv
│   │   ├── regional_forecast_results.csv
│   │   └── totals_forecast_results.csv
│   └── integrated/
│       ├── employment_industry_long.csv
│       ├── employment_region_long.csv
│       ├── jobs_online_monthly.csv
│       ├── jobs_online_quarterly.csv
│       ├── monthly_labour_market_master.csv
│       ├── quarterly_labour_force_master.csv
│       └── vacancy_master.csv
├── notebooks/
├── src/
├── requirements.txt
└── README.md
```

---

## Key Files

### App
- `app/Home.py` — dashboard landing page and summary view
- `app/pages/...` — detailed dashboard pages

### Data
- `data/integrated/jobs_online_monthly.csv` — main monthly labour demand dataset
- `data/integrated/vacancy_master.csv` — integrated vacancy-level analytical dataset
- `data/integrated/monthly_labour_market_master.csv` — monthly supporting labour context
- `data/integrated/quarterly_labour_force_master.csv` — quarterly supporting labour context
- `data/forecast/totals_forecast_results.csv` — national forecast outputs
- `data/forecast/industries_forecast_results.csv` — industry forecast outputs
- `data/forecast/regional_forecast_results.csv` — regional forecast outputs

### Other
- `requirements.txt` — Python dependencies for deployment
- `README.md` — project guide and dashboard documentation

---

## General Notes

- The dashboard uses **Jobs Online** as the main signal for labour demand.
- **Stats NZ** data is used as supporting context, not as a replacement for the Jobs Online series.
- Forecast results should be interpreted as **short-term directional signals**, not long-term predictions.
- National averages can hide important regional, industry, occupation, and skill-level differences.
- Most pages include interactive controls, charts, summary text, and either raw data views or download options.
- The visual design follows a **Massey-inspired professional style** using navy, gold, white, and light grey.

---

## Suggested Usage

This dashboard can be used for:

- project presentation and demonstration
- labour market trend exploration
- short-term hiring demand monitoring
- regional and sector comparison
- communicating project findings in a more interactive format than the notebook alone

---

## Acknowledgements

This project uses publicly available labour market data from:

- **MBIE Jobs Online**
- **Stats NZ**

The dashboard was built in **Streamlit** and designed as a presentation-ready companion to the main project notebook.
