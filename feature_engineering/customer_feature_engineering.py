import pandas as pd

# Load cleaned customer dataset
customers = pd.read_csv("../data/processed/customers_cleaned.csv")

print("Dataset Shape:", customers.shape)

# --------------------------
# Feature 1: Age Group
# --------------------------

customers["age_group"] = pd.cut(
    customers["age"],
    bins=[0,18,25,35,45,60,100],
    labels=["Teen","Young Adult","Adult","Middle Age","Senior","Elder"]
)

# --------------------------
# Feature 2: Membership Status
# --------------------------

customers["is_active_member"] = customers["club_member_status"].apply(
    lambda x: 0 if x=="UNKNOWN" else 1
)

# --------------------------
# Feature 3: Fashion News
# --------------------------

customers["receives_fashion_news"] = customers["fashion_news_frequency"].apply(
    lambda x: 0 if x=="NONE" else 1
)

# --------------------------
# Feature 4: Active Customer
# --------------------------

customers["is_active_customer"] = customers["Active"].apply(
    lambda x: 1 if x==1 else 0
)

# Save feature dataset
customers.to_csv("../data/processed/customer_features.csv", index=False)

print("Customer Features Generated Successfully!")