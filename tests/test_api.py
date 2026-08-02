import requests

BASE = "http://127.0.0.1:8000"

try:
    print("Testing Home")
    print(requests.get(BASE).json())

    print("\nTesting Health")
    print(requests.get(BASE + "/health").json())

    print("\nTesting Recommendations")
    print(requests.get(BASE + "/recommendations").json())

    print("\nTesting Customer")
    print(requests.get(BASE + "/recommendations/101").json())

except requests.exceptions.ConnectionError:
    print("❌ FastAPI server is not running.")
    print("Start it using:")
    print("python -m uvicorn api.main:app --reload")