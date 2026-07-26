import os
import faiss
import numpy as np
import pandas as pd
import torch

from models.two_tower_model import TwoTowerModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FEATURE_DIR = os.path.join(BASE_DIR, "data", "features")
MODEL_PATH = os.path.join(BASE_DIR, "saved_models", "two_tower_model.pth")

ITEM_FILE = os.path.join(FEATURE_DIR, "item_features.csv")

item_df = pd.read_csv(ITEM_FILE)

# Keep numeric features only
item_numeric = item_df.select_dtypes(include=[np.number])

item_tensor = torch.tensor(
    item_numeric.values.astype(np.float32)
)

model = TwoTowerModel(
    user_dim=5,
    item_dim=item_tensor.shape[1]
)

model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
model.eval()

with torch.no_grad():
    embeddings = model.candidate_tower(item_tensor).numpy()

os.makedirs("embeddings", exist_ok=True)
np.save("embeddings/item_embeddings.npy", embeddings)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

os.makedirs("ann", exist_ok=True)
faiss.write_index(index, "ann/item_index.faiss")

print("FAISS Index Created Successfully!")
print("Total Items :", index.ntotal)