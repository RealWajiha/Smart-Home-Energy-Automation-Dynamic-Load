

# ⚡ Smart Home Energy Automation & Dynamic Load Shedding

An interactive, end-to-end smart home energy monitoring and automation system built with **Python (Streamlit)** and **n8n Workflows**. This project simulates real-time smart meter telemetry, evaluates Time-of-Use (TOU) tariffs, detects power overload conditions, and triggers automated Gmail alerts—all without requiring any physical hardware or MQTT broker setup.

---

## 🚀 Key Features

* **Live Telemetry Simulator (Streamlit):** Control active power (Watts), voltage, current, and accumulated energy using an intuitive dark-themed UI.
* **n8n Webhook Processing Engine:** Seamlessly receives telemetry data via HTTP POST webhooks, calculates hourly costs, and estimates CO2 emissions.
* **Dynamic Load Shedding & Tariff Evaluation:** Automatically applies peak-hour tariff rules and checks if power consumption exceeds safe budget thresholds.
* **Automated Email Alerts (Gmail Node):** Instantly dispatches critical emergency alerts via Gmail when a power overload is detected.
* **Interactive Analytics & Audit Logs:** Visualize live power consumption trends using Plotly charts and review historical audit data in a clean data table.

---

## 🛠️ Tech Stack

* **Front-End / UI:** Python, Streamlit, Plotly, Pandas
* **Automation & Workflow Engine:** n8n (Webhooks, Code Nodes, IF Conditionals, Gmail Integration)
* **Communication Protocol:** HTTP REST Webhooks (JSON payload exchange)

---

## 📂 Project Architecture

1. **User Input:** The user adjusts power/voltage sliders on the **Streamlit** dashboard.
2. **Webhook Dispatch:** Clicking the trigger button sends a JSON payload to the **n8n Webhook URL**.
3. **Evaluation:** The n8n Code node calculates tariffs, costs, and checks for overloads.
4. **Response & Action:** 
   * Processed data is instantly returned to Streamlit via **Respond to Webhook** to render live metrics and charts.
   * If overloaded, n8n triggers the **Gmail node** to send an alert email.

---

## ⚙️ Setup & Installation Guide

### 1. Clone the Repository
```bash
git clone [https://github.com/RealWajiha/smart-home-energy-automation.git](https://github.com/RealWajiha/smart-home-energy-automation.git)
cd smart-home-energy-automation
```

### 2. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install streamlit requests pandas plotly
```

### 3. Configure n8n Workflow
1. Open your **n8n** dashboard.
2. Create a new workflow and import the workflow JSON file.
3. Configure your **Gmail node** credentials inside n8n.
4. Copy your **Webhook URL** (Test or Production URL).
5. Turn the workflow status to **Active / Published**.

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
* Open the local URL provided in your terminal (usually `http://localhost:8501`).
* Paste your n8n Webhook URL in the sidebar, adjust your telemetry metrics, and test the automation engine!

---

## 👩‍💻 Author
**Wajiha Fareed**
GitHub: [RealWajiha](https://github.com/RealWajiha)
