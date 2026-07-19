import pandas as pd

# Load dataset
customers = pd.read_csv("../data/raw/customers.csv")

print("Original Dataset Shape:", customers.shape)

# Check missing values
print("\nMissing Values:")
print(customers.isnull().sum())

# Fill missing values

# FN and Active -> replace missing with 0
customers["FN"] = customers["FN"].fillna(0)
customers["Active"] = customers["Active"].fillna(0)

# club_member_status -> replace missing with UNKNOWN
customers["club_member_status"] = customers["club_member_status"].fillna("UNKNOWN")

# fashion_news_frequency -> replace missing with NONE
customers["fashion_news_frequency"] = customers["fashion_news_frequency"].fillna("NONE")

# age -> replace missing with median age
customers["age"] = customers["age"].fillna(customers["age"].median())

# Check duplicates
print("\nDuplicate Rows:", customers.duplicated().sum())

# Save cleaned dataset
customers.to_csv("../data/processed/customers_cleaned.csv", index=False)

print("\nCleaning Completed Successfully!")