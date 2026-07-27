import pandas as pd


def check_missing(df):
    return df.isnull().sum()


def check_duplicates(df):
    return df.duplicated().sum()


def save_dataframe(df, path):
    df.to_csv(path, index=False)