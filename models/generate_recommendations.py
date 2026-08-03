import os
import torch
import pandas as pd

from models.two_tower_model import TwoTowerModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USER_FILE = os.path.join(BASE_DIR, "data", "features", "user_features.csv")
ITEM_FILE = os.path.join(BASE_DIR, "data", "features", "item_features.csv")
MODEL_FILE = os.path.join(BASE_DIR, "saved_models", "two_tower_model_day11.pth")
OUTPUT_FILE = os.path.join(BASE_DIR, "outputs", "recommendations.csv")

TOP_K = 10

print("Loading feature files...")

# users = pd.read_csv(USER_FILE)
# items = pd.read_csv(ITEM_FILE)

users = pd.read_csv(USER_FILE).head(20)
items = pd.read_csv(ITEM_FILE).head(100)

user_numeric = users.select_dtypes(include="number")
item_numeric = items.select_dtypes(include="number")

user_ids = users["customer_id"]
article_ids = items["article_id"]

print("Loading trained model...")

model = TwoTowerModel(
    user_dim=user_numeric.shape[1],
    item_dim=item_numeric.shape[1]
)

model.load_state_dict(
    torch.load(MODEL_FILE, map_location="cpu")
)

model.eval()

recommendations = []

print("Generating recommendations...")

with torch.no_grad():

    for user_index in range(len(user_numeric)):

        user_vector = torch.tensor(
            user_numeric.iloc[user_index].values,
            dtype=torch.float32
        ).unsqueeze(0)

        scores = []

        for item_index in range(len(item_numeric)):

            item_vector = torch.tensor(
                item_numeric.iloc[item_index].values,
                dtype=torch.float32
            ).unsqueeze(0)

            score = model(user_vector, item_vector).item()

            scores.append(
                (
                    article_ids.iloc[item_index],
                    score
                )
            )

        scores.sort(
            key=lambda x: x[1],
            reverse=True
        )

        top_items = scores[:TOP_K]

        for article_id, score in top_items:

            recommendations.append({
                "customer_id": user_ids.iloc[user_index],
                "article_id": article_id,
                "score": score
            })

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

pd.DataFrame(recommendations).to_csv(
    OUTPUT_FILE,
    index=False
)

print("Recommendations generated successfully.")
print(f"Saved to: {OUTPUT_FILE}")