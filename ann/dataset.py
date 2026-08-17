import pandas as pd
import torch

from torch.utils.data import Dataset
import random


class RecommendationDataset(Dataset):

    def __init__(self):

        print("Loading encoded datasets...")

        customers = pd.read_csv(
            "data/processed/customer_features_encoded.csv"
        )

        articles = pd.read_csv(
            "outputs/encoded/article_encoded.csv"
        )

        transactions = pd.read_csv(
            "outputs/encoded/transaction_encoded.csv"
        )

        print("Preparing customer features...")

        customers = customers[
            [
                "customer_id",
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
        ].copy()

        print("Preparing article features...")

        articles = articles[
            [
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
        ].copy()

        # ------------------------------------------------
        # Customer feature scaling
        # ------------------------------------------------

        customer_features = [
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

        # Normalize age
        customers["age"] = (
            customers["age"] / 100.0
        )

        # ------------------------------------------------
        # Article feature scaling
        # ------------------------------------------------

        article_features = [
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

        # Min-max normalization
        for column in article_features:

            min_value = articles[column].min()
            max_value = articles[column].max()

            if max_value != min_value:

                articles[column] = (
                    articles[column] - min_value
                ) / (
                    max_value - min_value
                )

            else:

                articles[column] = 0.0

        print("Generating negative samples...")

        article_ids = articles[
            "article_id"
        ].tolist()

        positive_pairs = set(
            zip(
                transactions["customer_id"],
                transactions["article_id"]
            )
        )

        negative_samples = []

        # Create one negative for each positive
        for _, row in transactions.iterrows():

            customer = row["customer_id"]

            while True:

                article = random.choice(
                    article_ids
                )

                if (
                    customer,
                    article
                ) not in positive_pairs:

                    negative_samples.append({
                        "customer_id": customer,
                        "article_id": article,
                        "label": 0
                    })

                    break

        negative_df = pd.DataFrame(
            negative_samples
        )

        positive_df = transactions[
            [
                "customer_id",
                "article_id",
                "label"
            ]
        ]

        data = pd.concat(
            [
                positive_df,
                negative_df
            ],
            ignore_index=True
        )

        print("Merging customer features...")

        data = data.merge(
            customers,
            on="customer_id",
            how="left"
        )

        print("Merging article features...")

        data = data.merge(
            articles,
            on="article_id",
            how="left"
        )

        data.fillna(
            0,
            inplace=True
        )

        self.data = data.sample(
            frac=1,
            random_state=42
        ).reset_index(
            drop=True
        )

        print("\nDataset Ready")

        print(
            self.data["label"].value_counts()
        )

    def __len__(self):

        return len(self.data)

    def __getitem__(self, idx):

        row = self.data.iloc[idx]

        customer = torch.tensor(
            [
                row["FN"],
                row["Active"],
                row["age"],
                row["is_active_member"],
                row["receives_fashion_news"],
                row["is_active_customer"],
                row["club_member_status_encoded"],
                row["fashion_news_frequency_encoded"],
                row["age_group_encoded"]
            ],
            dtype=torch.float32
        )

        article = torch.tensor(
            [
                row["product_type_no"],
                row["graphical_appearance_no"],
                row["colour_group_code"],
                row["department_no"],
                row["index_group_no"],
                row["section_no"],
                row["garment_group_no"],
                row["product_name_length"],
                row["description_length"]
            ],
            dtype=torch.float32
        )

        label = torch.tensor(
            row["label"],
            dtype=torch.float32
        )

        return (
            customer,
            article,
            label
        )