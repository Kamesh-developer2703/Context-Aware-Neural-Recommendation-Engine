import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data
DATA_DIR = os.path.join(BASE_DIR, "data")
FEATURE_DIR = os.path.join(DATA_DIR, "features")

# Outputs
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
LOG_DIR = os.path.join(OUTPUT_DIR, "logs")

# Models
MODEL_DIR = os.path.join(BASE_DIR, "saved_models")
MODEL_PATH = os.path.join(MODEL_DIR, "two_tower_model_day11.pth")

# API
HOST = "127.0.0.1"
PORT = 8000
TOP_K = 10

os.makedirs(LOG_DIR, exist_ok=True)