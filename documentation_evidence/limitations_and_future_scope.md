# Limitations and Future Scope

## 1. Current Limitations (Verified from Implementation)

### 1.1 Technical Limitations

| # | Limitation | Severity | Evidence |
|---|---|---|---|
| L-01 | **No requirements.txt** — Exact Python/library versions not pinned | Medium | No requirements.txt in workspace; scikit-learn 1.6.1 stated but unverified by file |
| L-02 | **KNN is impractical for real-time edge deployment** — 273 MB model file (79-feature baseline KNN), throughput of only 546 obs/s | High (for IIoT goal) | output/models/model_binary_baseline_79_KNN.joblib = 280 MB; results_cache.json |
| L-03 | **No real-time packet capture** — Only pre-defined presets used; no network stream ingestion | High (for production) | api_routes.py: only reads from attack_presets.json |
| L-04 | **No WSGI/production server** — Running Flask dev server; not suitable for multi-user production use | Medium | app.py: `app.run(debug=True)` only |
| L-05 | **Class imbalance not addressed** — 93.6% Anomaly vs. 6.4% Normal; no SMOTE, class weighting, or oversampling applied | Medium | dataset_info.txt; FAR values are low but recall varies across classifiers |
| L-06 | **Duplicate rows retained (26.22%)** — Paper decision to keep duplicates may inflate accuracy metrics | Medium | dataset_info.txt: "Duplicates KEPT (paper does not mention removal)" |
| L-07 | **ROC curve images not generated** — output/results/roc_curves/ is empty | Low (report only) | Directory listing confirmed empty |
| L-08 | **No automated test suite** — No pytest/unittest files; functional testing only via browser | Medium (quality) | No tests/ directory found |
| L-09 | **Hardcoded default SECRET_KEY** — Fallback key "iiot-nids-secret-key-2024" in config.py | Low (local demo only) | config.py line 26 |
| L-10 | **SVM Kernel poor performance** — binary_baseline_79_SVM_Kernel: 74.27% accuracy, 73.09% FAR | High finding | results_cache.json |
| L-11 | **LRU cache limited to 5 models** — Loading a 6th model evicts least-used; large KNN models cause I/O delays | Low | model_service.py: max_cached=5 |
| L-12 | **No user authentication** — Anyone with local access can run inference | Not applicable for local demo | app.py — intentional design |
| L-13 | **Only binary classification confusion matrices available in some naming conventions** — Some CM files may use alternate naming | Low | confusion_matrices/ listing: two formats exist |

---

### 1.2 Scientific/Methodological Limitations

| # | Limitation | Evidence / Notes |
|---|---|---|
| SL-01 | **Single dataset evaluation** — Only IoTID20 used; generalizability to other IIoT datasets (e.g., UNSW-NB15, CIC-IDS2017) not assessed | Scope limitation |
| SL-02 | **No cross-validation** — Single 70/30 stratified split; variance across splits not reported | methodology.html: fixed seed=42 |
| SL-03 | **MATLAB vs. Python numerical differences** — scikit-learn approximations of MATLAB algorithms may introduce minor performance discrepancies | methodology.html: "publication-grade equivalence" but not identical |
| SL-04 | **MRMR implementation details not fully visible** — MRMR computed in Jupyter notebook; exact Python library used is not recorded in web app code | Notebook not read (very large binary file) |
| SL-05 | **No adversarial robustness testing** — Models not tested against adversarial input perturbations | Out of scope |
| SL-06 | **9-class sub-category not evaluated** — dataset_info.txt shows 9 sub-categories; only binary and 5-class targets used | dataset_info.txt note |

---

## 2. Known Issues

| # | Issue | Impact | Status |
|---|---|---|---|
| I-01 | ROC curve directory is empty | Missing ROC curve visualizations for report | Can be regenerated from preds CSV files |
| I-02 | confusion matrix naming inconsistency — two naming formats (e.g., `binary_baseline_79_Gaussian_SVM_cm.png` vs. `cm_binary_baseline_79_Decision_Tree.png`) | Benchmark service handles both formats; low risk | Handled in benchmark_service.get_confusion_matrix_filename() |
| I-03 | SVM Kernel performance collapse at low feature counts | Not a bug — inherent kernel approximation limitation with few features | Documented as finding |

---

## 3. Future Scope (Realistic, Evidence-Based)

### 3.1 Short-Term Improvements (Technically Feasible)

| # | Enhancement | Description |
|---|---|---|
| FS-01 | **Generate ROC curves** | Compute and save ROC curves for all 108 experiments from prediction CSVs |
| FS-02 | **Add requirements.txt** | Pin all package versions for reproducibility |
| FS-03 | **Extend live demo to user-uploaded CSV** | Allow users to upload a custom network flow row for inference |
| FS-04 | **Add cross-validation** | 5-fold stratified cross-validation to report variance bounds on accuracy |
| FS-05 | **Add automated test suite** | pytest-based unit tests for all service methods |
| FS-06 | **Address class imbalance** | Test SMOTE oversampling or class_weight='balanced' and compare impact on FAR |
| FS-07 | **Remove duplicate rows** | Retrain with deduplication and compare accuracy to current results |

### 3.2 Medium-Term Improvements

| # | Enhancement | Description |
|---|---|---|
| FS-08 | **Cross-dataset validation** | Apply trained models (or retrain pipeline) on UNSW-NB15, CIC-IoT2023 to test generalizability |
| FS-09 | **Real-time packet capture integration** | Integrate with CICFlowMeter or PyShark to process live network traffic |
| FS-10 | **Production deployment** | Add Gunicorn + Nginx configuration for multi-user web service |
| FS-11 | **Additional algorithms** | Random Forest, XGBoost, LightGBM comparison against the 6 current classifiers |
| FS-12 | **SHAP explainability** | Replace DT path traversal with SHAP values for model-agnostic explanations |

### 3.3 Long-Term Research Extensions

| # | Enhancement | Description |
|---|---|---|
| FS-13 | **Federated learning for IIoT** | Distribute training across edge nodes without centralizing raw data |
| FS-14 | **Concept drift detection** | Monitor model performance degradation as new attack patterns emerge |
| FS-15 | **Embedded system deployment** | Port MRMR-12 Decision Tree to Raspberry Pi / Arduino for actual edge evaluation |
| FS-16 | **Supervised autoencoder reduction** | Replace unsupervised PCA with supervised variational autoencoder for dimensionality reduction |
| FS-17 | **Adversarial attack robustness** | Test models against evasion attacks (adversarial feature perturbations) |

---

## 4. Comparison: Current vs. Ideal State

| Aspect | Current State | Ideal State |
|---|---|---|
| Feature reduction validation | 4 PCA checkpoints verified vs. paper | Full statistical comparison including confidence intervals |
| Evaluation | Single train/test split | 5-fold cross-validation |
| Dataset | IoTID20 only | Multi-dataset evaluation |
| Explainability | DT path only; MLP has no local explanation | SHAP or LIME for all model types |
| Deployment | Flask dev server, local only | Production-grade WSGI deployment |
| Test coverage | 0% automated | ≥80% unit test coverage |
| Real-time inference | Static presets only | Live network stream integration |
