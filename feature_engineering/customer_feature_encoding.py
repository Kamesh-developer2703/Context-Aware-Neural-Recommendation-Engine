import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load customer features
customers = pd.read_csv("../data/processed/customer_features.csv")

# Create LabelEncoder object
encoder = LabelEncoder()

# Encode Club Member Status
customers["club_member_status_encoded"] = encoder.fit_transform(
    customers["club_member_status"].astype(str)
)

# Encode Fashion News Frequency
customers["fashion_news_frequency_encoded"] = encoder.fit_transform(
    customers["fashion_news_frequency"].astype(str)
)

# Encode Age Group
customers["age_group_encoded"] = encoder.fit_transform(
    customers["age_group"].astype(str)
)

# Save encoded dataset
customers.to_csv("../data/processed/customer_features_encoded.csv", index=False)

print("Customer feature encoding completed successfully!")
df = pd.read_csv("../data/processed/customer_features_encoded.csv")
print(df.head())
print(df.columns)
