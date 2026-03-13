import csv
import time
import random
import os
from datetime import datetime

LOG_FILE = "sync.log"


def initialize_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("timestamp,temp\n")


def simulate_sensor():
    initialize_log()
    print("Starting Melting Iron Simulation...")
    while True:
        with open(LOG_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            # Simulate a temperature range between 140 and 200
            temp = round(random.uniform(140, 200), 2)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, temp])
            print(f"Logged: {timestamp}, {temp}°C")
        time.sleep(2)


if __name__ == "__main__":
    simulate_sensor()
