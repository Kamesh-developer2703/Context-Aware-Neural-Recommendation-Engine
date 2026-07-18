import os
import pandas as pd

# Define paths relative to project root
INPUT_PATH = os.path.join("data", "raw", "articles.csv")
OUTPUT_PATH = os.path.join("data", "preprocessing", "cleaned_articles.csv")

def clean_articles():
    if not os.path.exists(INPUT_PATH):
        print(f"❌ Error: Please place articles.csv inside 'data/raw/'. Path: {INPUT_PATH}")
        return

    print("⏳ Loading articles metadata for cleaning...")
    df = pd.read_csv(INPUT_PATH)
    
    print(f"📊 Original Shape: {df.shape}")

    # 1. Drop redundant ID/Code columns where a descriptive text name exists
    redundant_cols = [
        'product_type_no', 
        'graphical_appearance_no', 
        'colour_group_code', 
        'perceived_colour_value_id', 
        'perceived_colour_master_id',
        'department_no', 
        'index_code', 
        'index_group_no', 
        'section_no', 
        'garment_group_no'
    ]
    
    # Drop columns only if they exist in the dataframe
    cols_to_drop = [col for col in redundant_cols if col in df.columns]
    df_cleaned = df.drop(columns=cols_to_drop)
    print(f"✂️ Dropped {len(cols_to_drop)} redundant code columns.")

    # 2. Handle missing text values safely for neural embeddings
    if 'detail_desc' in df_cleaned.columns:
        missing_desc = df_cleaned['detail_desc'].isnull().sum()
        df_cleaned['detail_desc'] = df_cleaned['detail_desc'].fillna("Unknown")
        print(f"📝 Filled {missing_desc} missing product descriptions with 'Unknown'.")

    # 3. Final Verification
    print("\n=== ✅ Cleaned Data Summary ===")
    print(f"Total Rows Retained: {df_cleaned.shape[0]}")
    print(f"Total Features Retained: {df_cleaned.shape[1]}")
    print(f"Remaining Columns: {list(df_cleaned.columns)}")

    # 4. Save the processed artifact
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df_cleaned.to_csv(OUTPUT_PATH, index=False)
    print(f"💾 Cleaned dataset successfully saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    clean_articles()
    
