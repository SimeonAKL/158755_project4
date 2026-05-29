import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Forecast Explorer", layout="wide")

st.title("Forecast Explorer")

st.write(
    """
This page presents short-term labour-demand forecasts based on the project forecasting outputs.
Users can switch between national, industry, and regional forecasts, inspect the projected trend,
and view forecast values in table form.
"""
)

TOTALS_PATH = os.path.join("data", "forecast", "totals_forecast_results.csv")
INDUSTRIES_PATH = os.path.join("data", "forecast", "industries_forecast_results.csv")
REGIONS_PATH = os.path.join("data", "forecast", "regional_forecast_results.csv")

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

try:
    df_totals = load_csv(TOTALS_PATH)
    df_industries = load_csv(INDUSTRIES_PATH)
    df_regions = load_csv(REGIONS_PATH)
except Exception as e:
    st.error(f"Error loading forecast data: {e}")
    st.stop()

df_totals["date"] = pd.to_datetime(df_totals["date"], errors="coerce")
df_industries["date"] = pd.to_datetime(df_industries["date"], errors="coerce")
df_regions["date"] = pd.to_datetime(df_regions["date"], errors="coerce")

st.header("Forecast Selection")

forecast_type = st.selectbox(
    "Select forecast type",
    ["National", "Industry", "Region"]
)

horizon = st.selectbox(
    "Select number of forecast periods to display",
    [3, 6],
    index=1
)

if forecast_type == "National":
    st.subheader("National Forecast Explorer")

    df_plot = df_totals[["date", "forecast", "lower_bound", "upper_bound"]].copy()
    df_plot = df_plot.dropna(subset=["forecast"]).sort_values("date").tail(horizon)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_plot["date"], df_plot["forecast"], marker="o", label="Forecast")
    ax.fill_between(
        df_plot["date"],
        df_plot["lower_bound"],
        df_plot["upper_bound"],
        alpha=0.2,
        label="Forecast interval"
    )
    ax.set_title("National Labour Demand Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Forecast Index")
    ax.grid(True, alpha=0.3)
    ax.legend()
    st.pyplot(fig)

    latest_forecast = df_plot["forecast"].iloc[-1]
    latest_date = df_plot["date"].iloc[-1]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Latest forecast", f"{latest_forecast:.2f}")
    with col2:
        st.metric("Lower bound", f"{df_plot['lower_bound'].iloc[-1]:.2f}")
    with col3:
        st.metric("Upper bound", f"{df_plot['upper_bound'].iloc[-1]:.2f}")

    st.write(
        f"""
The national forecast shows the projected short-term path of aggregate labour demand in New Zealand.
The latest displayed forecast value is **{latest_forecast:.2f}** for **{latest_date.strftime('%b %Y')}**.
"""
    )

    st.dataframe(df_plot.reset_index(drop=True), use_container_width=True)

    csv_data = df_plot.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download national forecast as CSV",
        data=csv_data,
        file_name="national_forecast_selection.csv",
        mime="text/csv"
    )

    st.subheader("Business takeaway")
    st.write(
        "Short-term forecast signals can help highlight whether aggregate labour demand is stable, strengthening, or softening in the near term."
    )

elif forecast_type == "Industry":
    st.subheader("Industry Forecast Explorer")

    industry_options = {
        "IT": ("it_forecast", "it_lower", "it_upper"),
        "Health Care": ("health_care_forecast", "health_care_lower", "health_care_upper"),
        "Construction": ("construction_forecast", "construction_lower", "construction_upper"),
        "Education": ("education_forecast", "education_lower", "education_upper"),
        "Hospitality": ("hospitality_forecast", "hospitality_lower", "hospitality_upper"),
        "Sales": ("sales_forecast", "sales_lower", "sales_upper")
    }

    selected_industry = st.selectbox("Select industry", list(industry_options.keys()))
    forecast_col, lower_col, upper_col = industry_options[selected_industry]

    df_plot = df_industries[["date", forecast_col, lower_col, upper_col]].copy()
    df_plot = df_plot.dropna(subset=[forecast_col]).sort_values("date").tail(horizon)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_plot["date"], df_plot[forecast_col], marker="o", label=selected_industry)
    ax.fill_between(
        df_plot["date"],
        df_plot[lower_col],
        df_plot[upper_col],
        alpha=0.2,
        label="Forecast interval"
    )
    ax.set_title(f"{selected_industry} Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Forecast Index")
    ax.grid(True, alpha=0.3)
    ax.legend()
    st.pyplot(fig)

    latest_forecast = df_plot[forecast_col].iloc[-1]
    latest_date = df_plot["date"].iloc[-1]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Latest forecast", f"{latest_forecast:.2f}")
    with col2:
        st.metric("Lower bound", f"{df_plot[lower_col].iloc[-1]:.2f}")
    with col3:
        st.metric("Upper bound", f"{df_plot[upper_col].iloc[-1]:.2f}")

    if len(df_plot) >= 2:
        current_val = df_plot[forecast_col].iloc[-1]
        previous_val = df_plot[forecast_col].iloc[-2]
        if current_val > previous_val:
            direction_text = "shows a short-term upward direction"
        elif current_val < previous_val:
            direction_text = "shows a short-term softening pattern"
        else:
            direction_text = "appears broadly stable in the short term"
        st.info(f"{selected_industry} {direction_text} based on the latest forecast periods.")

    st.write(
        f"""
This chart shows the projected short-term labour-demand path for **{selected_industry}**.
The latest displayed forecast value is **{latest_forecast:.2f}** for **{latest_date.strftime('%b %Y')}**.
"""
    )

    display_df = df_plot.rename(columns={
        forecast_col: "forecast",
        lower_col: "lower_bound",
        upper_col: "upper_bound"
    })

    st.dataframe(display_df.reset_index(drop=True), use_container_width=True)

    csv_data = display_df.to_csv(index=False).encode("utf-8")
    safe_name = selected_industry.lower().replace(" ", "_")
    st.download_button(
        label="Download industry forecast as CSV",
        data=csv_data,
        file_name=f"{safe_name}_forecast_selection.csv",
        mime="text/csv"
    )

    st.subheader("Business takeaway")
    st.write(
        "Short-term forecast signals can help highlight which sectors are stable, strengthening, or softening in the near term."
    )

elif forecast_type == "Region":
    st.subheader("Regional Forecast Explorer")

    region_options = {
        "Auckland": ("auckland_forecast", "auckland_lower", "auckland_upper"),
        "Wellington": ("wellington_forecast", "wellington_lower", "wellington_upper"),
        "Canterbury": ("canterbury_forecast", "canterbury_lower", "canterbury_upper")
    }

    selected_region = st.selectbox("Select region", list(region_options.keys()))
    forecast_col, lower_col, upper_col = region_options[selected_region]

    df_plot = df_regions[["date", forecast_col, lower_col, upper_col]].copy()
    df_plot = df_plot.dropna(subset=[forecast_col]).sort_values("date").tail(horizon)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_plot["date"], df_plot[forecast_col], marker="o", label=selected_region)
    ax.fill_between(
        df_plot["date"],
        df_plot[lower_col],
        df_plot[upper_col],
        alpha=0.2,
        label="Forecast interval"
    )
    ax.set_title(f"{selected_region} Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Forecast Index")
    ax.grid(True, alpha=0.3)
    ax.legend()
    st.pyplot(fig)

    latest_forecast = df_plot[forecast_col].iloc[-1]
    latest_date = df_plot["date"].iloc[-1]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Latest forecast", f"{latest_forecast:.2f}")
    with col2:
        st.metric("Lower bound", f"{df_plot[lower_col].iloc[-1]:.2f}")
    with col3:
        st.metric("Upper bound", f"{df_plot[upper_col].iloc[-1]:.2f}")

    if len(df_plot) >= 2:
        current_val = df_plot[forecast_col].iloc[-1]
        previous_val = df_plot[forecast_col].iloc[-2]
        if current_val > previous_val:
            direction_text = "shows a short-term upward direction"
        elif current_val < previous_val:
            direction_text = "shows a short-term softening pattern"
        else:
            direction_text = "appears broadly stable in the short term"
        st.info(f"{selected_region} {direction_text} based on the latest forecast periods.")

    st.write(
        f"""
This chart shows the projected short-term labour-demand path for **{selected_region}**.
The latest displayed forecast value is **{latest_forecast:.2f}** for **{latest_date.strftime('%b %Y')}**.
"""
    )

    display_df = df_plot.rename(columns={
        forecast_col: "forecast",
        lower_col: "lower_bound",
        upper_col: "upper_bound"
    })

    st.dataframe(display_df.reset_index(drop=True), use_container_width=True)

    csv_data = display_df.to_csv(index=False).encode("utf-8")
    safe_name = selected_region.lower().replace(" ", "_")
    st.download_button(
        label="Download regional forecast as CSV",
        data=csv_data,
        file_name=f"{safe_name}_forecast_selection.csv",
        mime="text/csv"
    )

    st.subheader("Business takeaway")
    st.write(
        "Regional forecast signals show that short-term labour demand may not move in the same way across major labour markets."
    )