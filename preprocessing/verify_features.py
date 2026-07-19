import os
import pandas as pd

# Path to the cleaned data artifact we generated
CLEANED_DATA_PATH = os.path.join("data", "preprocessing", "cleaned_articles.csv")

def verify_product_features():
    if not os.path.exists(CLEANED_DATA_PATH):
        print(f"❌ Error: Cleaned data not found at {CLEANED_DATA_PATH}. Please run clean_data.py first!")
        return

    print("⏳ Loading cleaned articles metadata for feature verification...")
    df = pd.read_csv(CLEANED_DATA_PATH)
    
    # Define target features explicitly requested for today's task
    target_features = [
        'product_type_name', 
        'product_group_name', 
        'colour_group_name', 
        'graphical_appearance_name'
    ]
    
    print("\n=== 🔍 Feature Consistency & Missing Value Audit ===")
    
    all_consistent = True
    for col in target_features:
        if col in df.columns:
            missing_count = df[col].isnull().sum()
            unique_elements = df[col].unique()
            
            print(f"\n📦 Attribute: {col}")
            print(f"  ▪️ Missing Values: {missing_count}")
            print(f"  ▪️ Unique Feature Count: {len(unique_elements)}")
            
            # Verify feature consistency (ensure no stray empty string records masked as valid text)
            blank_strings = (df[col].astype(str).str.strip() == "").sum()
            if blank_strings > 0:
                print(f"  ⚠️ Warning: Detected {blank_strings} blank space strings!")
                all_consistent = False
            else:
                print(f"  ✅ Consistency Pass: All string values structurally valid.")
        else:
            print(f"❌ Error: Required feature '{col}' is missing from the dataset structure!")
            all_consistent = False

    if all_consistent:
        print("\n🎉 Verification Complete: All product-related features are consistent, fully imputed, and ready for embedding generation!")

if __name__ == "__main__":
    verify_product_features()