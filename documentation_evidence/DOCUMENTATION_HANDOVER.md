# DOCUMENTATION HANDOVER

**Prepared for:** ChatGPT / Technical Writer
**Prepared by:** Antigravity — Automated Project Analysis
**Date:** 2026-10-20
**Project Workspace:** `d:\Mini_Project`

---

## 1. Verified Project Title and Purpose

**Title (Verified):**
> "Enhancing Security in Industrial IoT Networks: Machine Learning Solutions for Feature Selection and Reduction"
> *(Same title as the IEEE Access 2024 base paper by Houkan et al., which this project reproduces)*

**Application Title in UI:**
> "Industrial IoT Network Intrusion Detection — Experimental Reproduction and Benchmarking Suite"
> (from `templates/index.html` — page title: "IIoT Intrusion Detection Lab")

**Purpose:**
This project reproduces, in Python + Flask + scikit-learn, the experimental methodology of Houkan et al. (IEEE Access, 2024) which evaluated PCA and MRMR dimensionality reduction for machine learning-based intrusion detection in Industrial IoT networks. The project trains 108 ML models on the IoTID20 dataset (625,783 network flows), evaluates them, and provides an interactive web dashboard for live inference and explainability.

---

## 2. Main Technologies and Architecture

**Technology Stack:**
- Python + Flask (web framework)
- scikit-learn 1.6.1 (ML training and inference)
- joblib (model serialization)
- NumPy + pandas (numerical computing)
- Vanilla HTML/CSS/JavaScript (no frontend framework)

**Architecture:** Two-subsystem design:
1. **Offline training pipeline** (Jupyter Notebook) — generates all 108 trained models and artifacts
2. **Online Flask web application** — serves trained artifacts for live inference and visualization

**Flask application pattern:** Application Factory + Blueprints (main_bp for pages, api_bp for REST API) + 5 service singletons

---

## 3. Implemented Modules

| Module | File | Status |
|---|---|---|
| Application factory | app.py | Complete |
| Configuration | config.py | Complete |
| Page routes | routes/main_routes.py | Complete (5 pages + 4 static asset routes) |
| API routes | routes/api_routes.py | Complete (3 endpoints) |
| Model service (LRU cache) | services/model_service.py | Complete |
| Benchmark service | services/benchmark_service.py | Complete |
| Inference service | services/inference_service.py | Complete |
| Explainability service | services/explain_service.py | Complete |
| Feature catalog | services/feature_catalog.py | Complete (79 features, 9 categories) |
| Attack preset library | data_presets/attack_presets.json | Complete (5+ presets) |
| Frontend HTML templates | templates/*.html | Complete (6 pages) |
| CSS styling | static/css/main.css | Complete |
| Demo JavaScript | static/js/demo.js | Complete |
| Training notebook | IoT_Intrusion_Detection_Reproduction.ipynb | EXECUTED — all 108 artifacts generated |

---

## 4. Most Important Test Results and Evidence

### Peak Binary Classification KPIs (All from results_cache.json — VERIFIED)

| KPI | Value | Experiment |
|---|---|---|
| Peak binary accuracy | **99.897%** | binary_baseline_79_Decision_Tree |
| MRMR-12 compressed accuracy | **99.864%** | binary_mrmr_12_Decision_Tree |
| Accuracy drop (MRMR-12 vs. baseline) | **0.033%** | Trivial degradation |
| Feature compression ratio | **84.81%** | 79 → 12 features |
| Max inference throughput | **~8.25M obs/s** | binary_mrmr_12_Decision_Tree |
| Baseline DT throughput | **1.23M obs/s** | binary_baseline_79_Decision_Tree |
| Throughput improvement | **~6.7×** | MRMR-12 DT vs. baseline DT |
| MRMR-12 training time | **1.04 seconds** | vs. 62.72s for baseline DT |
| Training time reduction | **98.3%** | MRMR-12 DT vs. baseline DT |
| Minimum False Alarm Rate | **0.0074%** | binary_baseline_79_Decision_Tree |
| KNN baseline model size | **273 MB** | model_binary_baseline_79_KNN.joblib |
| Best multiclass accuracy | **98.922%** | multiclass_pca_12_KNN |

### PCA Verification (All PASS — within ≤0.04% of paper targets)
- k=4: 88.77% vs. 88.74% target (+0.03%)
- k=12: 99.16% vs. 99.12% target (+0.04%)
- k=23: 99.91% vs. 99.90% target (+0.01%)
- k=50: 100.00% vs. 99.99% target (+0.01%)

---

## 5. Most Useful Screenshots, Tables, and Diagrams

### Immediately Available Figures (from output/ directory):
1. `output/results/accuracy_vs_features_binary.png` — **TOP PRIORITY** — Accuracy vs. feature count across all methods/models
2. `output/results/efficiency_frontier_binary.png` — Accuracy vs. throughput Pareto frontier
3. `output/feature_engineering/pca_cumulative_variance.png` — PCA variance curve
4. `output/eda/class_distribution_label.png` — Binary class imbalance chart
5. `output/eda/correlation_heatmap.png` — 79×79 feature correlation heatmap
6. `output/results/confusion_matrices/binary_baseline_79_Decision_Tree_cm.png` — Baseline CM
7. `output/results/confusion_matrices/binary_mrmr_12_Decision_Tree_cm.png` — MRMR-12 CM

### Key Tables for Report (Can be typeset from evidence):
- Table: 108 experiment results (from results_cache.json — 9 columns per row)
- Table: MRMR top-12 binary feature rankings (from mrmr_binary_rankings.csv)
- Table: MRMR top-12 multiclass feature rankings (from mrmr_multiclass_rankings.csv)
- Table: MATLAB-to-scikit-learn algorithm mapping (from methodology.html)
- Table: PCA cumulative variance verification (from features.html)
- Table: Dataset statistics (from dataset_info.txt)

### Mermaid Diagrams (Ready in system_architecture.md):
- High-level architecture diagram
- Inference sequence diagram

---

## 6. Documentation Format Requirements

| Requirement | Status |
|---|---|
| Institution | SASTRA Deemed University (assumed) |
| Format template | NOT FOUND in workspace — must be obtained from department |
| Assumed structure | 6 chapters + prelim pages (see documentation_format_analysis.md) |
| Citation style | IEEE (assumed — verify with department) |
| Key formatting | Times New Roman 12pt, 1.5 line spacing, 1.5" left margin (assumed) |

**The user MUST obtain the official SASTRA department report template before formatting.**

---

## 7. Missing Information That Must Be Supplied

| # | Item | Critical? |
|---|---|---|
| 1 | Student name(s) and register number(s) | YES — needed for title page |
| 2 | Supervisor name and designation | YES — needed for title page and certificate |
| 3 | Department name | YES |
| 4 | Academic year and semester | YES |
| 5 | Official SASTRA report format template | YES |
| 6 | 5–8 literature survey papers on IIoT NIDS and dimensionality reduction | YES — Chapter 2 blocked |
| 7 | Full citation for Houkan et al. 2024 (DOI, volume, page numbers) | MEDIUM |
| 8 | Full citation for IoTID20 dataset (Ullah & Mahmoud) | MEDIUM |
| 9 | UI screenshots (run the app and capture 8–10 browser screenshots) | HIGH — Chapter 5 |
| 10 | Python/library version details (`pip freeze` output) | LOW |

---

## 8. Unresolved Implementation Issues

| Issue | Impact on Report |
|---|---|
| ROC curve images are absent (empty directory) | Mention as limitation; can generate from preds CSVs if needed |
| SVM Kernel shows very poor performance (74% binary accuracy) | Report as empirical finding — algorithm choice discussion |
| KNN requires 273 MB model file — impractical for IIoT edge | Cite as evidence supporting the need for feature reduction |
| No automated test suite | Acknowledge as limitation; note functional validation via 108 experiments |
| Exact MRMR library not documented | Mention as reproducibility gap; notebook inspection would clarify |

---

## 9. Paths to All Generated Documentation Evidence Files

All files are in: `d:\Mini_Project\documentation_evidence\`

| File | Purpose |
|---|---|
| [`documentation_format_analysis.md`](file:///d:/Mini_Project/documentation_evidence/documentation_format_analysis.md) | Template analysis — institutional format requirements |
| [`project_overview.md`](file:///d:/Mini_Project/documentation_evidence/project_overview.md) | Full project identity, objectives, requirements, dataset |
| [`technology_stack.md`](file:///d:/Mini_Project/documentation_evidence/technology_stack.md) | All technologies, ML algorithms, artifacts |
| [`system_architecture.md`](file:///d:/Mini_Project/documentation_evidence/system_architecture.md) | Architecture diagrams, data flows, Mermaid sources |
| [`module_analysis.md`](file:///d:/Mini_Project/documentation_evidence/module_analysis.md) | All 12 modules analyzed in detail |
| [`database_and_api_analysis.md`](file:///d:/Mini_Project/documentation_evidence/database_and_api_analysis.md) | Flat-file data schema, all API endpoints |
| [`algorithm_and_code_analysis.md`](file:///d:/Mini_Project/documentation_evidence/algorithm_and_code_analysis.md) | MRMR, PCA, DT path, LRU cache algorithms |
| [`testing_and_results.md`](file:///d:/Mini_Project/documentation_evidence/testing_and_results.md) | 108 experiment results, functional tests, KPIs |
| [`screenshot_inventory.md`](file:///d:/Mini_Project/documentation_evidence/screenshot_inventory.md) | Existing figures inventory + screenshots to capture |
| [`reference_inventory.md`](file:///d:/Mini_Project/documentation_evidence/reference_inventory.md) | All references found and needed |
| [`report_structure_mapping.md`](file:///d:/Mini_Project/documentation_evidence/report_structure_mapping.md) | Per-chapter mapping of evidence to report sections |
| [`limitations_and_future_scope.md`](file:///d:/Mini_Project/documentation_evidence/limitations_and_future_scope.md) | Known bugs, limitations, future enhancements |
| [`SOURCE_FILE_INDEX.md`](file:///d:/Mini_Project/documentation_evidence/SOURCE_FILE_INDEX.md) | Complete file inventory with paths and descriptions |
| [`DOCUMENTATION_GAPS.md`](file:///d:/Mini_Project/documentation_evidence/DOCUMENTATION_GAPS.md) | All missing information and actions required |
| [`DOCUMENTATION_HANDOVER.md`](file:///d:/Mini_Project/documentation_evidence/DOCUMENTATION_HANDOVER.md) | This file |

---

## 10. Recommended Chapter-by-Chapter Writing Order

Write in this sequence for maximum coherence and minimal rework:

| Step | Chapter | Reason |
|---|---|---|
| 1 | **Abstract** | Short, forces core summary — good starting anchor |
| 2 | **Chapter 5: Results and Discussion** | Data is the strongest part; all numbers verified |
| 3 | **Chapter 4: Implementation / Methodology** | Flows from understanding the results |
| 4 | **Chapter 3: System Analysis and Design** | Flows from methodology |
| 5 | **Chapter 1: Introduction** | Can reference results and objectives once chapters 3–5 are drafted |
| 6 | **Chapter 6: Conclusion and Future Scope** | Write after Introduction to ensure coherence |
| 7 | **Chapter 2: Literature Survey** | Needs external paper research — do last but insert second |
| 8 | **Preliminary pages** (after all chapters) | Title page, ToC, List of Figures, etc. done last |

---

## 11. Quick-Reference Verified Facts for ChatGPT

Use these verified numbers directly in the report without modification:

```
Dataset: IoTID20 — 625,783 network flows × 86 columns
Features used: 79 (after removing metadata headers and label columns)
Binary labels: Anomaly (585,710 = 93.60%), Normal (40,073 = 6.40%)
Multiclass: Mirai 66.43%, Scan 12.03%, DoS 9.49%, Normal 6.40%, MITM ARP 5.65%
Train/test split: 70%/30% stratified, random_state=42 → 438,048 / 187,735
Missing values: 0 | Duplicates: 164,087 (26.22%) — kept intentionally
Infinite values: 368 each in Flow_Byts/s and Flow_Pkts/s — replaced

Feature reduction configurations: k ∈ {4, 12, 23, 50} for PCA and MRMR; k=79 for baseline
Total experiments: 108 (2 tasks × 9 feature configs × 6 classifiers)
All 108 models trained and saved as .joblib files — CONFIRMED

Top 12 Binary MRMR Features: Dst_Port, Init_Bwd_Win_Byts, Fwd_Pkt_Len_Std, ACK_Flag_Cnt, Src_Port, Fwd_Header_Len, Pkt_Len_Std, Bwd_Header_Len, Protocol, TotLen_Fwd_Pkts, Pkt_Len_Var, Subflow_Fwd_Byts
Top 12 Multiclass MRMR Features: SYN_Flag_Cnt, Fwd_IAT_Tot, Protocol, Flow_IAT_Min, Fwd_Pkt_Len_Std, Flow_IAT_Mean, Dst_Port, ACK_Flag_Cnt, Idle_Min, Idle_Mean, Bwd_IAT_Mean, Init_Bwd_Win_Byts

PCA Cumulative Variance:
  k=4: 88.77% (paper: 88.74%, Δ=+0.03%) ✓
  k=12: 99.16% (paper: 99.12%, Δ=+0.04%) ✓
  k=23: 99.91% (paper: 99.90%, Δ=+0.01%) ✓
  k=50: 100.00% (paper: 99.99%, Δ=+0.01%) ✓

Key Binary Results:
  Baseline DT (79 features): Acc=99.897%, F1=99.19%, FAR=0.0074%, Throughput=1,231,213/s, Train=62.72s
  MRMR-12 DT (12 features): Acc=99.864%, F1=98.93%, FAR=1.95%, Throughput=8,249,703/s, Train=1.04s
  Accuracy drop: 0.033% | Training time reduction: 98.3% | Throughput gain: 6.7×
  Feature compression: 84.81% (79→12)

SVM Kernel (known poor performer):
  binary_baseline_79_SVM_Kernel: Acc=74.27%, FAR=73.09% — kernel approximation issue

Best Multiclass: multiclass_pca_12_KNN: 98.922%

ML Algorithms (6): Decision Tree, KNN, Neural Network (MLP 25 neurons), Gaussian SVM, SVM Kernel (RFF), Logistic Regression Kernel (Nystroem)
```
