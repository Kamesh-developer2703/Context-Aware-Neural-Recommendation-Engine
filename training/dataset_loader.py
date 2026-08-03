import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader

# Load datasets
customers = pd.read_csv("../data/processed/customer_features_encoded.csv")
transactions = pd.read_csv("../data/raw/transactions_train.csv")

print("Customers Shape:", customers.shape)
print("Transactions Shape:", transactions.shape)

# Merge datasets
merged = transactions.merge(
    customers,
    on="customer_id",
    how="left"
)

print("Merged Shape:", merged.shape)

# Features for training
feature_columns = [
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

# Replace missing values
merged[feature_columns] = merged[feature_columns].fillna(0)

# Custom Dataset
class CustomerDataset(Dataset):

    def __init__(self, dataframe):
        self.features = torch.tensor(
            dataframe[feature_columns].values,
            dtype=torch.float32
        )

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx]

dataset = CustomerDataset(merged)

loader = DataLoader(
    dataset,
    batch_size=64,
    shuffle=True
)

print("Total Samples:", len(dataset))

for batch in loader:
    print("Batch Shape:", batch.shape)
    break

print("Dataset Loader Ready!")