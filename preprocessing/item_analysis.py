import os
import pandas as pd

# Define path relative to project root
DATA_PATH = os.path.join("data", "raw", "articles.csv")

def main():
    if not os.path.exists(DATA_PATH):
        print(f"❌ Error: Please place articles.csv inside 'data/raw/'. Current path looking for: {DATA_PATH}")
        return

    # Load dataset
    print("⏳ Loading articles metadata...")
    df = pd.read_csv(DATA_PATH)
    
    # 1. Structural Check
    print("\n=== 📊 Dataset Dimensions ===")
    print(f"Total Rows (Articles): {df.shape[0]}")
    print(f"Total Features (Columns): {df.shape[1]}")
    
    # 2. Key Target Features Analysis
    target_features = ['product_group_name', 'graphical_appearance_name', 'colour_group_name', 'department_name', 'index_name']
    
    print("\n=== 🔍 Item Feature Breakdown ===")
    for col in target_features:
        if col in df.columns:
            unique_count = df[col].nunique()
            missing_count = df[col].isnull().sum()
            print(f"🔹 {col:<30} | Unique Values: {unique_count:<5} | Missing: {missing_count}")
            
    # 3. Top Categories Preview
    print("\n=== 👗 Sample Product Group Distribution ===")
    print(df['product_group_name'].value_counts().head(5))

if __name__ == "__main__":
    main()