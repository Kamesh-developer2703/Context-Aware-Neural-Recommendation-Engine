import pandas as pd

df = pd.read_csv("outputs/recommendations.csv")

print("Total Recommendations :", len(df))
print("Unique Customers :", df.customer_id.nunique())
print("Unique Articles :", df.article_id.nunique())
print("Average Score :", df.score.mean())
print("Maximum Score :", df.score.max())
print("Minimum Score :", df.score.min())