import streamlit as st
import pandas as pd

from models.forecasting import get_materials, get_forecast
from models.optimization import get_inventory_snapshot, run_scenario

# Main Page
st.set_page_config(

    page_title="ReelSynapse - Optima Team",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="logo.jpeg"
)

# Sidebar
st.sidebar.title("ReelSynapse")
st.sidebar.markdown("by *Optima Team*")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Scenario Simulation", "Reports"],
    index=0,
)
horizon_days = st.sidebar.slider("Forecast Horizon (days)", 7, 90, 30)

# Dashboard
if page == "Dashboard":
    st.title("📊 Inventory & Demand Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Inventory Value", "3.2M EGP", "+5%")
    col2.metric("Forecast Accuracy", "87%", "+3%")
    col3.metric("Overall Risk Level", "Medium")

    st.markdown("---")

    # Material Selection
    st.subheader("Demand Forecast")
    materials = get_materials()
    material = st.selectbox("Select Material", materials, index=0)

    df_forecast = get_forecast(material, horizon_days=horizon_days)
    df_plot = df_forecast.set_index("date")[["actual", "forecast"]]
    st.line_chart(df_plot)

    # Inventory Status
    st.subheader("📦 Current Inventory Status")
    inv_df = get_inventory_snapshot()
    st.dataframe(inv_df, use_container_width=True)

#  Scenario Simulation
elif page == "Scenario Simulation":
    st.title("🧪 Scenario Simulation")
    st.markdown(
        "Try changing of the folllowing parameter to see its effect"
    )

    col1, col2 = st.columns(2)

    with col1:
        price_change = st.slider("Price Change (%)", -50, 50, 0)
        demand_change = st.slider("Demand Change (%)", -50, 50, 0)

    with col2:
        lead_time_change = st.slider("Lead Time Change (%)", -50, 50, 0)
        base_demand = st.number_input(
            "Base Monthly Demand (tons)",
            min_value=10.0,
            max_value=10000.0,
            value=100.0,
            step=10.0,
        )

    if st.button("Run Scenario"):
        result = run_scenario(
            base_demand=base_demand,
            price_change_pct=price_change,
            demand_change_pct=demand_change,
            lead_time_change_pct=lead_time_change,
        )

        st.success("You Have Applied a New Scenario")

        c1, c2, c3 = st.columns(3)
        c1.metric("New Demand (tons)", f"{result['new_demand']:.1f}")
        c2.metric("Estimated Cost Index", f"{result['estimated_cost_index']:.1f}")
        c3.metric("Shortage Risk (%)", f"{result['shortage_risk_pct']:.1f}")

        st.markdown("### Details")
        st.write(
            f"- Demand factor: x{result['demand_factor']:.2f}\n"
            f"- Price factor: x{result['price_factor']:.2f}\n"
            f"- Lead time factor: x{result['lead_time_factor']:.2f}"
        )


# Report Page
elif page == "Reports":
    st.title("📑 Reports (Placeholder)")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")

    report_type = st.selectbox(
        "Report Type",
        ["Summary", "Inventory Only", "Forecast Only", "Full"],
    )

    if st.button("Generate Report"):
        st.info(
            "No Generation Till Now"

        )
        st.write(
            f"(TRAiL MASSAGE) Generating *{report_type}* report from {start_date} to {end_date} "
        )