import time
import concurrent.futures
import requests

BASE_URL = "http://127.0.0.1:8000"
CUSTOMER_ID = 1

REPEATED_REQUESTS = 20
CONCURRENT_REQUESTS = 10


def make_request():
    start = time.perf_counter()

    try:
        response = requests.get(
            f"{BASE_URL}/recommendations/{CUSTOMER_ID}",
            timeout=10,
        )

        elapsed = (time.perf_counter() - start) * 1000

        return {
            "status": response.status_code,
            "time_ms": round(elapsed, 2),
        }

    except requests.RequestException as exc:
        elapsed = (time.perf_counter() - start) * 1000

        return {
            "status": "FAILED",
            "time_ms": round(elapsed, 2),
            "error": str(exc),
        }


def repeated_test():
    print("\n========== REPEATED REQUEST TEST ==========")

    results = [make_request() for _ in range(REPEATED_REQUESTS)]

    successful = [
        result for result in results
        if result["status"] == 200
    ]

    times = [
        result["time_ms"]
        for result in successful
    ]

    print(f"Successful Requests: {len(successful)}/{REPEATED_REQUESTS}")

    if times:
        print(f"Average Response Time: {sum(times) / len(times):.2f} ms")
        print(f"Minimum Response Time: {min(times):.2f} ms")
        print(f"Maximum Response Time: {max(times):.2f} ms")


def concurrent_test():
    print("\n========== CONCURRENT REQUEST TEST ==========")

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=CONCURRENT_REQUESTS
    ) as executor:
        results = list(
            executor.map(
                lambda _: make_request(),
                range(CONCURRENT_REQUESTS),
            )
        )

    successful = [
        result for result in results
        if result["status"] == 200
    ]

    times = [
        result["time_ms"]
        for result in successful
    ]

    print(
        f"Successful Requests: "
        f"{len(successful)}/{CONCURRENT_REQUESTS}"
    )

    if times:
        print(
            f"Average Response Time: "
            f"{sum(times) / len(times):.2f} ms"
        )
        print(
            f"Maximum Response Time: "
            f"{max(times):.2f} ms"
        )


if __name__ == "__main__":
    print("Starting recommendation API performance tests...")
    print(f"Target: {BASE_URL}/recommendations/{CUSTOMER_ID}")

    repeated_test()
    concurrent_test()

    print("\nPerformance testing completed.")