import requests

BASE = "http://127.0.0.1:8000"

CUSTOMER_ID = "00000dbacae5abe5e23885899a1fa44253a17956c6d1c3d25f88aa139fdfc657"

try:
    print("Testing Home")
    print(requests.get(BASE).json())

    print("\nTesting Health")
    print(requests.get(BASE + "/health").json())

    print("\nTesting Recommendations")
    print(requests.get(BASE + "/recommendations").json())

    print("\nTesting Customer")
    print(
        requests.get(
            BASE + f"/recommendations/{CUSTOMER_ID}"
        ).json()
    )

except requests.exceptions.ConnectionError:
    print("Could not connect to API. Start the server first.")
    print("Start it using:")
    print("python -m uvicorn api.main:app --reload")