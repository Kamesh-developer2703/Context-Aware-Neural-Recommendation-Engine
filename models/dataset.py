import os
import random
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FEATURE_DIR = os.path.join(BASE_DIR, "data", "features")

USER_FILE = os.path.join(FEATURE_DIR, "user_features.csv")
ITEM_FILE = os.path.join(FEATURE_DIR, "item_features.csv")
TRANSACTION_FILE = os.path.join(FEATURE_DIR, "contextual_features.csv")


class RecommendationDataset(Dataset):

    def __init__(self, negative_ratio=1):

        print("Loading datasets...")

        self.users = pd.read_csv(USER_FILE)
        self.items = pd.read_csv(ITEM_FILE)
        self.transactions = pd.read_csv(TRANSACTION_FILE)

        # Keep only numeric columns
        self.user_numeric = self.users.select_dtypes(include=[np.number])
        self.item_numeric = self.items.select_dtypes(include=[np.number])

        # Mapping IDs to row index
        self.user_index = {
            cid: idx
            for idx, cid in enumerate(self.users["customer_id"])
        }

        self.item_index = {
            aid: idx
            for idx, aid in enumerate(self.items["article_id"])
        }

        print("Generating positive & negative samples...")

        self.samples = []

        all_articles = self.items["article_id"].tolist()

        for _, row in self.transactions.iterrows():

            customer = row["customer_id"]
            article = row["article_id"]

            if (
                customer not in self.user_index
                or article not in self.item_index
            ):
                continue

            # Positive sample
            self.samples.append((customer, article, 1))

            # Generate negative samples
            for _ in range(negative_ratio):

                negative = random.choice(all_articles)

                while negative == article:
                    negative = random.choice(all_articles)

        # This line must be inside the loop
        self.samples.append((customer, negative, 0))

        print(f"Total Samples : {len(self.samples)}")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):

        customer, article, label = self.samples[idx]

        user_row = self.user_numeric.iloc[
            self.user_index[customer]
        ]

        item_row = self.item_numeric.iloc[
            self.item_index[article]
        ]

        user_tensor = torch.tensor(
            user_row.values.astype(np.float32)
        )

        item_tensor = torch.tensor(
            item_row.values.astype(np.float32)
        )

        label_tensor = torch.tensor(
            label,
            dtype=torch.float32
        )

        return user_tensor, item_tensor, label_tensor