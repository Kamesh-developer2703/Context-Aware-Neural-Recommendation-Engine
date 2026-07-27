import pandas as pd
import torch

from model import TwoTowerModel


# -----------------------------
# Load Model
# -----------------------------
model = TwoTowerModel()

model.load_state_dict(
    torch.load("models/two_tower_model_v2.pth")
)

model.eval()

print("Model Loaded Successfully!")


# -----------------------------
# Load Encoded Data
# -----------------------------
customers = pd.read_csv("outputs/encoded/customer_encoded.csv")
articles = pd.read_csv("outputs/encoded/article_encoded.csv")

print("Encoded data loaded.")


# -----------------------------
# Select Customer
# -----------------------------
customer_id = customers.iloc[0]["customer_id"]

customer = customers[
    customers["customer_id"] == customer_id
].iloc[0]

customer_tensor = torch.tensor([[
    customer["age"],
    customer["club_member_status"],
    customer["fashion_news_frequency"],
    customer["FN"],
    customer["Active"]
]], dtype=torch.float32)


# -----------------------------
# Score Every Article
# -----------------------------
recommendations = []

for _, article in articles.iterrows():

    article_tensor = torch.tensor([[
        article["product_type_no"],
        article["graphical_appearance_no"],
        article["colour_group_code"],
        article["department_no"],
        article["index_group_no"],
        article["section_no"],
        article["garment_group_no"],
        article["product_name_length"],
        article["description_length"]
    ]], dtype=torch.float32)

    with torch.no_grad():

        score = model(
            customer_tensor,
            article_tensor
        ).item()

    recommendations.append(
        (
            article["article_id"],
            score
        )
    )


# -----------------------------
# Sort Recommendations
# -----------------------------
recommendations.sort(
    key=lambda x: x[1],
    reverse=True
)

top10 = recommendations[:10]


# -----------------------------
# Display
# -----------------------------
print("\nCustomer ID")
print(customer_id)

print("\nTop 10 Recommendations\n")

for i, (article, score) in enumerate(top10, start=1):

    print(
        f"{i}. {article}  Score: {score:.4f}"
    )


# -----------------------------
# Save CSV
# -----------------------------
df = pd.DataFrame(
    top10,
    columns=[
        "article_id",
        "score"
    ]
)

df.to_csv(
    "outputs/recommendations.csv",
    index=False
)

print("\nRecommendations saved to outputs/recommendations.csv")