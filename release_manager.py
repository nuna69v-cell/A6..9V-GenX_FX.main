import os
import subprocess
import time
import pandas as pd
from datetime import datetime

# --- Configuration via Environment Variables ---
LOG_FILE = "sync.log"
# Fallback to defaults if env vars aren't found
CRITICAL_THRESHOLD = float(os.getenv("CRITICAL_THRESHOLD", 180.0))
FORGEJO_REPO = os.getenv("FORGEJO_REPO")
FORGEJO_TOKEN = os.getenv("FORGEJO_TOKEN")
COOLDOWN_PERIOD = 300

last_release_time = 0


def create_forgejo_release(temp):
    if not FORGEJO_TOKEN:
        print("❌ Error: FORGEJO_TOKEN not set. Cannot create release.")
        return

    tag = datetime.now().strftime("overheat-%Y%m%d-%H%M%S")
    title = f"CRITICAL: {temp}°C Breach"

    print(f"🚀 Triggering Forgejo Release for {tag}...")

    try:
        # Using environment variables in the subprocess call
        # Some CLIs accept tokens via ENV or flags
        env = os.environ.copy()
        env["FORGEJO_AUTH_TOKEN"] = FORGEJO_TOKEN

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
            ],
            check=True,
            env=env,
        )
        print("✅ Release successful.")
    except Exception as e:
        print(f"❌ Release failed: {e}")


def monitor_loop():
    global last_release_time
    print("Monitoring started...")
    while True:
        try:
            if os.path.exists(LOG_FILE):
                df = pd.read_csv(LOG_FILE, names=["timestamp", "temp"])
                latest_temp = float(df.iloc[-1]["temp"])

                if latest_temp > CRITICAL_THRESHOLD:
                    current_time = time.time()
                    if current_time - last_release_time > COOLDOWN_PERIOD:
                        print(f"⚠️ Critical temperature detected: {latest_temp}")
                        create_forgejo_release(latest_temp)
                        last_release_time = current_time
            time.sleep(5)
        except Exception as e:
            print(f"Error in monitor loop: {e}")
            time.sleep(5)


if __name__ == "__main__":
    monitor_loop()
