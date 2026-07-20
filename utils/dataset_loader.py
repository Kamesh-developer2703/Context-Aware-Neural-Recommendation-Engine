import os
import kagglehub
import pandas as pd

def load_dataset():
    path = kagglehub.competition_download(
        "h-and-m-personalized-fashion-recommendations"
    )

    customers = pd.read_csv(os.path.join(path, "customers.csv"))
    articles = pd.read_csv(os.path.join(path, "articles.csv"))
    transactions = pd.read_csv(os.path.join(path, "transactions_train.csv"))

    return customers, articles, transactions