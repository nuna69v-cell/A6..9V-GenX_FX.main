import os
from utils import tail_file # Information from our shared utility

# 1. Configuration Information
LOG_FILE = "sync.log"
THRESHOLD = 180.0
REPO_NAME = "Hello-GenX-1041"

def trigger_release(temp):
    print(f"Triggering release at {temp}°C")

def run_mission_control():
    # 2. Logic Information
    print(f"⚡ Bolt: VisionOps Active on {REPO_NAME}")

    for entry in tail_file(LOG_FILE):
        # 3. Data Processing Information
        try:
            timestamp, temp = entry.split(',')
            temp_float = float(temp)

            # 4. Action Information
            if temp_float >= THRESHOLD:
                trigger_release(temp_float) # Calls your Forgejo logic
        except Exception as e:
            continue

if __name__ == "__main__":
    run_mission_control()
