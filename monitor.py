import streamlit as st
import time
import os

st.title("🔥 Hot Melting Iron: Live Sync Monitor")


# Function to read your automation logs
def get_logs():
    if os.path.exists("sync.log"):
        with open("sync.log", "r") as f:
            return f.readlines()[-10:]  # Get last 10 lines
    return ["No logs found..."]


placeholder = st.empty()

while True:
    with placeholder.container():
        st.subheader("Current Activity")
        logs = get_logs()
        for line in logs:
            st.text(line.strip())

        st.progress(100)  # You can tie this to actual progress logic
    time.sleep(2)  # Refresh every 2 seconds
