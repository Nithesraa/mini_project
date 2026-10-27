# Project Overview

## 1. Project Title (Verified)

**"Enhancing Security in Industrial IoT Networks: Machine Learning Solutions for Feature Selection and Reduction"**

This is also the exact title of the base reference paper (Houkan et al., IEEE Access, 2024) that this project reproduces. The web app title used is: **"Industrial IoT Network Intrusion Detection — Experimental Reproduction and Benchmarking Suite"**

---

## 2. Project Domain and Application Type

- **Domain:** Cybersecurity / Network Intrusion Detection / Industrial Internet of Things (IIoT)
- **Application Type:** Experimental reproduction study + interactive web-based benchmarking and live-inference dashboard
- **Sub-domain:** Dimensionality reduction for resource-constrained IIoT edge ML inference

---

## 3. Problem Statement (Verified from index.html and methodology.html)

Industrial Internet of Things (IIoT) deployments rely on resource-constrained edge gateways (embedded processors with limited CPU, RAM, and battery) to monitor network traffic in real time. Traditional network intrusion detection systems (NIDS) operate on large, high-dimensional network flow feature vectors (79+ features in this dataset). Processing 80+ features simultaneously at edge gateways causes:

1. Packet drops due to insufficient real-time processing capacity
2. Excessive power consumption leading to battery exhaustion in field-deployed sensors
3. Increased training time and memory footprint for ML models

**Specific Gap:** The 2024 IEEE Access paper by Houkan et al. proposed using PCA and MRMR to reduce the feature space, but did not provide an open, reproducible Python implementation. The original experiments were conducted in MATLAB Classification Learner, creating a reproducibility gap.

---

## 4. Existing System and Its Limitations

| Limitation | Evidence Source |
|---|---|
| High-dimensional input (79 features) | dataset_info.txt, index.html |
| MATLAB-only implementation (original study) | methodology.html |
| No reproducible Python codebase | methodology.html — MATLAB-to-sklearn mapping table |
| No interactive evaluation dashboard | (implicit — project contribution) |
| KNN on full 79 features: 273 MB model file | output/models/ — model_binary_baseline_79_KNN.joblib |

---

## 5. Proposed System and Contributions (Verified)

The project implements a complete Python reproduction of the Houkan et al. study and extends it with a live web-based evaluation platform. **Verified contributions:**

1. **Full experimental reproduction:** 108 models trained across 2 tasks × 9 feature configurations × 6 ML algorithms — all 108 `.joblib` files confirmed present in `output/models/`
2. **PCA dimensionality reduction track:** Reduces 79 features to k ∈ {4, 12, 23, 50} principal components. PCA cumulative variance verified against paper targets (within 0.04% delta — confirmed in features.html)
3. **MRMR supervised feature selection:** Selects top-k features using Minimum Redundancy Maximum Relevance criterion for both binary and multiclass tasks. Rankings verified in `output/feature_engineering/mrmr_binary_rankings.csv` and `mrmr_multiclass_rankings.csv`
4. **MATLAB-to-scikit-learn mathematical translation:** 6 classifier families reproduced with exact hyperparameter mappings
5. **Interactive Flask web application:** Dashboard, live demo, benchmarks table (108 experiments), feature reduction analysis page, methodology page
6. **Live inference engine:** Serves real trained models for real-time prediction on authentic test-set network flows
7. **Decision tree explainability:** Dynamic path traversal extracted from `model.decision_path()` — not simulated

---

## 6. Main Aim

To reproduce, validate, and interactively demonstrate that supervised MRMR feature selection achieves near-identical intrusion detection accuracy (≤0.03% accuracy drop) versus full-feature baselines while reducing feature dimensionality by up to 84.8%, thereby enabling deployment on resource-constrained IIoT edge gateways.

---

## 7. Specific Objectives (Verified from implementation)

1. Ingest and preprocess the IoTID20 dataset (625,783 flows, 86 columns → 79 features after header removal)
2. Partition data with a reproducible 70/30 stratified split (random_state=42)
3. Apply PCA and compute k-component subspaces for k ∈ {4, 12, 23, 50}
4. Execute MRMR feature selection for binary and multiclass targets separately
5. Train 6 ML classifiers per feature configuration per task (108 total experiments)
6. Evaluate all models on 187,735 held-out test flows and record: accuracy, precision, recall, F1, FAR, AUC, throughput, training time, model file size
7. Verify PCA explained variance fractions against paper-reported values
8. Serve trained models via a Flask REST API for live interactive inference
9. Display 108 benchmark results in a filterable web table with confusion matrix viewer

---

## 8. Dataset

| Property | Value | Evidence Source |
|---|---|---|
| Name | IoTID20 | index.html, base reference paper |
| Authors | Ullah & Mahmoud | index.html |
| Total flow records | 625,783 | dataset_info.txt, index.html |
| Total columns (raw) | 86 | dataset_info.txt (shape: 625783 × 86) |
| Feature columns used | 79 | After removing 4 metadata headers + 2 label columns |
| Binary label: Anomaly | 585,710 (93.60%) | dataset_info.txt |
| Binary label: Normal | 40,073 (6.40%) | dataset_info.txt |
| Multiclass: Mirai | 415,677 (66.43%) | dataset_info.txt |
| Multiclass: Scan | 75,265 (12.03%) | dataset_info.txt |
| Multiclass: DoS | 59,391 (9.49%) | dataset_info.txt |
| Multiclass: Normal | 40,073 (6.40%) | dataset_info.txt |
| Multiclass: MITM ARP Spoofing | 35,377 (5.65%) | dataset_info.txt |
| Missing values | 0 | dataset_info.txt |
| Duplicate rows | 164,087 (26.22%) — kept intentionally | dataset_info.txt |
| Infinite values | 368 each in Flow_Byts/s and Flow_Pkts/s | dataset_info.txt |
| Data file size | ~295 MB (CSV) | Data/IoT Network Intrusion Dataset.csv |
| Training set | 438,048 samples (70%) | index.html |
| Test set | 187,735 samples (30%) | index.html |
| Class imbalance | Severe: 93.6% Anomaly vs. 6.4% Normal | dataset_info.txt |

---

## 9. Experimental Configuration (Verified)

| Parameter | Value | Evidence |
|---|---|---|
| Feature reduction methods | Baseline (79), PCA, MRMR | results_cache.json, config.py |
| Feature counts evaluated (k) | 4, 12, 23, 50 (+ 79 baseline) | results_cache.json |
| Classification tasks | Binary (Anomaly/Normal), Multiclass (5-class) | results_cache.json |
| ML algorithms | Decision Tree, KNN, Neural Network, Gaussian SVM, SVM Kernel, Logistic Regression Kernel | results_cache.json |
| Total trained models | 108 (2 × 9 × 6) | 108 .joblib files confirmed |
| Train/test split | 70% / 30%, stratified, seed=42 | index.html, methodology.html |
| Preprocessing | MinMax scaling [0,1], infinite value replacement | methodology.html |

---

## 10. Scope and Boundaries

**In scope (verified as implemented):**
- Reproduction of Houkan et al. 2024 experiments for binary and 5-class classification
- PCA and MRMR feature reduction at k ∈ {4, 12, 23, 50}
- 6 ML classifier families
- Interactive Flask web application for visualization and live inference
- Confusion matrix viewer for all 108 experiments

**Out of scope (not implemented):**
- Real-time packet capture or network stream ingestion
- Deployment on physical IoT hardware
- Custom/new ML architectures not mentioned in the base paper
- User authentication or database storage
- Cross-dataset validation
- Production deployment (WSGI/Nginx/Docker configuration)

---

## 11. Intended Users

- Academic reviewers / panel members evaluating the project
- Researchers seeking to reproduce Houkan et al. 2024
- Students and educators studying IIoT network security and ML dimensionality reduction

---

## 12. Functional Requirements (Verified from implementation)

| FR | Description | Implemented |
|---|---|---|
| FR-01 | Display dashboard with 4 KPI cards | ✅ index.html + benchmark_service.py |
| FR-02 | List and filter 108 benchmark results | ✅ benchmarks.html + api_routes.py |
| FR-03 | View confusion matrix for any experiment | ✅ benchmarks.html modal + CM images |
| FR-04 | Select preset network flows for live inference | ✅ demo.html + attack_presets.json |
| FR-05 | Configure reduction method, k, classifier for inference | ✅ demo.html dropdowns |
| FR-06 | Execute live inference via /api/predict POST endpoint | ✅ api_routes.py + inference_service.py |
| FR-07 | Display Decision Tree traversal path explanation | ✅ explain_service.py (model.decision_path()) |
| FR-08 | Display PCA component loadings for PCA inference | ✅ explain_service.py |
| FR-09 | Display feature relevance table for any configuration | ✅ explain_service.py |
| FR-10 | View MRMR feature rankings (binary and multiclass) | ✅ features.html |
| FR-11 | View PCA cumulative variance plot and verification table | ✅ features.html |
| FR-12 | View methodology and MATLAB-sklearn equivalence table | ✅ methodology.html |
| FR-13 | Serve pre-rendered EDA, confusion matrix, result images | ✅ main_routes.py static asset routes |

---

## 13. Non-Functional Requirements

| NFR | Description | Status |
|---|---|---|
| NFR-01 | Low inference latency (<1ms for DT) | Achieved: DT ~0.001ms observed in benchmarks |
| NFR-02 | Model loading with LRU cache (max 5 cached) | Implemented: model_service.py OrderedDict cache |
| NFR-03 | No authentication required (read-only demo) | Intentional design |
| NFR-04 | Max upload size 16 MB | Set in config.py |
| NFR-05 | SECRET_KEY from environment variable | config.py |

---

## 14. Constraints

1. No user-facing upload of arbitrary CSV data (only pre-defined presets used for live demo)
2. Python scikit-learn approximations of MATLAB algorithms introduce minor numerical differences (documented in methodology.html)
3. KNN models require full training data for inference (very large .joblib files: 273 MB for 79-feature KNN)
4. No formal unit test suite exists
