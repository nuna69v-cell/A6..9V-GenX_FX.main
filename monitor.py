import streamlit as st
import pandas as pd
import time
import os

# --- CONFIGURATION ---
CRITICAL_TEMP = 1450
WARNING_TEMP = 1200
LOG_FILE = "sync.log"

st.set_page_config(page_title="Iron Sync Monitor", layout="wide")

def get_alert_styles(temp):
    """Returns CSS based on temperature thresholds."""
    if temp >= CRITICAL_TEMP:
        return "background-color: #ff4b4b; color: white;", "🚨 CRITICAL OVERHEAT"
    elif temp >= WARNING_TEMP:
        return "background-color: #ffa500; color: black;", "⚠️ WARNING: HIGH TEMP"
    else:
        return "background-color: #0e1117; color: white;", "✅ SYSTEM STABLE"

# UI Header
st.title("🔥 Hot Melting Iron Live Monitor")
placeholder = st.empty()

while True:
    try:
        if not os.path.exists(LOG_FILE):
            st.error(f"Waiting for {LOG_FILE} to be created...")
            time.sleep(1)
            continue

        df = pd.read_csv(LOG_FILE, names=["timestamp", "temp"], header=0)
        if not df.empty:
            current_temp = float(df['temp'].iloc[-1])
            prev_temp = float(df['temp'].iloc[-2]) if len(df) > 1 else current_temp

            style, status_msg = get_alert_styles(current_temp)
            delta = current_temp - prev_temp

            with placeholder.container():
                # Inject Dynamic CSS for Alert Background
                st.markdown(f"""
                    <style>
                    .stApp {{
                        {style}
                        transition: background-color 0.5s ease;
                    }}
                    </style>
                    """, unsafe_allow_html=True)

                # Dashboard Layout
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Current Iron Temp", f"{current_temp:.1f}°C", delta=f"{delta:.1f}°C")
                with col2:
                    st.header(status_msg)

                # Live Chart
                st.line_chart(df.set_index('timestamp')['temp'])

                # Table View
                st.subheader("Recent Sync Data")
                st.dataframe(df.tail(10), use_container_width=True)

    except Exception as e:
        st.error(f"Error reading sync.log: {e}")

    time.sleep(1)
