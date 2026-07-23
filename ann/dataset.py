import pandas as pd
import torch
from torch.utils.data import Dataset


class RecommendationDataset(Dataset):

    def __init__(self):

        print("Loading encoded datasets...")

        self.customers = pd.read_csv("outputs/encoded/customer_encoded.csv")
        self.articles = pd.read_csv("outputs/encoded/article_encoded.csv")
        self.transactions = pd.read_csv("outputs/encoded/transaction_encoded.csv")

        print("Preparing customer features...")

        '''customer_cols = [
            "customer_id",
            "age",
            "club_member_status",
            "fashion_news_frequency",
            "FN",
            "Active",
            "total_purchases",
            "total_spent",
            "average_price",
            "unique_products"
        ]'''
        customer_cols = [
    "customer_id",
    "age",
    "club_member_status",
    "fashion_news_frequency",
    "FN",
    "Active"
]

        self.customers = self.customers[customer_cols]

        print("Preparing article features...")

        article_cols = [
            "article_id",
            "product_type_no",
            "graphical_appearance_no",
            "colour_group_code",
            "department_no",
            "index_group_no",
            "section_no",
            "garment_group_no",
            "product_name_length",
            "description_length"
        ]

        self.articles = self.articles[article_cols]

        print("Merging customer features...")

        data = self.transactions.merge(
            self.customers,
            on="customer_id",
            how="left"
        )

        print("Merging article features...")

        data = data.merge(
            self.articles,
            on="article_id",
            how="left"
        )

        data.fillna(0, inplace=True)

        self.data = data

        print("\nDataset Ready")
        print("Shape :", self.data.shape)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):

        row = self.data.iloc[idx]

        ''' customer = torch.tensor([
            row["age"],
            row["club_member_status"],
            row["fashion_news_frequency"],
            row["FN"],
            row["Active"],
            row["total_purchases"],
            row["total_spent"],
            row["average_price"],
            row["unique_products"]
        ], dtype=torch.float32) '''

        customer = torch.tensor([
    row["age"],
    row["club_member_status"],
    row["fashion_news_frequency"],
    row["FN"],
    row["Active"]
], dtype=torch.float32)

        article = torch.tensor([
            row["product_type_no"],
            row["graphical_appearance_no"],
            row["colour_group_code"],
            row["department_no"],
            row["index_group_no"],
            row["section_no"],
            row["garment_group_no"],
            row["product_name_length"],
            row["description_length"]
        ], dtype=torch.float32)

        label = torch.tensor(
            row["label"],
            dtype=torch.float32
        )

        return customer, article, label