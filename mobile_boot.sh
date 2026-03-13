#!/bin/bash

# ⚡ Bolt: Automated VisionOps Mobile Startup
echo "🚀 Initializing VisionOps Command Center..."

# 1. Activate the Performance Environment
source vision-env/bin/activate

# 2. Start the Background Sync (The MQL5 Bridge/Simulator)
# We run this in the background (&) so the dashboard can start too.
python simulate_melt.py &
SIM_PID=$!
echo "✅ Simulator started [PID: $SIM_PID]"

# 3. Start the High-Speed Monitor
echo "📊 Launching Streamlit Monitor on Port 8501..."
streamlit run monitor.py --server.port=8501 --server.headless=true

# Cleanup on exit
trap "kill $SIM_PID" EXIT
