import pandas as pd

print("=" * 50)
print("Recommendation Evaluation")
print("=" * 50)

recommendations = pd.read_csv("outputs/recommendations.csv")

print(f"Total Recommendations : {len(recommendations)}")
print(f"Unique Customers       : {recommendations['customer_id'].nunique()}")
print(f"Unique Articles        : {recommendations['article_id'].nunique()}")

print()

avg_score = recommendations["score"].mean()
max_score = recommendations["score"].max()
min_score = recommendations["score"].min()

print(f"Average Score : {avg_score:.4f}")
print(f"Highest Score : {max_score:.4f}")
print(f"Lowest Score  : {min_score:.4f}")

top_customer = (
    recommendations.groupby("customer_id")
    .size()
    .sort_values(ascending=False)
)

print()
print("Top Customers by Recommendation Count")
print(top_customer.head())

report = pd.DataFrame({
    "Metric": [
        "Total Recommendations",
        "Unique Customers",
        "Unique Articles",
        "Average Score",
        "Highest Score",
        "Lowest Score"
    ],
    "Value": [
        len(recommendations),
        recommendations["customer_id"].nunique(),
        recommendations["article_id"].nunique(),
        avg_score,
        max_score,
        min_score
    ]
})

report.to_csv(
    "outputs/performance_report.csv",
    index=False
)

print("\nPerformance report saved.")