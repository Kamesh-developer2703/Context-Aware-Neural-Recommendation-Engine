import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("outputs/recommendations.csv")

plt.figure(figsize=(10,5))

plt.hist(df["score"], bins=20)

plt.title("Recommendation Score Distribution")
plt.xlabel("Score")
plt.ylabel("Frequency")

plt.savefig("outputs/score_distribution.png")

print("Graph Saved Successfully!")