import csv
import os
from datetime import datetime

LOG_FILE = "outputs/logs/api_requests.csv"

os.makedirs("outputs/logs", exist_ok=True)

def log_request(endpoint, customer_id, status):

    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "endpoint",
                "customer_id",
                "status"
            ])

        writer.writerow([
            datetime.now(),
            endpoint,
            customer_id,
            status
        ])