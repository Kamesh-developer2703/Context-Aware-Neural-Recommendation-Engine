import os
import pandas as pd
import torch

from ann.model import TwoTowerModel


class RecommendationEngine:

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

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        print("Recommendation Engine Device:", self.device)

        if torch.cuda.is_available():
            print(
                "GPU:",
                torch.cuda.get_device_name(0)
            )

        # -----------------------------
        # Load model
        # -----------------------------

        self.model = TwoTowerModel().to(self.device)

        model_path = "models/two_tower_model_v2.pth"

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model not found: {model_path}"
            )

        self.model.load_state_dict(
            torch.load(
                model_path,
                map_location=self.device
            )
        )

        self.model.eval()

        print("Two Tower model loaded.")

        # -----------------------------
        # Load customers
        # -----------------------------

        self.customers = pd.read_csv(
            "data/processed/customer_features_encoded.csv"
        )

        self.customers["customer_id"] = (
            self.customers["customer_id"].astype(str)
        )

        # -----------------------------
        # Load articles
        # -----------------------------

        self.articles = pd.read_csv(
            "outputs/encoded/article_encoded.csv"
        )

        # -----------------------------
        # Prepare article tensors
        # -----------------------------

        article_values = (
            self.articles[self.ARTICLE_FEATURES]
            .fillna(0)
            .values
        )

        self.article_tensor = torch.tensor(
            article_values,
            dtype=torch.float32,
            device=self.device
        )

        print(
            "Loaded articles:",
            len(self.articles)
        )

        # -----------------------------
        # Pre-compute article embeddings
        # -----------------------------

        print("Generating article embeddings...")

        with torch.no_grad():

            self.article_embeddings = (
                self.model.article_tower(
                    self.article_tensor
                )
            )

        print(
            "Article embeddings ready:",
            self.article_embeddings.shape
        )

    # -----------------------------------------
    # Find customer
    # -----------------------------------------

    def get_customer(self, customer_id):

        customer_id = str(customer_id)

        customer = self.customers[
            self.customers["customer_id"] == customer_id
        ]

        if customer.empty:
            return None

        return customer.iloc[0]

    # -----------------------------------------
    # Generate recommendations
    # -----------------------------------------

    def recommend(
        self,
        customer_id,
        limit=10
    ):

        customer = self.get_customer(customer_id)

        if customer is None:
            return None

        customer_values = [
            customer[column]
            for column in self.CUSTOMER_FEATURES
        ]

        customer_tensor = torch.tensor(
            [customer_values],
            dtype=torch.float32,
            device=self.device
        )

        # Customer embedding
        with torch.no_grad():

            customer_embedding = (
                self.model.customer_tower(
                    customer_tensor
                )
            )

            # Compare customer with ALL articles
            scores = torch.matmul(
                self.article_embeddings,
                customer_embedding.T
            ).squeeze(1)

            limit = min(
                int(limit),
                len(scores)
            )

            top_scores, top_indices = torch.topk(
                scores,
                k=limit
            )

        results = []

        for score, index in zip(
            top_scores.cpu().tolist(),
            top_indices.cpu().tolist()
        ):

            article_id = int(
                self.articles.iloc[index]["article_id"]
            )

            results.append({
                "customer_id": customer_id,
                "article_id": article_id,
                "score": float(score)
            })

        return results


# -----------------------------------------
# Singleton engine
# -----------------------------------------

_engine = None


def get_engine():

    global _engine

    if _engine is None:
        _engine = RecommendationEngine()

    return _engine


def get_dynamic_recommendations(
    customer_id,
    limit=10
):

    engine = get_engine()

    return engine.recommend(
        customer_id,
        limit
    )