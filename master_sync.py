import time
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
    print(f"Logged: {log_line.strip()}")

def run_sync():
    initialize_log()
    current_temp = 1100.0  # Starting temperature

    print("INFO: Initializing JULES_API Connection...")
    time.sleep(1)

    print("INFO: Fetching remote: mouyleng172/all-in-one...")
    time.sleep(1)

    print("INFO: Analyzing branch: main...")
    time.sleep(1)

    try:
        print("WARNING: 🔥 HEAT INCREASING: Preparing Hot Melting Iron merge...")
        for _ in range(10):
            # Simulate rising temperature during sync
            current_temp += random.uniform(20.0, 50.0)
            log_temp(current_temp)
            time.sleep(1)

            # Occasionally drop temperature slightly
            if random.random() > 0.7:
                current_temp -= random.uniform(5.0, 15.0)

        print("INFO: Merging unrelated histories...")
        log_temp(current_temp + 10)
        time.sleep(1)

        print("INFO: RESETTING HARD to origin/main...")
        current_temp -= 50
        log_temp(current_temp)
        time.sleep(1)

        print("INFO: Pushing to secondary stream: MQL5...")
        for _ in range(5):
            current_temp += random.uniform(10.0, 30.0)
            log_temp(current_temp)
            time.sleep(1)

        print("SUCCESS: ✅ SYNC COMPLETE.")

        # Cooldown phase
        for _ in range(5):
            current_temp -= random.uniform(40.0, 80.0)
            log_temp(current_temp)
            time.sleep(1)

    except Exception as e:
        print(f"ERROR: Sync failed - {str(e)}")


if __name__ == "__main__":
    run_sync()
