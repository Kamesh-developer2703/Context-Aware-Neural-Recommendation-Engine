import os
import joblib
import pandas as pd
import torch
import torch.nn.functional as F

from ann.model import TwoTowerModel


class RecommendationEngine:

    # =========================================================
    # Feature definitions
    # =========================================================

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

    # =========================================================
    # Initialize Recommendation Engine
    # =========================================================

    def __init__(self):

        # -----------------------------------------------------
        # Device
        # -----------------------------------------------------

        self.device = torch.device(
            "cuda" if torch.cuda.is_available()
            else "cpu"
        )

        print(
            "Recommendation Engine Device:",
            self.device
        )

        if torch.cuda.is_available():

            print(
                "GPU:",
                torch.cuda.get_device_name(0)
            )

        # -----------------------------------------------------
        # File paths
        # -----------------------------------------------------

        self.model_path = (
            "models/two_tower_model_v2.pth"
        )

        self.customer_scaler_path = (
            "models/scalers/customer_scaler.pkl"
        )

        self.article_scaler_path = (
            "models/scalers/article_scaler.pkl"
        )

        self.customer_file = (
            "data/processed/"
            "customer_features_encoded.csv"
        )

        self.article_file = (
            "outputs/encoded/"
            "article_encoded.csv"
        )

        # -----------------------------------------------------
        # Validate required files
        # -----------------------------------------------------

        self._check_required_files()

        # -----------------------------------------------------
        # Load model
        # -----------------------------------------------------

        self._load_model()

        # -----------------------------------------------------
        # Load scalers
        # -----------------------------------------------------

        self._load_scalers()

        # -----------------------------------------------------
        # Load data
        # -----------------------------------------------------

        self._load_data()

        # -----------------------------------------------------
        # Generate article embeddings
        # -----------------------------------------------------

        self._generate_article_embeddings()

    # =========================================================
    # Check required files
    # =========================================================

    def _check_required_files(self):

        required_files = [
            self.model_path,
            self.customer_scaler_path,
            self.article_scaler_path,
            self.customer_file,
            self.article_file
        ]

        for file_path in required_files:

            if not os.path.exists(file_path):

                raise FileNotFoundError(
                    f"Required file not found: {file_path}"
                )

    # =========================================================
    # Load Two-Tower model
    # =========================================================

    def _load_model(self):

        print("\nLoading Two-Tower model...")

        self.model = TwoTowerModel().to(
            self.device
        )

        self.model.load_state_dict(
            torch.load(
                self.model_path,
                map_location=self.device
            )
        )

        self.model.eval()

        print(
            "Two Tower model loaded."
        )

    # =========================================================
    # Load feature scalers
    # =========================================================

    def _load_scalers(self):

        print(
            "\nLoading feature scalers..."
        )

        self.customer_scaler = joblib.load(
            self.customer_scaler_path
        )

        self.article_scaler = joblib.load(
            self.article_scaler_path
        )

        print(
            "Customer scaler loaded."
        )

        print(
            "Article scaler loaded."
        )

    # =========================================================
    # Load customer and article data
    # =========================================================

    def _load_data(self):

        print(
            "\nLoading customer data..."
        )

        self.customers = pd.read_csv(
            self.customer_file
        )

        self.customers[
            "customer_id"
        ] = (
            self.customers[
                "customer_id"
            ].astype(str)
        )

        print(
            "Loaded customers:",
            len(self.customers)
        )

        print(
            "\nLoading article data..."
        )

        self.articles = pd.read_csv(
            self.article_file
        )

        print(
            "Loaded articles:",
            len(self.articles)
        )

    # =========================================================
    # Generate article embeddings
    # =========================================================

    def _generate_article_embeddings(self):

        print(
            "\nPreparing article features..."
        )

        # -----------------------------------------------------
        # Select article features
        # -----------------------------------------------------

        article_features = (
            self.articles[
                self.ARTICLE_FEATURES
            ]
            .fillna(0)
        )

        # -----------------------------------------------------
        # Apply SAME scaler used during training
        # -----------------------------------------------------

        article_features_scaled = (
            self.article_scaler.transform(
                article_features
            )
        )

        # -----------------------------------------------------
        # Convert to tensor
        # -----------------------------------------------------

        self.article_tensor = torch.tensor(
            article_features_scaled,
            dtype=torch.float32,
            device=self.device
        )

        print(
            "Article feature tensor:",
            self.article_tensor.shape
        )

        # -----------------------------------------------------
        # Generate embeddings
        # -----------------------------------------------------

        print(
            "\nGenerating article embeddings..."
        )

        with torch.no_grad():

            self.article_embeddings = (
                self.model.article_tower(
                    self.article_tensor
                )
            )

            # -------------------------------------------------
            # Normalize embeddings
            # -------------------------------------------------

            self.article_embeddings = F.normalize(
                self.article_embeddings,
                p=2,
                dim=1
            )

        print(
            "Article embeddings ready:",
            self.article_embeddings.shape
        )

    # =========================================================
    # Find customer
    # =========================================================

    def get_customer(
        self,
        customer_id
    ):

        customer_id = str(
            customer_id
        )

        customer = self.customers[
            self.customers[
                "customer_id"
            ] == customer_id
        ]

        if customer.empty:

            return None

        return customer.iloc[0]

    # =========================================================
    # Generate recommendations
    # =========================================================

    def recommend(
        self,
        customer_id,
        limit=10
    ):

        # -----------------------------------------------------
        # Find customer
        # -----------------------------------------------------

        customer = self.get_customer(
            customer_id
        )

        if customer is None:

            return None

        # -----------------------------------------------------
        # Validate limit
        # -----------------------------------------------------

        try:

            limit = int(limit)

        except (TypeError, ValueError):

            limit = 10

        if limit < 1:

            limit = 10

        limit = min(
            limit,
            len(self.articles)
        )

        # -----------------------------------------------------
        # Get customer features
        # -----------------------------------------------------

        customer_features = (
        customer[
            self.CUSTOMER_FEATURES
        ]
        .fillna(0)
        .infer_objects(copy=False)
        )

        customer_features_scaled = (
            self.customer_scaler.transform(
                customer_features.to_frame().T
            )
        )

        # -----------------------------------------------------
        # Convert customer to tensor
        # -----------------------------------------------------

        customer_tensor = torch.tensor(
            customer_features_scaled,
            dtype=torch.float32,
            device=self.device
        )

        # -----------------------------------------------------
        # Generate customer embedding
        # -----------------------------------------------------

        with torch.no_grad():

            customer_embedding = (
                self.model.customer_tower(
                    customer_tensor
                )
            )

            # -------------------------------------------------
            # Normalize customer embedding
            # -------------------------------------------------

            customer_embedding = F.normalize(
                customer_embedding,
                p=2,
                dim=1
            )

            # -------------------------------------------------
            # Cosine similarity
            # -------------------------------------------------

            scores = torch.matmul(
                self.article_embeddings,
                customer_embedding.T
            ).squeeze(1)

            # -------------------------------------------------
            # Top-K recommendations
            # -------------------------------------------------

            top_scores, top_indices = (
                torch.topk(
                    scores,
                    k=limit
                )
            )

        # -----------------------------------------------------
        # Convert results
        # -----------------------------------------------------

        results = []

        for score, index in zip(
            top_scores.cpu().tolist(),
            top_indices.cpu().tolist()
        ):

            article_id = int(
                self.articles.iloc[
                    index
                ]["article_id"]
            )

            results.append(
                {
                    "customer_id": customer_id,
                    "article_id": article_id,
                    "score": round(
                        float(score),
                        6
                    )
                }
            )

        return results


# =============================================================
# Singleton Recommendation Engine
# =============================================================

_engine = None


def get_engine():

    global _engine

    if _engine is None:

        _engine = RecommendationEngine()

    return _engine


# =============================================================
# Public function
# =============================================================

def get_dynamic_recommendations(
    customer_id,
    limit=10
):

    engine = get_engine()

    return engine.recommend(
        customer_id,
        limit
    )