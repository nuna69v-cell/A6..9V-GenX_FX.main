import time
import sys
import datetime
import random
import os

LOG_FILE = "sync.log"

def initialize_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("timestamp,temp\n")

def log_temp(temp):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp},{temp:.1f}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_line)
        f.flush()

def simulate_hot_melt():
    tasks = [
        "Initializing JULES_API Connection...",
        "Fetching remote: mouyleng172/all-in-one...",
        "Analyzing branch: main...",
        "🔥 HEAT INCREASING: Preparing Hot Melting Iron merge...",
        "Merging unrelated histories...",
        "RESETTING HARD to origin/main...",
        "Pushing to secondary stream: MQL5...",
        "✅ SYNC COMPLETE.",
    ]

    initialize_log()
    current_temp = 1150.0

    print("--- STARTING LIVE SIMULATION ---")
    for i, task in enumerate(tasks):
        # Progress bar simulation
        progress = (i + 1) / len(tasks)
        bar = "█" * int(progress * 20) + "-" * (20 - int(progress * 20))

        sys.stdout.write(f"\r[{bar}] {task}")
        sys.stdout.flush()

        # Simulate temperature changes based on the task
        if "HEAT INCREASING" in task or "Merging" in task:
            # Heat up rapidly during merge
            for _ in range(3):
                current_temp += random.uniform(50.0, 120.0)
                log_temp(current_temp)
                time.sleep(0.5)
        elif "RESETTING" in task:
            # Cool down
            for _ in range(2):
                current_temp -= random.uniform(30.0, 60.0)
                log_temp(current_temp)
                time.sleep(0.75)
        else:
            # Slow heat or cool down
            current_temp += random.uniform(-10.0, 25.0)
            log_temp(current_temp)
            time.sleep(1.5)

    print("\n\nSimulation finished. System is stable.")

    # Final cool down
    for _ in range(5):
        current_temp -= random.uniform(30.0, 60.0)
        log_temp(current_temp)
        time.sleep(0.5)

if __name__ == "__main__":
    simulate_hot_melt()
