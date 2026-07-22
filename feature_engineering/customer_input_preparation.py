import pandas as pd

# Load encoded customer features
customers = pd.read_csv("../data/processed/customer_features_encoded.csv")

print("Dataset Shape:", customers.shape)

# Features required for the customer tower
required_features = [
    "FN",
    "Active",
    "age",
    "is_active_member",
    "receives_fashion_news",
    "is_active_customer",
    "club_member_status_encoded",
    "fashion_news_frequency_encoded",
    "age_group_encoded"
]

# Check for missing columns
missing_columns = [col for col in required_features if col not in customers.columns]

if missing_columns:
    print("Missing Columns:", missing_columns)
else:
    print("All required columns are available.")

# Check for missing values
print("\nMissing Values:")
print(customers[required_features].isnull().sum())

# Create customer input dataset
customer_inputs = customers[required_features]

# Save input dataset
customer_inputs.to_csv(
    "../data/processed/customer_model_input.csv",
    index=False
)

print("\nCustomer input preparation completed successfully!")