import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader

CUSTOMER_FILE = "data/processed/customer_features_encoded.csv"
TRANSACTION_FILE = "data/raw/transactions_train.csv"

# Features required for training
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

print("Loading customer features...")

customers = pd.read_csv(
    CUSTOMER_FILE,
    usecols=["customer_id"] + feature_columns
)

print("Customers Shape:", customers.shape)


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


# Process transactions in chunks
chunk_size = 100000
total_samples = 0

print("Processing transactions in chunks...")

for transactions in pd.read_csv(
    TRANSACTION_FILE,
    usecols=["customer_id"],
    chunksize=chunk_size
):

    merged = transactions.merge(
        customers,
        on="customer_id",
        how="left"
    )

    merged[feature_columns] = merged[feature_columns].fillna(0)

    dataset = CustomerDataset(merged)

    loader = DataLoader(
        dataset,
        batch_size=64,
        shuffle=True
    )

    total_samples += len(dataset)

    print(
        f"Processed chunk: {len(dataset)} samples | "
        f"Total: {total_samples}"
    )

    # Test first batch only
    for batch in loader:
        print("Batch Shape:", batch.shape)
        break

print("Total Samples:", total_samples)
print("Dataset Loader Ready!")