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

model.load_state_dict(
    torch.load(
        "saved_models/two_tower_model.pth",
        map_location=device
    )
)

model.eval()

results = []

print("Running inference...")

with torch.no_grad():

    for i in range(min(1000, len(dataset))):

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