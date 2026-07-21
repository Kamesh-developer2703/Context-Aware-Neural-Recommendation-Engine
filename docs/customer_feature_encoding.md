# Customer Feature Encoding

## Objective
Convert categorical customer features into numerical values for model training.

## Encoded Features

### 1. Club Member Status
- Encoded using LabelEncoder.
- New column: `club_member_status_encoded`

### 2. Fashion News Frequency
- Encoded using LabelEncoder.
- New column: `fashion_news_frequency_encoded`

### 3. Age Group
- Encoded using LabelEncoder.
- New column: `age_group_encoded`

## Output
Generated file:
- customer_features_encoded.csv

## Summary
The categorical customer features were successfully encoded into numerical values, making them suitable for use in the neural recommendation model.