import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import os


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


def fit_scalers():

    print("Loading datasets...")

    customers = pd.read_csv(
        "data/processed/customer_features_encoded.csv"
    )

    articles = pd.read_csv(
        "outputs/encoded/article_encoded.csv"
    )

    customer_scaler = StandardScaler()

    article_scaler = StandardScaler()

    print("Fitting customer scaler...")

    customer_scaler.fit(
        customers[CUSTOMER_FEATURES]
        .fillna(0)
    )

    print("Fitting article scaler...")

    article_scaler.fit(
        articles[ARTICLE_FEATURES]
        .fillna(0)
    )

    os.makedirs(
        "models/scalers",
        exist_ok=True
    )

    joblib.dump(
        customer_scaler,
        "models/scalers/customer_scaler.pkl"
    )

    joblib.dump(
        article_scaler,
        "models/scalers/article_scaler.pkl"
    )

    print("\nScalers saved successfully.")

    print(
        "Customer scaler:",
        "models/scalers/customer_scaler.pkl"
    )

    print(
        "Article scaler:",
        "models/scalers/article_scaler.pkl"
    )


if __name__ == "__main__":
    fit_scalers()