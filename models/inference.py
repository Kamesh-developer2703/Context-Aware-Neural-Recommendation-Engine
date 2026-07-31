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
TOP_K = 10
print("Running inference...")
# Disable gradient computation for faster inference
with torch.no_grad():

    MAX_SAMPLES = min(1000, len(dataset))

    for i in range(MAX_SAMPLES):

        

        user, item, label = dataset[i]

        score = torch.sigmoid(
            model(
                user.unsqueeze(0).to(device),
                item.unsqueeze(0).to(device)
            )
        ).item()
# Store prediction results for evaluation
        results.append({
            "sample_id": i,
            "actual_label": int(label),
            "score": round(score, 4)
    })
# Sort recommendations by score (highest first)
results.sort(key=lambda x: x["score"], reverse=True)

# Keep only Top-K recommendations
top_results = results[:TOP_K]
os.makedirs("outputs", exist_ok=True)

pd.DataFrame(results).to_csv(
    "outputs/recommendations.csv",
    index=False
)
# Save Top-K recommendations separately
pd.DataFrame(top_results).to_csv(
    "outputs/top_k_recommendations.csv",
    index=False
)

print(f"Top-{TOP_K} recommendations saved to outputs/top_k_recommendations.csv")
print("Recommendations saved to outputs/recommendations.csv")