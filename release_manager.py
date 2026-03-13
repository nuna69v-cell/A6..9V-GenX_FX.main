import os
import subprocess
import time
from datetime import datetime

import pandas as pd

# --- Configuration ---
LOG_FILE = "sync.log"
CRITICAL_THRESHOLD = 180.0
COOLDOWN_PERIOD = 300  # 5 minutes in seconds
FORGEJO_REPO = "user/hot-iron-project"

last_release_time = 0


def create_forgejo_release(temp):
    """Triggers the Forgejo CLI to create a new release."""
    tag = datetime.now().strftime("overheat-%Y%m%d-%H%M%S")
    title = f"CRITICAL: Temperature Breach {temp}°C"
    note = f"Automated release triggered by MQL5 bridge. Temperature recorded: {temp}°C at {datetime.now()}."

    print(f"🚀 Creating Forgejo Release: {tag}...")

    try:
        # Example command: forgejo-cli release create --repo [repo] --tag [tag] --title [title] --note [note]
        # Adjust arguments based on your specific Forgejo CLI version
        subprocess.run(
            [
                "forgejo-cli",
                "release",
                "create",
                "--repo",
                FORGEJO_REPO,
                "--tag",
                tag,
                "--title",
                title,
                "--note",
                note,
            ],
            check=True,
        )
        print("✅ Release published successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create release: {e}")


def monitor_and_act():
    global last_release_time
    print("👀 Monitoring MQL5 signals for critical events...")

    while True:
        try:
            if os.path.exists(LOG_FILE):
                df = pd.read_csv(LOG_FILE, names=["timestamp", "temp"])
                if not df.empty:
                    current_temp = df.iloc[-1]["temp"]

                    # Check threshold and cooldown
                    current_time = time.time()
                    if current_temp >= CRITICAL_THRESHOLD:
                        if (current_time - last_release_time) > COOLDOWN_PERIOD:
                            create_forgejo_release(current_temp)
                            last_release_time = current_time
                        else:
                            print(
                                f"⚠️ Threshold hit ({current_temp}°C), but in cooldown."
                            )
        except Exception as e:
            print(f"Error reading log: {e}")

        time.sleep(5)  # Check every 5 seconds


if __name__ == "__main__":
    monitor_and_act()
