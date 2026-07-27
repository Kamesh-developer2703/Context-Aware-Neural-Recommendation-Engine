import pandas as pd

# Load recommendations
recommendations = pd.read_csv("outputs/recommendations.csv")

# Load actual transactions
transactions = pd.read_csv("outputs/encoded/transaction_encoded.csv")

# Select the same customer used in inference
customer_id = transactions.iloc[0]["customer_id"]

# Actual purchased articles
actual_items = set(
    transactions[
        transactions["customer_id"] == customer_id
    ]["article_id"]
)

# Recommended articles
recommended_items = set(
    recommendations["article_id"]
)

# -------------------------
# Evaluation Metrics
# -------------------------

hits = len(
    actual_items.intersection(recommended_items)
)

precision = hits / len(recommended_items)

recall = hits / len(actual_items)

hit_rate = 1 if hits > 0 else 0

print("=" * 40)
print("Recommendation Evaluation")
print("=" * 40)

print(f"Customer ID : {customer_id}")
print(f"Actual Purchased : {len(actual_items)}")
print(f"Recommended : {len(recommended_items)}")
print(f"Common Items : {hits}")

print("\nMetrics")
print(f"Precision@10 : {precision:.4f}")
print(f"Recall       : {recall:.4f}")
print(f"Hit Rate     : {hit_rate}")

# Save report

report = pd.DataFrame({
    "customer_id":[customer_id],
    "actual_items":[len(actual_items)],
    "recommended_items":[len(recommended_items)],
    "hits":[hits],
    "precision":[precision],
    "recall":[recall],
    "hit_rate":[hit_rate]
})

report.to_csv(
    "outputs/evaluation_report.csv",
    index=False
)

print("\nEvaluation report saved.")