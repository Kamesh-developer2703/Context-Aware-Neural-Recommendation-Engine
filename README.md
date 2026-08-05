# 🧠 Context-Aware Neural Recommendation Engine

An end-to-end Candidate Retrieval System designed using a **Two-Tower Neural Architecture** (User Tower & Candidate/Item Tower) to retrieve personalized item recommendations based on categorical article metadata and customer interaction contexts.

---

## 📌 Executive Summary
* **Architecture:** Two-Tower Deep Learning Retrieval Network (Categorical Embedding Layers + Dense Feature Projection Layers).
* **Target Features Encoded:** `product_type_name`, `product_group_name`, `colour_group_name`, `graphical_appearance_name`.
* **Primary Metric Performance (@ K=10):**
  * **Precision@10:** `0.0978` (+1530.0% relative uplift over baseline)
  * **Recall@10:** `0.1956` (+1530.0% relative uplift over baseline)
  * **Hit Rate@10:** `0.7400` / **74.0%** (+1175.9% relative uplift over baseline)
  * **F1-Score@10:** `0.1305` (+1531.2% relative uplift over baseline)

---

## 🏗️ System Architecture & Workflow

1. **Preprocessing & Label Encoding:**
   * Handled missing value imputation and built continuous zero-indexed label encodings for all target attributes.
   * Saved mapping dictionaries to `data/preprocessing/feature_encoders.json` for bidirectional decoding during inference.
2. **Feature Engineering (`feature_engineering/item_features.py`):**
   * Assembled item entity features, ensured 0 duplicate article ID keys, and exported input cardinalities in `data/preprocessing/item_tower_schema.json`.
3. **Neural Model Architecture (`models/two_tower_model.py`):**
   * **Item Tower:** Concatenates categorical entity embeddings into dense feed-forward projection layers (`Dense(128) -> BatchNorm -> Dropout(0.2) -> Dense(64)`).
   * **User Tower:** Maps user context vectors into a matching 64-dimensional latent embedding space.
   * **Loss Function:** In-Batch Softmax Cross-Entropy Loss (`tfrs.tasks.Retrieval`).
4. **Post-Processing & Quality Verification (`evaluation/post_process_recommendations.py`):**
   * Applied candidate deduplication, removed previously purchased items, and verified strict descending score ranking logic across multi-customer testing profiles.

---

## 📊 Performance Benchmarks & Summary Results

### 📈 Metric Evaluation Table (@ K = 10)
| Metric | Baseline Model | Two-Tower Neural Model | Relative Improvement (Uplift) |
| :--- | :--- | :--- | :--- |
| **Precision@10** | 0.0060 | **0.0978** | **+1530.0%** |
| **Recall@10** | 0.0120 | **0.1956** | **+1530.0%** |
| **Hit Rate@10** | 0.0580 (5.8%) | **0.7400 (74.0%)** | **+1175.9%** |
| **F1-Score@10** | 0.0080 | **0.1305** | **+1531.2%** |

---

## 🖼️ Evaluation Visualizations & Generated Artifacts

All evaluation plot artifacts are exported in `evaluation/plots/`:
* `loss_vs_epochs.png` — Training & Validation Softmax Loss convergence trajectory across epochs.
* `recommendation_count_distribution.png` — Candidate coverage and long-tail distribution analysis.
* `evaluation_metrics_k10.png` — Quantitative benchmark bar charts (@ K=10).
* `performance_comparison_chart.png` — Iterative comparative analysis between previous results and current model outputs.

---

## 🚀 Future Scope & Enhancements
1. **Real-Time Vector Indexing:** Integrate **FAISS** or **ScaNN** for approximate nearest neighbor (ANN) retrieval at sub-millisecond latencies.
2. **Multimodal Feature Fusion:** Ingest visual image features via ResNet/CLIP alongside textual descriptions (`detail_desc`).
3. **Two-Stage Ranking Architecture:** Pair the retrieval candidate tower with a downstream Deep & Cross Network (DCNv2) for fine-grained personalized scoring.

### 🚀 Key Improvements & Final Deliverables
* **FastAPI Service Verification:** Fully operational REST API (`api/main.py`) serving real-time candidate retrieval with customer-specific context.
* **Interactive OpenAPI/Swagger Docs:** Integrated interactive documentation accessible at `/docs`.
* **Complete Evaluation Suite:** Quantitative benchmarks ($K=10$), loss convergence plots, and qualitative expected vs. actual recommendation comparisons.
* **Asset Organization:** Structured all evaluation graphs, report JSONs, feature encoders, and schema dictionaries into clean module directories.

### 🖼️ Documentation Visual Assets
* **Swagger UI Overview:** `evaluation/plots/swagger_ui_overview.png`
* **API Customer Input:** `evaluation/plots/customer_endpoint_input.png`
* **Recommendation Response:** `evaluation/plots/recommendation_response_output.png`
* **Loss vs. Epochs:** `evaluation/plots/loss_vs_epochs.png`
* **Performance Comparison:** `evaluation/plots/performance_comparison_chart.png`