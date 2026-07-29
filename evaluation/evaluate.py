import pandas as pd
import os

# Load recommendations
recommendations = pd.read_csv("outputs/recommendations.csv")

print("========== Recommendation Evaluation ==========")

print(f"Total Recommendations : {len(recommendations)}")
print(f"Unique Articles       : {recommendations['article_id'].nunique()}")

if "score" in recommendations.columns:
    print(f"Average Score         : {recommendations['score'].mean():.4f}")
    print(f"Highest Score         : {recommendations['score'].max():.4f}")
    print(f"Lowest Score          : {recommendations['score'].min():.4f}")

# Save evaluation report
report = pd.DataFrame({
    "Metric": [
        "Total Recommendations",
        "Unique Articles",
        "Average Score",
        "Highest Score",
        "Lowest Score"
    ],
    "Value": [
        len(recommendations),
        recommendations["article_id"].nunique(),
        recommendations["score"].mean(),
        recommendations["score"].max(),
        recommendations["score"].min()
    ]
})

os.makedirs("outputs", exist_ok=True)
report.to_csv("outputs/evaluation_report.csv", index=False)

print("\nEvaluation report saved successfully!")