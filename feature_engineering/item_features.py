import os
import pandas as pd
import json

# Paths relative to project root
ENCODED_DATA_PATH = os.path.join("data", "preprocessing", "encoded_articles.csv")
OUTPUT_SUMMARY_PATH = os.path.join("data", "preprocessing", "item_tower_schema.json")

def prepare_item_tower_features():
    if not os.path.exists(ENCODED_DATA_PATH):
        print(f"❌ Error: Encoded dataset not found at {ENCODED_DATA_PATH}. Run preprocessing/encode_features.py first!")
        return

    print("⏳ Loading encoded articles dataset for Item Tower feature preparation...")
    df = pd.read_csv(ENCODED_DATA_PATH)

    # 1. Define required field schema for Candidate/Item Tower inputs
    required_id_fields = ['article_id']
    required_text_fields = ['detail_desc']
    required_encoded_fields = [
        'product_type_name_encoded',
        'product_group_name_encoded',
        'colour_group_name_encoded',
        'graphical_appearance_name_encoded'
    ]

    all_required_fields = required_id_fields + required_text_fields + required_encoded_fields

    print("\n=== 🔍 Auditing Required Fields for Candidate Tower ===")
    missing_fields = [field for field in all_required_fields if field not in df.columns]

    if missing_fields:
        print(f"❌ Verification Failed! Missing fields in dataset: {missing_fields}")
        return
    else:
        print("✅ Field Presence Audit: All required candidate feature fields are present in dataset.")

    # 2. Quality Check: Null Values & Data Types
    print("\n=== 🧪 Quality & Integrity Checks ===")
    quality_pass = True

    for field in all_required_fields:
        nulls = df[field].isnull().sum()
        dtype = str(df[field].dtype)
        print(f"🔹 Field: {field:<35} | Dtype: {dtype:<8} | Nulls: {nulls}")
        
        if nulls > 0:
            quality_pass = False

    # Check unique article count matching row count (article_id must be unique primary key)
    unique_articles = df['article_id'].nunique()
    total_rows = len(df)
    print(f"\n🔑 Primary Key Check: {unique_articles} unique article_ids out of {total_rows} total rows.")

    if unique_articles != total_rows:
        print("⚠️ Warning: Duplicate article IDs detected!")
        quality_pass = False

    # 3. Export Candidate Tower Feature Schema Metadata
    if quality_pass:
        schema_metadata = {
            "total_candidate_items": total_rows,
            "item_id_field": "article_id",
            "text_features": required_text_fields,
            "categorical_encoded_features": {
                "product_type_name_encoded": {"cardinality": int(df['product_type_name_encoded'].nunique())},
                "product_group_name_encoded": {"cardinality": int(df['product_group_name_encoded'].nunique())},
                "colour_group_name_encoded": {"cardinality": int(df['colour_group_name_encoded'].nunique())},
                "graphical_appearance_name_encoded": {"cardinality": int(df['graphical_appearance_name_encoded'].nunique())}
            },
            "status": "Ready for Item Tower Embedding Ingestion"
        }

        os.makedirs(os.path.dirname(OUTPUT_SUMMARY_PATH), exist_ok=True)
        with open(OUTPUT_SUMMARY_PATH, 'w') as f:
            json.dump(schema_metadata, f, indent=4)

        print(f"\n💾 Item Tower feature schema saved to: {OUTPUT_SUMMARY_PATH}")
        print("\n🎉 Item Tower Feature Preparation Passed! All fields ready for model training.")

if __name__ == "__main__":
    prepare_item_tower_features()
    