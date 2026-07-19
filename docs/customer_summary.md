# Customer Dataset Summary

## Dataset Information

- Dataset Name: customers.csv
- Number of Rows: 1,371,980
- Number of Columns: 7

## Column Summary

| Column Name | Data Type | Missing Values | Description |
|-------------|-----------|---------------:|-------------|
| customer_id | object | 0 | Unique customer identifier |
| FN | float64 | 895050 | Fashion News subscription indicator |
| Active | float64 | 907576 | Customer activity indicator |
| club_member_status | object | 6062 | Membership status of the customer |
| fashion_news_frequency | object | 16011 | Frequency of receiving fashion news |
| age | float64 | 15861 | Age of the customer |
| postal_code | object | 0 | Customer postal code |

## Duplicate Records

- Total duplicate records: **0**

## Observations

- The dataset contains **1,371,980 customer records**.
- There are **7 columns**.
- `customer_id` and `postal_code` have no missing values.
- `FN` and `Active` contain a large number of missing values.
- `club_member_status`, `fashion_news_frequency`, and `age` have relatively fewer missing values.
- No duplicate records were found.
- This dataset provides customer profile information that can be combined with transaction and article datasets to build a recommendation system.