import torch
import pandas as pd

from model import TwoTowerModel

model = TwoTowerModel()

model.load_state_dict(torch.load("models/two_tower_model.pth"))
model.eval()

customers = pd.read_csv("outputs/encoded/customer_encoded.csv")
articles = pd.read_csv("outputs/encoded/article_encoded.csv")

user = customers.iloc[0]

customer_tensor = torch.tensor([
    user["age"],
    user["club_member_status"],
    user["fashion_news_frequency"]
], dtype=torch.float32)

scores = []

for _, article in articles.iterrows():

    article_tensor = torch.tensor([
        article["average_price"],
        article["total_spent"],
        article["unique_products"]
    ], dtype=torch.float32)

    with torch.no_grad():

        score = model(
            customer_tensor.unsqueeze(0),
            article_tensor.unsqueeze(0)
        )

    scores.append(score.item())

    articles["score"] = scores

    top10 = articles.sort_values(
    by="score",
    ascending=False
).head(10)

print(top10)

top10.to_csv(
    "outputs/recommendations.csv",
    index=False
)

print("Recommendations saved!")