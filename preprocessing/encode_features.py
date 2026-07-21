import os
import pandas as pd
import json
from sklearn.preprocessing import LabelEncoder

# Define paths relative to project root
INPUT_PATH = os.path.join("data", "preprocessing", "cleaned_articles.csv")
OUTPUT_CSV_PATH = os.path.join("data", "preprocessing", "encoded_articles.csv")
ENCODER_MAPPING_PATH = os.path.join("data", "preprocessing", "feature_encoders.json")

def encode_article_features():
    if not os.path.exists(INPUT_PATH):
        print(f"❌ Error: Cleaned dataset not found at {INPUT_PATH}. Run clean_data.py first!")
        return

    print("⏳ Loading cleaned articles metadata for encoding...")
    df = pd.read_csv(INPUT_PATH)
    
    # 1. Target categorical features requested for encoding
    target_features = [
        'product_type_name', 
        'product_group_name', 
        'colour_group_name', 
        'graphical_appearance_name'
    ]
    
    label_mappings = {}
    encoded_df = df.copy()

    print("\n=== ⚙️ Encoding Categorical Features ===")
    for col in target_features:
        if col in encoded_df.columns:
            le = LabelEncoder()
            # Fit and transform feature string values to numerical integer IDs
            encoded_col_name = f"{col}_encoded"
            encoded_df[encoded_col_name] = le.fit_transform(encoded_df[col].astype(str))
            
            # Store key mapping for model inference & lookup
            label_mappings[col] = {str(label): int(idx) for idx, label in enumerate(le.classes_)}
            
            print(f"✅ Encoded '{col}' -> '{encoded_col_name}' ({len(le.classes_)} classes mapped)")
        else:
            print(f"⚠️ Warning: Feature '{col}' missing from input data!")

    # 2. Save Encoded Dataset and Mappings
    os.makedirs(os.path.dirname(OUTPUT_CSV_PATH), exist_ok=True)
    encoded_df.to_csv(OUTPUT_CSV_PATH, index=False)
    
    with open(ENCODER_MAPPING_PATH, 'w') as f:
        json.dump(label_mappings, f, indent=4)
        
    print(f"\n💾 Encoded dataset saved to: {OUTPUT_CSV_PATH}")
    print(f"💾 Encoder mappings saved to: {ENCODER_MAPPING_PATH}")

    # 3. Output Validation
    validate_encoding(encoded_df, target_features)

def validate_encoding(df, features):
    print("\n=== 🧪 Validating Encoded Outputs ===")
    all_valid = True
    
    for col in features:
        encoded_col = f"{col}_encoded"
        if encoded_col in df.columns:
            null_count = df[encoded_col].isnull().sum()
            min_val = df[encoded_col].min()
            max_val = df[encoded_col].max()
            unique_encoded = df[encoded_col].nunique()
            unique_original = df[col].nunique()
            
            print(f"\n📦 Check: {encoded_col}")
            print(f"  ▪️ Null Values: {null_count}")
            print(f"  ▪️ Index Range: [{min_val} to {max_val}]")
            print(f"  ▪️ Unique Code Count: {unique_encoded} (Original Raw Strings: {unique_original})")
            
            # Validation rule check
            if null_count == 0 and unique_encoded == unique_original:
                print(f"  ✅ Validation Passed: 1-to-1 encoding mapping preserved cleanly.")
            else:
                print(f"  ❌ Validation Failed: Discrepancy detected in category count or null values!")
                all_valid = False
                
    if all_valid:
        print("\n🎉 All target features successfully encoded and verified for candidate tower inputs!")

if __name__ == "__main__":
    encode_article_features()