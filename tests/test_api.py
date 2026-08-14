import requests

BASE = "http://127.0.0.1:8000"

CUSTOMER_ID = "00007d2de826758b65a93dd24ce629ed66842531df6699338c5570910a014cc2"

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