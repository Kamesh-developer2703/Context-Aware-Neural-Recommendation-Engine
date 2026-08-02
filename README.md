# Context-Aware-Neural-Recommendation-Engine
Team Members : Kameshwaran K , Mokshita Tailuru , Manav Kansal , Gopidinni Mounica
# Context-Aware Neural Recommendation Engine

## Project Overview

This project is a Deep Learning-based Recommendation System developed as part of the Zaalima Development Pvt. Ltd. Internship Program.

The system generates personalized product recommendations for an e-commerce platform by learning from user behavior, product metadata, and contextual information using a Two-Tower Neural Network architecture.

---

## Objective

Build a scalable recommendation engine capable of providing real-time, personalized product suggestions based on:

- User demographics
- Purchase history
- Product metadata
- Contextual features
- Long-term and short-term user preferences

---

## Dataset

**H&M Personalized Fashion Recommendations**

Dataset Source:
https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations

Main Files

- customers.csv
- articles.csv
- transactions_train.csv

---

## Technology Stack

- Python
- TensorFlow
- TensorFlow Recommenders (TFRS)
- Keras
- PySpark
- FastAPI
- Redis
- Apache Airflow
- Git & GitHub

---

## Project Architecture

Dataset
        │
        ▼
Data Cleaning
        │
        ▼
Feature Engineering
        │
        ▼
Two-Tower Neural Network
        │
        ▼
Model Training
        │
        ▼
Item Embeddings
        │
        ▼
Redis Feature Store
        │
        ▼
FastAPI
        │
        ▼
Top-K Recommendations

---

## Team Members

| Name | Role |
|------|------|
| Kameshwaran K | Team Leader |
| Mounika | Team Member |
| Mokshita | Team Member |
| Manav Kansal | Team Member |

---

## Project Timeline

### Week 1
- Data preprocessing
- Feature engineering
- Vocabulary creation

### Week 2
- Two-Tower model development
- Model training
- Model evaluation

### Week 3
- Model serving
- Redis integration
- ANN search

### Week 4
- FastAPI
- Airflow automation
- API testing
- Documentation

---

## Repository Structure

```
context-aware-neural-recommendation-engine/

│── data/
│   ├── raw/
│   ├── processed/
│
│── notebooks/
│
│── preprocessing/
│
│── feature_engineering/
│
│── models/
│
│── api/
│
│── airflow/
│
│── redis/
│
│── embeddings/
│
│── evaluation/ 
│
│── docs/
│
│── diagrams/
│
│── tests/
│
│── utils/
│
│── requirements.txt
│── README.md
│── .gitignore
```

---

## Expected Outcome

A scalable recommendation engine capable of generating personalized product recommendations using Deep Learning and contextual user information.

---

## License

This project is developed for educational and internship purposes under Zaalima Development Pvt. Ltd.
## Inference

Run the trained recommendation model:

python -m models.inference

Outputs are saved to:

outputs/recommendations.csv

Model checkpoints are stored in:

saved_models/
## Day 9 Progress

### End-to-End Testing
- Successfully tested the complete recommendation pipeline.
- Verified dataset loading, model loading, inference execution, and recommendation generation.

### Recommendation Output
- Recommendations are automatically saved to:
  outputs/recommendations.csv

### Bug Fixes
- Added model checkpoint validation before loading.
- Verified recommendation output generation across multiple customer samples.

### Status
- End-to-end testing completed successfully.
- Recommendation pipeline is stable and working as expected.
# Recommendation Testing Report

## Objective
Validate recommendation generation and Top-K recommendation outputs.

## Test Environment

- Framework: PyTorch
- Dataset: RecommendationDataset
- Model: Two-Tower Recommendation Model

## Tests Performed

### 1. Recommendation Generation

- Successfully generated recommendation scores.
- Tested inference on 1000 samples.

Status: PASS

---

### 2. Top-K Recommendation Validation

Top-K = 10

Observed Output:

| Sample ID | Actual Label | Score |
|-----------|-------------|-------|
| 0 | 1 | 1.0000 |
| 1 | 1 | 1.0000 |
| 2 | 1 | 1.0000 |
| 3 | 1 | 1.0000 |
| 4 | 1 | 1.0000 |
| 5 | 1 | 1.0000 |
| 6 | 1 | 1.0000 |
| 7 | 1 | 1.0000 |
| 8 | 1 | 1.0000 |
| 9 | 1 | 1.0000 |

Observation:

- Top-10 recommendations were generated successfully.
- Recommendations are sorted by prediction score.
- All Top-K samples belong to positive interactions (label = 1).

Status: PASS

---

### 3. Bug Fixes

- Added model path validation.
- Added Top-K recommendation export.
- Added actual labels for evaluation.
- Improved inference code readability.
- Added inference optimization using `torch.no_grad()`.

Status: PASS

---

## Conclusion

The recommendation inference pipeline executed successfully.

Recommendation outputs were generated correctly and exported to:

- outputs/recommendations.csv
- outputs/top_k_recommendations.csv
Bug Report

1. Removed duplicate dataset access in inference loop.
2. Added Top-K recommendation output generation.
3. Improved inference readability with comments.
4. Sorted recommendation scores before saving output.
5. Verified API responses for sample requests.