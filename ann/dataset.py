import pandas as pd
import torch
from torch.utils.data import Dataset
import random
import joblib


class RecommendationDataset(Dataset):

    CUSTOMER_FEATURES = [
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

    ARTICLE_FEATURES = [
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

        # -----------------------------------------
        # Select customer features
        # -----------------------------------------

        print("Preparing customer features...")

        customers = customers[
            ["customer_id"] + self.CUSTOMER_FEATURES
        ].copy()

        # -----------------------------------------
        # Select article features
        # -----------------------------------------

        print("Preparing article features...")

        articles = articles[
            ["article_id"] + self.ARTICLE_FEATURES
        ].copy()

        # -----------------------------------------
        # Generate negative samples
        # -----------------------------------------

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

        # -----------------------------------------
        # Positive samples
        # -----------------------------------------

        positive_df = transactions[
            [
                "customer_id",
                "article_id",
                "label"
            ]
        ].copy()

        # -----------------------------------------
        # Combine positive + negative
        # -----------------------------------------

        data = pd.concat(
            [
                positive_df,
                negative_df
            ],
            ignore_index=True
        )

        # -----------------------------------------
        # Merge customer features
        # -----------------------------------------

        print("Merging customer features...")

        data = data.merge(
            customers,
            on="customer_id",
            how="left"
        )

        # -----------------------------------------
        # Merge article features
        # -----------------------------------------

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

        # -----------------------------------------
        # Load scalers
        # -----------------------------------------

        print("Loading feature scalers...")

        self.customer_scaler = joblib.load(
            "models/scalers/customer_scaler.pkl"
        )

        self.article_scaler = joblib.load(
            "models/scalers/article_scaler.pkl"
        )

        # -----------------------------------------
        # Scale customer features
        # -----------------------------------------

        print("Scaling customer features...")

        data[self.CUSTOMER_FEATURES] = (
            self.customer_scaler.transform(
                data[self.CUSTOMER_FEATURES]
            )
        )

        # -----------------------------------------
        # Scale article features
        # -----------------------------------------

        print("Scaling article features...")

        data[self.ARTICLE_FEATURES] = (
            self.article_scaler.transform(
                data[self.ARTICLE_FEATURES]
            )
        )

        # -----------------------------------------
        # Shuffle dataset
        # -----------------------------------------

        self.data = data.sample(
            frac=1,
            random_state=42
        ).reset_index(drop=True)

        print("\nDataset Ready")

        print(
            self.data["label"].value_counts()
        )

    def __len__(self):

        return len(self.data)

    def __getitem__(self, idx):

        row = self.data.iloc[idx]

        # -----------------------------------------
        # Customer tensor
        # -----------------------------------------

        customer = torch.tensor(
            row[self.CUSTOMER_FEATURES].values.astype(
                "float32"
            )
        )

        # -----------------------------------------
        # Article tensor
        # -----------------------------------------

        article = torch.tensor(
            row[self.ARTICLE_FEATURES].values.astype(
                "float32"
            )
        )

        # -----------------------------------------
        # Label
        # -----------------------------------------

        label = torch.tensor(
            row["label"],
            dtype=torch.float32
        )

        return customer, article, label