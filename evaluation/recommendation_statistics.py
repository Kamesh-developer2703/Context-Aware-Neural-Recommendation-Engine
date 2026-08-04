import pandas as pd

df = pd.read_csv("outputs/recommendations.csv")

print("=" * 50)
print("Recommendation Statistics")
print("=" * 50)

print(df.describe())

print()

print("Top 10 Highest Scores")

print(
    df.sort_values(
        by="score",
        ascending=False
    ).head(10)
)