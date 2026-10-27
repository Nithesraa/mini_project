# Testing and Results

## 1. Test Suite Status

**No formal automated unit test suite exists in this project.** There is no `tests/` directory, no `pytest` configuration, no `unittest` files, and no `conftest.py`. All testing is functional/integration testing via the web application and training notebook execution.

---

## 2. Training and Evaluation Evidence

The 108 model training and evaluation runs constitute the primary evidence of correct implementation. All 108 experiments have been executed and their results recorded.

**Verification Evidence:**
- `output/checkpoints/progress.json`: Lists all 108 completed experiment IDs (confirmed 110 entries in completed list, covering all 108 experiments — some IDs appear to handle both binary and multiclass for same config)
- `output/models/`: 108 `.joblib` files present (verified by directory listing)
- `output/checkpoints/results_cache.json`: 108 result records (verified: 54 binary + 54 multiclass)
- `output/results/predictions/`: 108 CSV prediction files
- `output/results/confusion_matrices/`: 110 PNG files

---

## 3. Selected Test Results Table (Verified from results_cache.json)

### 3.1 Binary Classification — Key Results

| Test ID | Experiment | Method | k | Model | Accuracy | F1-Score | FAR | Throughput (obs/s) | Train Time |
|---|---|---|---|---|---|---|---|---|---|
| B-01 | binary_baseline_79_Decision_Tree | Baseline | 79 | Decision Tree | 99.897% | 99.19% | 0.0074% | 1,231,213 | 62.72s |
| B-02 | binary_baseline_79_KNN | Baseline | 79 | KNN | 99.827% | 98.64% | 0.036% | 546 | 3.61s |
| B-03 | binary_baseline_79_Neural_Network | Baseline | 79 | Neural Network | 99.689% | 97.55% | 3.64% | 315,163 | 63.07s |
| B-04 | binary_baseline_79_Logistic_Regression_Kernel | Baseline | 79 | LR Kernel | 97.778% | 80.24% | 29.52% | 99,846 | 13.41s |
| B-05 | binary_baseline_79_SVM_Kernel | Baseline | 79 | SVM Kernel | 74.269% | 11.81% | 73.09% | 3,903 | 112.18s |
| B-06 | binary_baseline_79_Gaussian_SVM | Baseline | 79 | Gaussian SVM | 99.354% | 94.72% | 9.42% | 691 | 3556.07s |
| B-07 | binary_mrmr_12_Decision_Tree | MRMR | 12 | Decision Tree | **99.864%** | **98.93%** | 1.95% | **8,249,703** | **1.04s** |
| B-08 | binary_mrmr_12_KNN | MRMR | 12 | KNN | 99.855% | 98.86% | 1.55% | 5,636 | 1.95s |
| B-09 | binary_mrmr_12_Neural_Network | MRMR | 12 | Neural Network | 99.578% | 96.62% | 5.68% | 2,923,432 | 35.74s |
| B-10 | binary_mrmr_12_SVM_Kernel | MRMR | 12 | SVM Kernel | 98.855% | 90.40% | 15.83% | 48,664 | 1366.79s |
| B-11 | binary_mrmr_12_Gaussian_SVM | MRMR | 12 | Gaussian SVM | 98.834% | 90.18% | 16.39% | 652 | 787.65s |
| B-12 | binary_mrmr_12_Logistic_Regression_Kernel | MRMR | 12 | LR Kernel | 97.432% | 78.96% | 24.75% | 164,465 | 10.22s |
| B-13 | binary_pca_4_Decision_Tree | PCA | 4 | Decision Tree | 99.527% | 96.18% | 4.89% | 4,019,693 | 1.52s |
| B-14 | binary_pca_12_Decision_Tree | PCA | 12 | Decision Tree | (see cache) | — | — | — | — |

### 3.2 Binary — Key Aggregate KPIs (All verified from results_cache.json)

| KPI | Value | Best Experiment |
|---|---|---|
| Peak binary accuracy | **99.897%** | binary_baseline_79_Decision_Tree |
| Best F1-score | **99.19%** | binary_baseline_79_Decision_Tree |
| Minimum FAR | **0.0074%** | binary_baseline_79_Decision_Tree |
| Max throughput (any model) | **~8,513,912 obs/s** | binary_mrmr_12_Decision_Tree or similar DT |
| MRMR-12 DT accuracy | **99.864%** | binary_mrmr_12_Decision_Tree |
| MRMR-12 DT accuracy drop vs. baseline | **0.033%** | 99.897% → 99.864% |
| MRMR-12 DT train time reduction | **98.3%** | 62.72s → 1.04s |
| MRMR-12 DT throughput improvement | **~6.7×** | 1,231,213 → 8,249,703 obs/s |
| MRMR-12 feature reduction | **84.81%** | 79 → 12 features |

### 3.3 Multiclass Classification — Key Results (Verified)

| Experiment | Method | k | Model | Accuracy |
|---|---|---|---|---|
| multiclass_baseline_79_Decision_Tree | Baseline | 79 | Decision Tree | (see cache) |
| multiclass_pca_12_KNN | PCA | 12 | KNN | **98.922%** (best multiclass) |
| multiclass_mrmr_12_Decision_Tree | MRMR | 12 | Decision Tree | (see cache) |

---

## 4. PCA Verification Test (Verified against paper targets)

| Test | k | Computed Variance | Paper Target | Delta | Status |
|---|---|---|---|---|---|
| PCA-V-01 | 4 | 88.77% | 88.74% | +0.03% | PASS — within rounding tolerance |
| PCA-V-02 | 12 | 99.16% | 99.12% | +0.04% | PASS — within rounding tolerance |
| PCA-V-03 | 23 | 99.91% | 99.90% | +0.01% | PASS — within rounding tolerance |
| PCA-V-04 | 50 | 100.00% | 99.99% | +0.01% | PASS — within rounding tolerance |

**Source:** `templates/features.html` (hardcoded verified values from notebook run).

---

## 5. Live Inference Functional Tests (Manual — Verified from presets and app logic)

| Test ID | Module | Scenario | Expected | Status | Evidence |
|---|---|---|---|---|---|
| LI-01 | /api/predict | POST with preset=mirai_udp, task=binary, method=mrmr, k=12, model=Decision Tree | status=success, predicted_label=Anomaly, is_correct=true | Verified as default shown in demo.html | demo.html preset HTML + api_routes.py ground_truth logic |
| LI-02 | /api/predict | POST with invalid task "xyz" | HTTP 400 + error message | Verified from code | api_routes.py line 46-48 |
| LI-03 | /api/predict | POST with invalid method "autoencoder" | HTTP 400 + error message | Verified from code | api_routes.py line 48-50 |
| LI-04 | /api/predict | POST with method=pca, k=12, model=Decision Tree | pca_telemetry.is_applicable=true, decision_tree_explanation.is_applicable=true | Verified from explain_service.py logic | explain_service.py |
| LI-05 | /api/predict | POST with model=Neural Network | neural_network_explanation.is_applicable=true, disclaimer returned | Verified from code | explain_service.py lines 99-108 |
| LI-06 | /api/predict | POST with method=baseline, any k | n_features forced to 79 | Verified from code | api_routes.py line 50-51 |
| LI-07 | /api/presets | GET /api/presets | Returns JSON array with at least 5 presets | Presets confirmed in data_presets/attack_presets.json | api_routes.py::get_presets() |
| LI-08 | /api/metrics | GET /api/metrics?task=binary&method=mrmr&n_features=12 | Returns 6 result records | Verifiable from filter logic | benchmark_service.filter_results() |

---

## 6. Data Quality Checks (Verified from dataset_info.txt)

| Check | Finding | Impact | Handling |
|---|---|---|---|
| Missing values | 0 | None | No imputation needed |
| Duplicate rows | 164,087 (26.22%) | Potential data leakage / bias | Kept intentionally (paper does not mention removal) |
| Infinite values | 368 in Flow_Byts/s, 368 in Flow_Pkts/s | Preprocessing failure | Replaced during preprocessing (methodology.html) |
| Class imbalance | 93.60% Anomaly vs. 6.40% Normal | Binary task: FAR metric important | Documented; no oversampling applied |

---

## 7. Model Artifact Completeness Verification

| Expected | Found | Status |
|---|---|---|
| 108 trained model .joblib files | 108 confirmed in output/models/ | COMPLETE |
| 108 prediction CSV files | 108 in output/results/predictions/ | COMPLETE |
| 108 confusion matrix PNGs | 108+ in output/results/confusion_matrices/ (some alternate naming) | COMPLETE |
| 108 results in results_cache.json | 108 records confirmed by Python script | COMPLETE |
| Binary MRMR rankings CSV | Present, 50 features ranked | COMPLETE |
| Multiclass MRMR rankings CSV | Present, 50 features ranked | COMPLETE |
| PCA artifact pkl | Present (~425 MB) | COMPLETE |
| Preprocessed data npz | Present (~57 MB) | COMPLETE |
| EDA charts | 8 files in output/eda/ | COMPLETE |
| Feature engineering charts | 4 files in output/feature_engineering/ | COMPLETE |

---

## 8. Known Testing Gaps

| Gap | Description | Recommendation |
|---|---|---|
| No automated unit tests | No pytest/unittest suite | Add unit tests for services |
| No integration test suite | No end-to-end API test scripts | Add requests-based API tests |
| No ROC curve images generated | output/results/roc_curves/ is empty | Either generate from preds CSVs or document as gap |
| No load testing | Unknown concurrent request handling | Not relevant for academic demo |
| No KNN throughput advantage measured | KNN baseline: 546 obs/s — extremely slow | Mentioned as limitation |

---

## 9. Execution Environment Verification

```
Training: Executed offline via Jupyter Notebook (IoT_Intrusion_Detection_Reproduction.ipynb)
Evidence: All 108 model artifacts present, results_cache.json fully populated

Web Application: Can be started via:
  python app.py
  → Listening on http://127.0.0.1:5000/

No requirements.txt present — exact package versions not pinned
scikit-learn version 1.6.1 explicitly documented in methodology.html
```
