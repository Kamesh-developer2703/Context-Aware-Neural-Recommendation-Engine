import os

import pandas as pd
import torch
import torch.nn.functional as F

from models.two_tower_model import TwoTowerModel


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ITEM_FILE = os.path.join(
    BASE_DIR,
    "data",
    "features",
    "item_features.csv"
)

MODEL_FILE = os.path.join(
    BASE_DIR,
    "saved_models",
    "two_tower_model_day11.pth"
)


# --------------------------------------------------
# Global cache
# --------------------------------------------------

_article_ids = None
_article_embeddings = None


# --------------------------------------------------
# Load article embeddings
# --------------------------------------------------

def load_article_embeddings():

    global _article_ids
    global _article_embeddings

    if _article_embeddings is not None:
        return

    print("Loading article features...")

    articles = pd.read_csv(ITEM_FILE)

    # Keep only numeric features
    numeric_articles = articles.select_dtypes(
        include=["number"]
    )

    _article_ids = numeric_articles[
        "article_id"
    ].astype(int).values

    # Same feature structure used by the model
    article_features = numeric_articles.values

    article_tensor = torch.tensor(
        article_features,
        dtype=torch.float32
    )

    print("Loading trained model...")

    model = TwoTowerModel(
        user_dim=5,
        item_dim=13,
        embedding_dim=64
    )

    state_dict = torch.load(
        MODEL_FILE,
        map_location="cpu"
    )

    model.load_state_dict(state_dict)

    model.eval()

    print("Generating article embeddings...")

    with torch.no_grad():

        embeddings = model.candidate_tower(
            article_tensor
        )

        # Normalize for cosine similarity
        embeddings = F.normalize(
            embeddings,
            p=2,
            dim=1
        )

    _article_embeddings = embeddings

    print(
        f"Loaded {_article_embeddings.shape[0]} "
        "article embeddings."
    )


# --------------------------------------------------
# Find similar articles
# --------------------------------------------------

def get_similar_articles(article_id, limit=10):

    load_article_embeddings()

    article_id = int(article_id)

    matches = (
        _article_ids == article_id
    )

    if not matches.any():

        return None

    target_index = matches.argmax()

    target_embedding = (
        _article_embeddings[target_index]
    )

    # Cosine similarity because embeddings are normalized
    similarity_scores = torch.matmul(
        _article_embeddings,
        target_embedding
    )

    # Don't recommend the same article
    similarity_scores[target_index] = -1

    # We need extra results because the target
    # article has been removed.
    top_k = min(
        limit,
        len(_article_ids) - 1
    )

    scores, indices = torch.topk(
        similarity_scores,
        k=top_k
    )

    results = []

    for score, index in zip(
        scores.tolist(),
        indices.tolist()
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