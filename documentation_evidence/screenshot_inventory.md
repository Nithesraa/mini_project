# Screenshot and Figure Inventory

## 1. Existing Output Images (All Verified Present on Disk)

### 1.1 EDA (Exploratory Data Analysis) Charts

| Figure ID | File Path | What It Shows | Module | Suggested Report Section | Notes |
|---|---|---|---|---|---|
| FIG-EDA-01 | `d:\Mini_Project\output\eda\class_distribution_label.png` | Binary class distribution bar chart (Anomaly 93.6% vs. Normal 6.4%) | Dataset Analysis | Chapter 3 — System Analysis, Dataset Description | Key chart showing class imbalance |
| FIG-EDA-02 | `d:\Mini_Project\output\eda\class_distribution_cat.png` | 5-class multiclass distribution (Mirai, Scan, DoS, Normal, MITM) | Dataset Analysis | Chapter 3 — System Analysis | Shows attack type distribution |
| FIG-EDA-03 | `d:\Mini_Project\output\eda\class_distributions.png` | Combined class distribution overview | Dataset Analysis | Chapter 3 — System Analysis | May be summary of EDA-01+02 |
| FIG-EDA-04 | `d:\Mini_Project\output\eda\correlation_heatmap.png` | Feature correlation heatmap (79×79) | Feature Engineering | Chapter 4 — Methodology | Shows inter-feature correlation used for MRMR justification |

### 1.2 Feature Engineering Charts

| Figure ID | File Path | What It Shows | Module | Suggested Report Section | Notes |
|---|---|---|---|---|---|
| FIG-FE-01 | `d:\Mini_Project\output\feature_engineering\pca_cumulative_variance.png` | PCA cumulative explained variance vs. component number | Feature Reduction | Chapter 4 — Methodology / PCA Analysis | Critical figure: shows elbow at k=12 captures 99.16% variance |

### 1.3 Benchmark Result Charts

| Figure ID | File Path | What It Shows | Module | Suggested Report Section | Notes |
|---|---|---|---|---|---|
| FIG-RES-01 | `d:\Mini_Project\output\results\accuracy_vs_features_binary.png` | Binary accuracy vs. feature count for each ML model and method | Benchmarks | Chapter 5 — Results and Discussion | Key comparison chart: PCA vs. MRMR at different k |
| FIG-RES-02 | `d:\Mini_Project\output\results\efficiency_frontier_binary.png` | Accuracy vs. throughput scatter (efficiency frontier) | Benchmarks | Chapter 5 — Results and Discussion | Pareto frontier visualization |

### 1.4 Confusion Matrices (Selected Key Examples)

| Figure ID | File Path | What It Shows | Suggested Report Section | Notes |
|---|---|---|---|---|
| FIG-CM-01 | `d:\Mini_Project\output\results\confusion_matrices\binary_baseline_79_Decision_Tree_cm.png` | Confusion matrix: binary DT baseline (best overall accuracy 99.897%) | Chapter 5 — Results | Most important: the reference model |
| FIG-CM-02 | `d:\Mini_Project\output\results\confusion_matrices\binary_mrmr_12_Decision_Tree_cm.png` | Confusion matrix: binary DT MRMR-12 (best compressed accuracy 99.864%) | Chapter 5 — Results | Key comparison: shows minimal degradation |
| FIG-CM-03 | `d:\Mini_Project\output\results\confusion_matrices\multiclass_baseline_79_Decision_Tree_cm.png` | Confusion matrix: multiclass DT baseline (5-class) | Chapter 5 — Results | Shows per-class performance |
| FIG-CM-04 | `d:\Mini_Project\output\results\confusion_matrices\multiclass_mrmr_12_Decision_Tree_cm.png` | Confusion matrix: multiclass DT MRMR-12 | Chapter 5 — Results | MRMR-12 multiclass performance |
| FIG-CM-05 | `d:\Mini_Project\output\results\confusion_matrices\binary_pca_12_Decision_Tree_cm.png` | Confusion matrix: binary DT PCA-12 | Chapter 5 — Results | PCA baseline comparison |
| FIG-CM-06 | `d:\Mini_Project\output\results\confusion_matrices\multiclass_pca_12_KNN_cm.png` | Confusion matrix: best multiclass model (PCA-12 KNN, 98.922%) | Chapter 5 — Results | Best multiclass performer |

**Note:** 110 confusion matrix PNG files exist in total. The above 6 are the most relevant for the report.

---

## 2. Missing Screenshots — Must Be Captured

The following screenshots should be captured by running the Flask application and taking browser screenshots.

### 2.1 Application UI Screenshots (Not Yet Captured)

| Needed Figure | How to Capture | Steps |
|---|---|---|
| FIG-UI-01: Dashboard / KPI Cards | Browser screenshot of http://127.0.0.1:5000/ | Run `python app.py`, navigate to /, take full-page screenshot |
| FIG-UI-02: Live Demo — Threat Detected (Anomaly) | Browser screenshot of /demo after clicking Execute | Select preset=Mirai UDP, task=Binary, method=MRMR, k=12, model=DT, click Execute |
| FIG-UI-03: Live Demo — Decision Tree Path Steps | Browser screenshot of /demo showing DT traversal path panel | Same as FIG-UI-02 — scroll to "Why This Prediction?" panel |
| FIG-UI-04: Live Demo — Normal Flow (Benign) | Browser screenshot showing Normal result | Select preset=Benign Industrial Normal, click Execute |
| FIG-UI-05: Benchmarks Table | Browser screenshot of /benchmarks showing 108 results table | Navigate to /benchmarks |
| FIG-UI-06: Confusion Matrix Modal | Browser screenshot of confusion matrix lightbox | Click "Inspect Matrix" for binary_mrmr_12_Decision_Tree |
| FIG-UI-07: Feature Reduction Page | Browser screenshot of /features showing MRMR rankings | Navigate to /features |
| FIG-UI-08: PCA Variance Curve Page | Browser screenshot of /features PCA section with variance plot | Navigate to /features, scroll to PCA section |
| FIG-UI-09: Methodology Page | Browser screenshot of /methodology showing MATLAB-sklearn table | Navigate to /methodology |
| FIG-UI-10: Live Demo — PCA Method selected | Browser screenshot showing PCA telemetry panel | Select method=PCA, k=12, click Execute |

---

## 3. Recommended Figures for Report (Priority Order)

| Priority | Figure ID | Source | Why Important |
|---|---|---|---|
| 1 | FIG-RES-01 | output/results/accuracy_vs_features_binary.png | Central result: shows accuracy vs. feature count trade-off across all methods |
| 2 | FIG-RES-02 | output/results/efficiency_frontier_binary.png | Shows Pareto efficiency frontier (accuracy vs. throughput) |
| 3 | FIG-CM-01 | output/results/confusion_matrices/binary_baseline_79_Decision_Tree_cm.png | Baseline reference model performance |
| 4 | FIG-CM-02 | output/results/confusion_matrices/binary_mrmr_12_Decision_Tree_cm.png | MRMR-12 compressed model performance |
| 5 | FIG-FE-01 | output/feature_engineering/pca_cumulative_variance.png | PCA variance curve (required for methodology chapter) |
| 6 | FIG-EDA-01 | output/eda/class_distribution_label.png | Dataset class imbalance visualization |
| 7 | FIG-EDA-04 | output/eda/correlation_heatmap.png | Feature correlation justifying MRMR |
| 8 | FIG-UI-01 | (to be captured) | Dashboard screenshot (system demonstration) |
| 9 | FIG-UI-02 | (to be captured) | Live demo threat detection output |
| 10 | FIG-UI-03 | (to be captured) | Decision tree explainability panel |
| 11 | FIG-CM-03 | output/results/confusion_matrices/multiclass_baseline_79_Decision_Tree_cm.png | Multiclass performance |
| 12 | FIG-UI-05 | (to be captured) | 108-model benchmarks table |

---

## 4. Suggested Proposed Figure Descriptions for Report

| Figure ID | Suggested Caption |
|---|---|
| FIG-RES-01 | Figure X.Y: Binary classification accuracy comparison across PCA and MRMR feature reduction configurations for all six machine learning algorithms. |
| FIG-RES-02 | Figure X.Y: Accuracy–throughput efficiency frontier for binary intrusion detection. Decision Tree at MRMR-12 achieves optimal Pareto trade-off. |
| FIG-CM-01 | Figure X.Y: Confusion matrix for the Decision Tree classifier operating on the full 79-feature baseline configuration (binary classification, test set of 187,735 flows). |
| FIG-CM-02 | Figure X.Y: Confusion matrix for the Decision Tree classifier operating on the MRMR top-12 feature configuration. Accuracy is within 0.033% of the baseline. |
| FIG-FE-01 | Figure X.Y: Cumulative explained variance of PCA components computed on the IoTID20 training set. 12 components capture 99.16% of total variance. |
| FIG-EDA-01 | Figure X.Y: Binary class distribution of the IoTID20 dataset. Anomalous flows comprise 93.6% of samples, indicating severe class imbalance. |

---

## 5. Existing Output Plot Sizes (Verified)

| File | Size | Aspect |
|---|---|---|
| accuracy_vs_features_binary.png | 164 KB | — |
| efficiency_frontier_binary.png | 200 KB | — |
| pca_cumulative_variance.png | 79.6 KB | — |
| class_distribution_label.png | 41 KB | — |
| class_distribution_cat.png | 61 KB | — |
| class_distributions.png | 246 KB | Combined |
| correlation_heatmap.png | 364 KB | Large heatmap |
| binary confusion matrices | ~83–97 KB each | Standard |
| multiclass confusion matrices | ~147–173 KB each | Larger (5×5 grid) |
