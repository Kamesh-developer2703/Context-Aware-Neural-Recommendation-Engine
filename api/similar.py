import os
import pandas as pd
import torch
import torch.nn.functional as F
import joblib

from ann.model import TwoTowerModel


# ============================================================
# Paths
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

ARTICLE_FILE = os.path.join(
    BASE_DIR,
    "outputs",
    "encoded",
    "article_encoded.csv"
)

MODEL_FILE = os.path.join(
    BASE_DIR,
    "models",
    "two_tower_model_v2.pth"
)

ARTICLE_SCALER_FILE = os.path.join(
    BASE_DIR,
    "models",
    "scalers",
    "article_scaler.pkl"
)


# ============================================================
# Device
# ============================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(
    f"Similar Articles Device: {DEVICE}"
)

if torch.cuda.is_available():

    print(
        f"GPU: {torch.cuda.get_device_name(0)}"
    )


# ============================================================
# Global cache
# ============================================================

_article_ids = None
_article_embeddings = None


# ============================================================
# Article feature columns
# ============================================================

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


# ============================================================
# Load article embeddings
# ============================================================

def load_article_embeddings():

    global _article_ids
    global _article_embeddings

    # --------------------------------------------------------
    # Already loaded
    # --------------------------------------------------------

    if _article_embeddings is not None:
        return

    print(
        "Loading article data..."
    )

    # --------------------------------------------------------
    # Check article file
    # --------------------------------------------------------

    if not os.path.exists(ARTICLE_FILE):

        raise FileNotFoundError(
            f"Article file not found: {ARTICLE_FILE}"
        )

    articles = pd.read_csv(
        ARTICLE_FILE
    )

    print(
        f"Loaded articles: {len(articles)}"
    )

    # --------------------------------------------------------
    # Validate columns
    # --------------------------------------------------------

    required_columns = [
        "article_id"
    ] + ARTICLE_FEATURES

    missing_columns = [
        column
        for column in required_columns
        if column not in articles.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing article columns: "
            + str(missing_columns)
        )

    # --------------------------------------------------------
    # Article IDs
    # --------------------------------------------------------

    _article_ids = (
        articles["article_id"]
        .astype(int)
        .values
    )

    # ========================================================
    # Load article scaler
    # ========================================================

    print(
        "Loading article scaler..."
    )

    if not os.path.exists(ARTICLE_SCALER_FILE):

        raise FileNotFoundError(
            f"Article scaler not found: "
            f"{ARTICLE_SCALER_FILE}"
        )

    article_scaler = joblib.load(
        ARTICLE_SCALER_FILE
    )

    print(
        "Article scaler loaded."
    )

    # ========================================================
    # Prepare article features
    # ========================================================

    article_df = (
        articles[ARTICLE_FEATURES]
        .fillna(0)
        .astype("float32")
    )

    # --------------------------------------------------------
    # IMPORTANT:
    # Use the SAME scaler used during training
    # --------------------------------------------------------

    article_features = article_scaler.transform(
        article_df
    )

    article_features = article_features.astype(
        "float32"
    )

    article_tensor = torch.tensor(
        article_features,
        dtype=torch.float32,
        device=DEVICE
    )

    print(
        "Scaled article feature tensor:",
        article_tensor.shape
    )

    # ========================================================
    # Load Two-Tower model
    # ========================================================

    print(
        "Loading current Two-Tower model..."
    )

    if not os.path.exists(MODEL_FILE):

        raise FileNotFoundError(
            f"Model file not found: {MODEL_FILE}"
        )

    model = TwoTowerModel().to(
        DEVICE
    )

    state_dict = torch.load(
        MODEL_FILE,
        map_location=DEVICE
    )

    model.load_state_dict(
        state_dict
    )

    model.eval()

    print(
        "Current Two-Tower model loaded."
    )

    # ========================================================
    # Generate article embeddings
    # ========================================================

    print(
        "Generating article embeddings..."
    )

    with torch.no_grad():

        embeddings = model.article_tower(
            article_tensor
        )

        embeddings = F.normalize(
            embeddings,
            p=2,
            dim=1
        )

    _article_embeddings = embeddings

    print(
        "Article embeddings ready:",
        _article_embeddings.shape
    )


# ============================================================
# Similar Articles
# ============================================================

def get_similar_articles(
    article_id,
    limit=10
):

    load_article_embeddings()

    article_id = int(
        article_id
    )

    # --------------------------------------------------------
    # Find target article
    # --------------------------------------------------------

    matches = (
        _article_ids == article_id
    )

    if not matches.any():

        return None

    target_index = int(
        matches.argmax()
    )

    # --------------------------------------------------------
    # Target embedding
    # --------------------------------------------------------

    target_embedding = (
        _article_embeddings[
            target_index
        ]
    )

    # --------------------------------------------------------
    # Cosine similarity
    # --------------------------------------------------------

    similarity_scores = torch.matmul(
        _article_embeddings,
        target_embedding
    )

    # --------------------------------------------------------
    # Don't recommend itself
    # --------------------------------------------------------

    similarity_scores[
        target_index
    ] = -1

    # --------------------------------------------------------
    # Top-K
    # --------------------------------------------------------

    top_k = min(
        int(limit),
        len(_article_ids) - 1
    )

    if top_k <= 0:

        return []

    scores, indices = torch.topk(
        similarity_scores,
        k=top_k
    )

    # --------------------------------------------------------
    # Build response
    # --------------------------------------------------------

    results = []

    for score, index in zip(
        scores.cpu().tolist(),
        indices.cpu().tolist()
    ):

        results.append({

            "article_id": int(
                _article_ids[index]
            ),

            "score": round(
                float(score),
                6
            )
        })

    return results