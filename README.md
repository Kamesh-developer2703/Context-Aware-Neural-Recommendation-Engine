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
