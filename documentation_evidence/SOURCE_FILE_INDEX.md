# Source File Index

## Complete Index of All Relevant Project Source Files

### Core Application Files

| File | Path | Size | Purpose | Key Contents |
|---|---|---|---|---|
| app.py | `d:\Mini_Project\app.py` | 642 B | Flask application factory | Blueprint registration, server config |
| config.py | `d:\Mini_Project\config.py` | 1,250 B | Path constants + server config | All artifact paths, SECRET_KEY, MAX_CONTENT_LENGTH |

### Route Handlers (Routes/)

| File | Path | Size | Purpose |
|---|---|---|---|
| main_routes.py | `d:\Mini_Project\routes\main_routes.py` | 2,646 B | Page routes (/, /demo, /benchmarks, /features, /methodology, static assets) |
| api_routes.py | `d:\Mini_Project\routes\api_routes.py` | 4,048 B | REST API (/api/presets, /api/predict, /api/metrics) |

### Service Layer (Services/)

| File | Path | Size | Purpose | Key Algorithms |
|---|---|---|---|---|
| model_service.py | `d:\Mini_Project\services\model_service.py` | 3,245 B | Model loading with LRU cache | LRU eviction (OrderedDict) |
| benchmark_service.py | `d:\Mini_Project\services\benchmark_service.py` | 2,256 B | Read results_cache.json | KPI computation |
| inference_service.py | `d:\Mini_Project\services\inference_service.py` | 4,383 B | End-to-end inference pipeline | Feature reduction, prediction, latency measurement |
| explain_service.py | `d:\Mini_Project\services\explain_service.py` | 9,961 B | Explainability engine | DT path traversal, PCA loadings, feature table |
| feature_catalog.py | `d:\Mini_Project\services\feature_catalog.py` | 21,477 B | 79-feature metadata catalog | All feature definitions, units, relevance text |

### HTML Templates (Templates/)

| File | Path | Size | Purpose |
|---|---|---|---|
| base.html | `d:\Mini_Project\templates\base.html` | 2,573 B | Shared layout: navbar, footer |
| index.html | `d:\Mini_Project\templates\index.html` | 5,689 B | Dashboard: KPI cards, research motivation, dataset stats |
| demo.html | `d:\Mini_Project\templates\demo.html` | 10,526 B | Live inference UI: presets, controls, results panels |
| benchmarks.html | `d:\Mini_Project\templates\benchmarks.html` | 6,693 B | 108-model results table with filter controls and CM modal |
| features.html | `d:\Mini_Project\templates\features.html` | 7,225 B | PCA verification table, MRMR rankings, 79-feature catalog |
| methodology.html | `d:\Mini_Project\templates\methodology.html` | 6,844 B | End-to-end pipeline diagram, MATLAB-sklearn mapping table |

### Static Assets (Static/)

| File | Path | Size | Purpose |
|---|---|---|---|
| main.css | `d:\Mini_Project\static\css\main.css` | 12,354 B | Complete CSS for dark-theme web application |
| demo.js | `d:\Mini_Project\static\js\demo.js` | 12,128 B | Live demo JavaScript: API calls, DOM updates, panel rendering |

### Data Files

| File | Path | Size | Purpose |
|---|---|---|---|
| attack_presets.json | `d:\Mini_Project\data_presets\attack_presets.json` | 35,594 B | Authentic test-set network flow presets for live demo |
| IoT Network Intrusion Dataset.csv | `d:\Mini_Project\Data\IoT Network Intrusion Dataset.csv` | ~295 MB | Original IoTID20 dataset (625,783 rows × 86 columns) |

### Training Notebook

| File | Path | Size | Purpose |
|---|---|---|---|
| IoT_Intrusion_Detection_Reproduction.ipynb | `d:\Mini_Project\IoT_Intrusion_Detection_Reproduction.ipynb` | 454,574 B | Complete offline training pipeline |

### Base Reference Paper

| File | Path | Size | Purpose |
|---|---|---|---|
| Enhancing_Security...pdf | `d:\Mini_Project\basepaper\Enhancing_Security_in_Industrial_IoT_Networks_Machine_Learning_Solutions_for_Feature_Selection_and_Reduction.pdf` | 7,325,104 B | Houkan et al. IEEE Access 2024 — the paper being reproduced |

### Checkpoint Artifacts (output/checkpoints/)

| File | Path | Size | Purpose |
|---|---|---|---|
| results_cache.json | `d:\Mini_Project\output\checkpoints\results_cache.json` | 55,436 B | 108 experiment benchmark results |
| progress.json | `d:\Mini_Project\output\checkpoints\progress.json` | 4,248 B | Training progress tracking |
| preprocessed_data.npz | `d:\Mini_Project\output\checkpoints\preprocessed_data.npz` | ~57 MB | Compressed feature arrays (train+test) |
| preprocessed_meta.pkl | `d:\Mini_Project\output\checkpoints\preprocessed_meta.pkl` | 2,393 B | Feature names, LabelEncoders |
| pca_result.pkl | `d:\Mini_Project\output\checkpoints\pca_result.pkl` | ~425 MB | Fitted PCA object, cumulative variance |

### Feature Engineering Artifacts (output/feature_engineering/)

| File | Path | Purpose |
|---|---|---|
| mrmr_binary_rankings.csv | `d:\Mini_Project\output\feature_engineering\mrmr_binary_rankings.csv` | Top 50 binary MRMR feature rankings |
| mrmr_multiclass_rankings.csv | `d:\Mini_Project\output\feature_engineering\mrmr_multiclass_rankings.csv` | Top 50 multiclass MRMR feature rankings |
| pca_cumulative_variance.png | `d:\Mini_Project\output\feature_engineering\pca_cumulative_variance.png` | PCA variance curve chart |
| pca_explained_variance.csv | `d:\Mini_Project\output\feature_engineering\pca_explained_variance.csv` | Per-component explained variance |

### EDA Artifacts (output/eda/)

| File | Path | Purpose |
|---|---|---|
| class_distribution_label.png | `d:\Mini_Project\output\eda\class_distribution_label.png` | Binary class distribution chart |
| class_distribution_cat.png | `d:\Mini_Project\output\eda\class_distribution_cat.png` | 5-class distribution chart |
| class_distributions.png | `d:\Mini_Project\output\eda\class_distributions.png` | Combined class distributions |
| correlation_heatmap.png | `d:\Mini_Project\output\eda\correlation_heatmap.png` | 79×79 feature correlation heatmap |
| dataset_info.txt | `d:\Mini_Project\output\eda\dataset_info.txt` | Dataset shape, dtypes, missing values, class counts |
| class_distribution_label.csv | `d:\Mini_Project\output\eda\class_distribution_label.csv` | Binary class count CSV |
| class_distribution_cat.csv | `d:\Mini_Project\output\eda\class_distribution_cat.csv` | 5-class count CSV |
| class_distribution_subcat.csv | `d:\Mini_Project\output\eda\class_distribution_subcat.csv` | 9-class sub-category count CSV |

### Result Charts (output/results/)

| File | Path | Purpose |
|---|---|---|
| accuracy_vs_features_binary.png | `d:\Mini_Project\output\results\accuracy_vs_features_binary.png` | Accuracy vs. feature count comparison chart |
| efficiency_frontier_binary.png | `d:\Mini_Project\output\results\efficiency_frontier_binary.png` | Pareto efficiency frontier chart |

### Model Files (output/models/) — Summary

| Count | Pattern | Feature Set | Example |
|---|---|---|---|
| 6 | model_binary_baseline_79_*.joblib | 79 features | model_binary_baseline_79_Decision_Tree.joblib |
| 24 | model_binary_mrmr_{k}_*.joblib | k ∈ {4,12,23,50} | model_binary_mrmr_12_Decision_Tree.joblib |
| 24 | model_binary_pca_{k}_*.joblib | k ∈ {4,12,23,50} | model_binary_pca_12_KNN.joblib |
| 6 | model_multiclass_baseline_79_*.joblib | 79 features | model_multiclass_baseline_79_Neural_Network.joblib |
| 24 | model_multiclass_mrmr_{k}_*.joblib | k ∈ {4,12,23,50} | — |
| 24 | model_multiclass_pca_{k}_*.joblib | k ∈ {4,12,23,50} | — |
| **108 total** | — | — | All present and verified |

### Confusion Matrices (output/results/confusion_matrices/) — Key Files

| File | Experiment |
|---|---|
| binary_baseline_79_Decision_Tree_cm.png | Best binary model (99.897%) |
| binary_mrmr_12_Decision_Tree_cm.png | Best compressed binary model (99.864%) |
| binary_mrmr_12_KNN_cm.png | Second-best compressed model |
| multiclass_baseline_79_Decision_Tree_cm.png | Best multiclass baseline |
| multiclass_pca_12_KNN_cm.png | Best overall multiclass model (98.922%) |
| (+ 105 more .png files) | All 108 experiments |
