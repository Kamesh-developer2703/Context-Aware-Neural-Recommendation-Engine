# Customer Data Preprocessing

## Steps Performed

1. Loaded customers.csv.
2. Checked missing values.
3. Replaced missing values in:
   - FN → 0
   - Active → 0
   - club_member_status → UNKNOWN
   - fashion_news_frequency → NONE
   - age → Median Age
4. Checked duplicate records.
5. Saved cleaned dataset as customers_cleaned.csv.

## Observations

- No duplicate records found.
- Age missing values were replaced with the median.
- Missing categorical values were replaced with meaningful defaults.
- Dataset is now ready for feature engineering.