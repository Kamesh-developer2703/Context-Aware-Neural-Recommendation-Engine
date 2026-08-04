import time
import requests

URL = "http://127.0.0.1:8000/recommendations"

start = time.time()

response = requests.get(URL)

end = time.time()

print("=" * 40)
print("API Performance Test")
print("=" * 40)

print("Status Code :", response.status_code)
print(f"Response Time : {(end-start):.4f} seconds")