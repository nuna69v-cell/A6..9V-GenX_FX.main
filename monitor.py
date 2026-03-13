import streamlit as st
import pandas as pd
import time
import os

st.set_page_config(page_title="Hot Melting Iron Monitor", layout="wide")

st.title("🔥 Hot Melting Iron Live Monitor")

# Placeholder for the dynamic UI components
placeholder = st.empty()

while True:
    try:
        # Read the CSV log
        if not os.path.exists("sync.log"):
            st.error("Waiting for sync.log to be created...")
            time.sleep(1)
            continue

        df = pd.read_csv("sync.log", names=["timestamp", "temp"], header=0)
        if not df.empty:
            last_row = df.iloc[-1]
            current_temp = float(last_row["temp"])

            # Determine Alert Status
            if current_temp >= 180:
                color = "#FF4B4B"  # Red
                status = "CRITICAL: OVERHEAT"
            elif 160 <= current_temp < 180:
                color = "#FFA500"  # Yellow
                status = "WARNING: HIGH TEMP"
            else:
                color = "#00FF00"  # Green
                status = "STANDARD"

            with placeholder.container():
                # Metric Display
                st.metric(
                    label="Current Temperature",
                    value=f"{current_temp} °C",
                    delta_color="inverse",
                )

                # Custom CSS Alert Box
                st.markdown(
                    f"""
                    <div style="background-color:{color}; padding:20px; border-radius:10px;">
                        <h2 style="color:white; text-align:center;">{status}</h2>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Temperature Trend Chart
                st.subheader("Temperature Trend (Last 20 Readings)")
                # Set index to timestamp for better x-axis rendering
                chart_data = df.tail(20).set_index("timestamp")
                st.line_chart(chart_data["temp"])

                # Raw Data Table
                st.subheader("Recent Sync Data")
                st.dataframe(df.tail(10), use_container_width=True)

    except Exception as e:
        st.error(f"Waiting for data... {e}")

    time.sleep(1)
