import pandas as pd
import torch
from torch.utils.data import Dataset


class RecommendationDataset(Dataset):

    def __init__(self):

        customers = pd.read_csv("outputs/encoded/customer_encoded.csv")
        transactions = pd.read_csv("outputs/encoded/transaction_encoded.csv")

        self.data = transactions.merge(
            customers,
            on="customer_id",
            how="left"
        )

        print("Dataset Loaded Successfully")
        print("Shape:", self.data.shape)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):

        row = self.data.iloc[idx]

        customer = torch.tensor([
            float(row["age"]),
            float(row["club_member_status"]),
            float(row["fashion_news_frequency"])
        ], dtype=torch.float32)

        article = torch.tensor([
            float(row["average_price_x"]),
            float(row["total_spent_x"]),
            float(row["unique_products_x"])
        ], dtype=torch.float32)

        label = torch.tensor(1.0, dtype=torch.float32)

        return customer, article, label