import os
import pandas as pd
import torch

from models.dataset import RecommendationDataset
from models.two_tower_model import TwoTowerModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

dataset = RecommendationDataset()

user, item, _ = dataset[0]

model = TwoTowerModel(
    user_dim=user.shape[0],
    item_dim=item.shape[0]
).to(device)
model_path = "saved_models/two_tower_model.pth"

if not os.path.exists(model_path):
    raise FileNotFoundError(f"{model_path} not found")

model.load_state_dict(
    torch.load(model_path, map_location=device)
)

model.eval()

results = []

print("Running inference...")

with torch.no_grad():

    test_indices = [0, 100, 500, 1000, 2000]

    for i in test_indices:

        if i >= len(dataset):
            continue

        user, item, label = dataset[i]

        user, item, label = dataset[i]

        score = torch.sigmoid(
            model(
                user.unsqueeze(0).to(device),
                item.unsqueeze(0).to(device)
            )
        ).item()

        results.append({
            "sample_id": i,
            "score": score
        })

os.makedirs("outputs", exist_ok=True)

pd.DataFrame(results).to_csv(
    "outputs/recommendations.csv",
    index=False
)

print("Recommendations saved to outputs/recommendations.csv")