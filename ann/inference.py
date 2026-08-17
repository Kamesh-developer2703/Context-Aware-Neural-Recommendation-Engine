import pandas as pd
import torch

from model import TwoTowerModel


# -----------------------------
# Device
# -----------------------------

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Using device:", device)

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))


# -----------------------------
# Load Model
# -----------------------------

model = TwoTowerModel().to(device)

model.load_state_dict(
    torch.load(
        "models/two_tower_model_v2.pth",
        map_location=device
    )
)

model.eval()

print("Model Loaded Successfully!")


# -----------------------------
# Load Encoded Data
# -----------------------------

customers = pd.read_csv(
    "data/processed/customer_features_encoded.csv"
)

articles = pd.read_csv(
    "outputs/encoded/article_encoded.csv"
)

print("Data loaded successfully.")


# -----------------------------
# Select Customer
# -----------------------------

customer_id = customers.iloc[0]["customer_id"]

customer = customers[
    customers["customer_id"] == customer_id
].iloc[0]


# -----------------------------
# 9 Customer Features
# -----------------------------

customer_tensor = torch.tensor([[
    customer["FN"],
    customer["Active"],
    customer["age"],
    customer["is_active_member"],
    customer["receives_fashion_news"],
    customer["is_active_customer"],
    customer["club_member_status_encoded"],
    customer["fashion_news_frequency_encoded"],
    customer["age_group_encoded"]
]], dtype=torch.float32).to(device)


# -----------------------------
# Score Articles
# -----------------------------

recommendations = []

print("Generating recommendations...")

with torch.no_grad():

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
        ]], dtype=torch.float32).to(device)

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
# Sort
# -----------------------------

recommendations.sort(
    key=lambda x: x[1],
    reverse=True
)

top10 = recommendations[:10]


# -----------------------------
# Display
# -----------------------------

print("\nCustomer ID:")
print(customer_id)

print("\nTop 10 Recommendations:\n")

for i, (article, score) in enumerate(
    top10,
    start=1
):

    print(
        f"{i}. Article: {article}  Score: {score:.4f}"
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

df.insert(
    0,
    "customer_id",
    customer_id
)

df.to_csv(
    "outputs/recommendations.csv",
    index=False
)

print(
    "\nRecommendations saved to "
    "outputs/recommendations.csv"
)