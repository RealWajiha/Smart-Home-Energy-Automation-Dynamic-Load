import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Smart Home Energy Automation & Dynamic Load Shedding",
    page_icon="⚡",
    layout="wide"
)

# ---------------- Dark Carbon & Emerald Green Theme ----------------
st.markdown(
    """
    <style>
        .stApp {
            background-color: #090d16;
            color: #e6edf3;
        }

        h1, h2, h3, h4, h5, h6, p, label {
            color: #e6edf3 !important;
        }

        .main-title {
            font-size: 2.3rem;
            font-weight: 800;
            background: linear-gradient(90deg, #10b981, #f59e0b, #ef4444);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            color: #9ca3af !important;
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
        }

        section[data-testid="stSidebar"] {
            background-color: #111827 !important;
            border-right: 1px solid #1f2937 !important;
        }

        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3, 
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {
            color: #f3f4f6 !important;
        }

        section[data-testid="stSidebar"] input {
            background-color: #1f2937 !important;
            color: #ffffff !important;
            border: 1px solid #374151 !important;
            border-radius: 8px !important;
        }

        div[data-testid="stMetric"] {
            background-color: #111827;
            border: 1px solid #1f2937;
            border-radius: 12px;
            padding: 16px;
        }

        div[data-testid="stMetricValue"] {
            color: #10b981 !important;
            font-weight: 700;
        }

        div[data-testid="stMetricLabel"] {
            color: #9ca3af !important;
        }

        .status-critical {
            background-color: #450a0a;
            border: 1px solid #ef4444;
            color: #fca5a5 !important;
            padding: 16px;
            border-radius: 10px;
            font-weight: 700;
            margin-bottom: 1rem;
        }

        .status-healthy {
            background-color: #064e3b;
            border: 1px solid #10b981;
            color: #a7f3d0 !important;
            padding: 16px;
            border-radius: 10px;
            font-weight: 700;
            margin-bottom: 1rem;
        }

        .stButton > button {
            background: linear-gradient(90deg, #10b981, #059669);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.6rem 1.8rem;
        }

        .stButton > button:hover {
            background: linear-gradient(90deg, #059669, #047857);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown('<h1 class="main-title">⚡ Smart Home Energy Automation & Dynamic Load Shedding</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Live Telemetry Simulator • n8n Webhook Engine • Automated Gmail Alerts</p>', unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.header("⚙️ Telemetry Controls")

webhook_url = st.sidebar.text_input(
    "n8n Webhook URL",
    value="http://localhost:5678/webhook-test/smart-home-telemetry",
    help="Copy the Webhook URL from your n8n Webhook node"
)

user_email = st.sidebar.text_input("Alert Recipient Email", value="wajihahareed00@gmail.com")

st.sidebar.subheader("🔌 Meter Simulator")
power_w = st.sidebar.slider("Active Power (Watts)", min_value=100, max_value=5000, value=2600, step=100)
voltage_v = st.sidebar.slider("Voltage (V)", min_value=180, max_value=250, value=230)
current_a = st.sidebar.number_input("Current (A)", value=round(power_w / voltage_v, 2))
accumulated_kwh = st.sidebar.number_input("Accumulated Energy (kWh)", value=14.2)

# Session state for tracking history
if "history" not in st.session_state:
    st.session_state.history = []

# Main Trigger Button
if st.button("🚀 Send Telemetry to n8n Engine"):
    payload = {
        "device_id": "SMART-METER-01",
        "active_power_w": power_w,
        "voltage_v": voltage_v,
        "current_a": current_a,
        "accumulated_energy_kwh": accumulated_kwh,
        "email": user_email
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        if response.status_code == 200:
            res_data = response.json()
            
            # Fix: Handle if n8n returns a list instead of a dict
            if isinstance(res_data, list) and len(res_data) > 0:
                res_data = res_data[0]
            
            st.session_state.history.append(res_data)
            st.success("Telemetry successfully processed by n8n Workflow!")
        else:
            st.error(f"n8n returned status code {response.status_code}. Make sure workflow is active!")
    except Exception as e:
        st.error(f"Could not connect to n8n Webhook. Error: {e}")

# Display Latest Result
if st.session_state.history:
    latest = st.session_state.history[-1]

    st.subheader("📊 Engine Evaluation Metrics")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Power Load", f"{latest.get('power_w', 0)} W")
    col2.metric("Peak Power Budget", f"{latest.get('power_limit_w', 0)} W")
    col3.metric("Est. Hourly Cost", f"${latest.get('hourly_cost_usd', 0)}")
    col4.metric("CO2 Footprint", f"{latest.get('co2_kg_per_hr', 0)} kg/h")

    # Overload Status Box
    if latest.get("is_overloaded", False):
        st.markdown(
            f'<div class="status-critical">🚨 OVERLOAD CRITICAL: Power load of {latest.get("power_w")}W exceeds budget limit of {latest.get("power_limit_w")}W! Auto-shedding triggered & Gmail Alert dispatched.</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="status-healthy">✅ SYSTEM HEALTHY: Consumption of {latest.get("power_w")}W is within the safe limit.</div>',
            unsafe_allow_html=True
        )

    st.divider()

    # Historical Telemetry Visualization
    st.subheader("📈 Telemetry Analytics History")
    df = pd.DataFrame(st.session_state.history)

    fig = px.line(
        df,
        x="timestamp",
        y="power_w",
        title="Live Power Consumption (Watts)",
        markers=True,
        color_discrete_sequence=["#10b981"]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e6edf3"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Audit Log Table")
    st.dataframe(df[["timestamp", "power_w", "voltage_v", "power_limit_w", "is_overloaded", "hourly_cost_usd"]], use_container_width=True)
else:
    st.info("👈 Set telemetry values on the sidebar and click 'Send Telemetry to n8n Engine' to start evaluating!")