import asyncio
import time
from typing import List

import httpx

# Configuration for the load test
API_URL = "http://127.0.0.1:8000"
API_KEY = "test_api_key_12345"
CONCURRENT_USERS = 50
TOTAL_SIGNALS = 5000


async def send_signals(
    client: httpx.AsyncClient, num_signals: int, user_id: int
) -> List[float]:
    """Send a batch of signals and record response times."""
    latencies = []

    for i in range(num_signals):
        signal = {
            "signal_id": f"LOAD_TEST_U{user_id}_{i}",
            "instrument": "EURUSD",
            "action": "BUY" if i % 2 == 0 else "SELL",
            "volume": 0.1,
            "stop_loss": 1.0950,
            "take_profit": 1.1050,
        }

        start_time = time.perf_counter()
        try:
            response = await client.post(
                f"{API_URL}/send_signal", json=signal, headers={"X-API-Key": API_KEY}
            )
            response.raise_for_status()
            latencies.append(time.perf_counter() - start_time)
        except Exception as e:
            print(f"User {user_id} failed to send signal {i}: {e}")

    return latencies


async def run_load_test():
    """Run the concurrent load test against the API."""
    print(
        f"Starting load test: {CONCURRENT_USERS} concurrent users, {TOTAL_SIGNALS} total signals..."
    )

    signals_per_user = TOTAL_SIGNALS // CONCURRENT_USERS

    async with httpx.AsyncClient() as client:
        # Verify API is up
        try:
            await client.get(f"{API_URL}/ping")
        except httpx.ConnectError:
            print(
                f"API is not running at {API_URL}. Start it with: uvicorn api.main:app"
            )
            return

        start_time = time.perf_counter()

        # Create concurrent tasks
        tasks = [
            send_signals(client, signals_per_user, i) for i in range(CONCURRENT_USERS)
        ]

        # Execute all tasks
        results = await asyncio.gather(*tasks)

        total_time = time.perf_counter() - start_time

        # Aggregate results
        all_latencies = []
        for user_latencies in results:
            all_latencies.extend(user_latencies)

        successful_signals = len(all_latencies)

        if not all_latencies:
            print("No signals were successfully sent.")
            return

        avg_latency = sum(all_latencies) / successful_signals * 1000  # ms
        max_latency = max(all_latencies) * 1000
        signals_per_second = successful_signals / total_time

        print("\n--- Load Test Results ---")
        print(f"Total Time: {total_time:.2f} seconds")
        print(f"Successful Signals: {successful_signals}/{TOTAL_SIGNALS}")
        print(f"Throughput: {signals_per_second:.2f} signals/second")
        print(f"Average Latency: {avg_latency:.2f} ms")
        print(f"Max Latency: {max_latency:.2f} ms")


if __name__ == "__main__":
    asyncio.run(run_load_test())
