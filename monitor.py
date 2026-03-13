import streamlit as st
import time
import os

st.set_page_config(layout="wide", page_title="Hot Melting Iron")

st.title("🔥 Hot Melting Iron: Live Sync Monitor")

# Function to read your automation logs
def get_logs():
    if os.path.exists("sync.log"):
        with open("sync.log", "r") as f:
            return f.readlines()[-15:]  # Get last 15 lines
    return ["No logs found..."]

placeholder = st.empty()

while True:
    with placeholder.container():
        st.subheader("Current Activity")
        logs = get_logs()

        # Parse logs to check for alerts
        for line in logs:
            line_clean = line.strip()
            if "ERROR" in line_clean:
                st.error(line_clean)
            elif "WARNING" in line_clean or "🔥" in line_clean:
                st.warning(line_clean)
            elif "SUCCESS" in line_clean or "✅" in line_clean:
                st.success(line_clean)
            else:
                st.text(line_clean)

        st.progress(100)  # You can tie this to actual progress logic
    time.sleep(2)  # Refresh every 2 seconds
