# Database and API Analysis

## 1. Database

This project does NOT use a relational database (no SQL, SQLite, PostgreSQL, MongoDB, or similar). All persistent data is stored as flat files on disk.

### Flat File Data Store Summary

| File / Artifact | Format | Purpose | Location |
|---|---|---|---|
| `results_cache.json` | JSON array (108 objects) | Pre-computed benchmark metrics for all experiments | `output/checkpoints/` |
| `attack_presets.json` | JSON array | Authentic test-set flow vectors for live demo (5+ presets) | `data_presets/` |
| `preprocessed_data.npz` | NumPy NPZ | Compressed training and test feature arrays + labels | `output/checkpoints/` |
| `preprocessed_meta.pkl` | Pickle (joblib) | Feature names, LabelEncoder objects for binary + multiclass | `output/checkpoints/` |
| `pca_result.pkl` | Pickle (joblib) | Fitted PCA object (all 79 components) + cumulative variance | `output/checkpoints/` |
| `mrmr_binary_rankings.csv` | CSV (2 columns: rank, feature) | MRMR feature importance order for binary task | `output/feature_engineering/` |
| `mrmr_multiclass_rankings.csv` | CSV (2 columns: rank, feature) | MRMR feature importance order for multiclass task | `output/feature_engineering/` |
| `model_*.joblib` (×108) | Pickle (joblib) | Serialized trained scikit-learn model pipeline objects | `output/models/` |
| `preds_*.csv` (×108) | CSV (2 columns: y_true, y_pred) | Test-set predictions per experiment | `output/results/predictions/` |
| `*_cm.png` (×110) | PNG | Confusion matrix visualizations | `output/results/confusion_matrices/` |
| `class_distribution_*.csv` | CSV | Class count summaries | `output/eda/` |
| `dataset_info.txt` | Plain text | EDA summary of dataset shape, dtypes, distributions | `output/eda/` |
| `pca_explained_variance.csv` | CSV | Per-component explained variance fraction | `output/feature_engineering/` |
| `progress.json` | JSON | Training progress tracker (completed experiment IDs) | `output/checkpoints/` |

---

## 2. Results Cache Schema (Verified from results_cache.json)

The results cache is a JSON array of 108 objects. Each object has the following fields:

| Field | Type | Description | Example Value |
|---|---|---|---|
| `task` | string | Classification task type | "binary" or "multiclass" |
| `method` | string | Feature reduction method | "baseline", "mrmr", "pca" |
| `n_features` | integer | Number of features/components used | 4, 12, 23, 50, 79 |
| `model_name` | string | Algorithm name | "Decision Tree" |
| `experiment_id` | string | Unique experiment identifier | "binary_mrmr_12_Decision_Tree" |
| `accuracy` | float | Classification accuracy on test set | 0.998636 |
| `precision` | float | Macro-averaged precision | 0.9966 |
| `recall` | float | Macro-averaged recall | 0.9898 |
| `f1_score` | float | Macro-averaged F1 | 0.9893 |
| `far` | float | False Alarm Rate (FP / (FP + TN)) | 0.000074 |
| `auc` | float | Area Under ROC Curve | 0.9975 |
| `train_time_sec` | float | Wall-clock training time in seconds | 1.04 |
| `pred_speed_obs_per_sec` | float | Inference throughput on test set | 8249703.0 |
| `model_size_kb` | float | Serialized model file size in KB | 16.79 |

**Total: 108 records — Verified: all 108 experiments confirmed in `progress.json`**

---

## 3. Attack Presets Schema (Verified from api_routes.py)

Each preset object in `attack_presets.json` contains:

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique preset identifier |
| `name` | string | Display name |
| `expected_binary` | string | Ground truth binary label |
| `expected_multiclass` | string | Ground truth multiclass label |
| `badge_color` | string | UI badge color class |
| `description` | string | Human-readable description |
| `sub_category` | string | Fine-grained sub-type |
| `raw_features` | object | Dict: feature_name → raw network measurement |
| `normalized_features` | object | Dict: feature_name → MinMax [0,1] value |
| `normalized_vector` | array[float] | 79-element array in canonical feature order |

---

## 4. API Endpoint Inventory

### Complete Endpoint Table

| Method | Endpoint | Purpose | Auth | Request | Response | Implementation |
|---|---|---|---|---|---|---|
| GET | `/` | Dashboard page | None | — | HTML | `main_routes.py::index()` |
| GET | `/demo` | Live inference demo page | None | — | HTML | `main_routes.py::demo()` |
| GET | `/benchmarks` | 108-experiment results table | None | — | HTML | `main_routes.py::benchmarks()` |
| GET | `/features` | Feature reduction analysis page | None | — | HTML | `main_routes.py::features()` |
| GET | `/methodology` | Methodology & MATLAB-sklearn mapping | None | — | HTML | `main_routes.py::methodology()` |
| GET | `/assets/cm/<filename>` | Serve confusion matrix PNG | None | filename | image/png | `main_routes.py::serve_cm()` |
| GET | `/assets/results/<filename>` | Serve result chart PNG | None | filename | image/png | `main_routes.py::serve_result_img()` |
| GET | `/assets/eda/<filename>` | Serve EDA image | None | filename | image/png | `main_routes.py::serve_eda_img()` |
| GET | `/assets/fe/<filename>` | Serve feature engineering image | None | filename | image/png | `main_routes.py::serve_fe_img()` |
| GET | `/api/presets` | Return attack preset metadata list | None | — | JSON | `api_routes.py::get_presets()` |
| POST | `/api/predict` | Execute live inference + explainability | None | JSON body | JSON | `api_routes.py::predict()` |
| GET | `/api/metrics` | Filter benchmark results | None | Query params | JSON | `api_routes.py::get_metrics()` |

---

## 5. /api/predict — Detailed Request/Response Specification

### Request Body (JSON)
```json
{
  "preset_id": "mirai_udp",
  "task": "binary",
  "method": "mrmr",
  "n_features": 12,
  "model_name": "Decision Tree"
}
```

### Validation Rules
- `task`: must be "binary" or "multiclass" — else 400
- `method`: must be "baseline", "mrmr", or "pca" — else 400
- `n_features`: if baseline → forced to 79; if mrmr/pca → must be in {4,12,23,50} or defaults to 12
- If preset not found → 500 error

### Response Body (JSON, success case)
```json
{
  "status": "success",
  "telemetry": {
    "latency_ms": 0.38,
    "timestamp": "2024-01-01T00:00:00Z"
  },
  "configuration": {
    "task": "binary",
    "method": "mrmr",
    "n_features": 12,
    "model_name": "Decision Tree",
    "experiment_id": "binary_mrmr_12_Decision_Tree"
  },
  "prediction": {
    "predicted_class_index": 0,
    "predicted_label": "Anomaly",
    "confidence_score": 0.9998,
    "class_probabilities": {"Anomaly": 0.9998, "Normal": 0.0002}
  },
  "reduction_summary": {
    "method": "mrmr",
    "original_features": 79,
    "active_features": 12,
    "compression_pct": 84.81
  },
  "decision_tree_explanation": {
    "is_applicable": true,
    "traversed_node_count": 8,
    "leaf_node_id": 45,
    "leaf_samples": 1234,
    "leaf_purity_pct": 99.97,
    "predicted_class_name": "Anomaly",
    "class_counts": {"Anomaly": 1234, "Normal": 1},
    "path_steps": [...]
  },
  "neural_network_explanation": {"is_applicable": false, "disclaimer": null},
  "pca_telemetry": {"is_applicable": false, "components": []},
  "feature_table": [...],
  "ground_truth": {
    "preset_id": "mirai_udp",
    "preset_name": "Mirai UDP Flooding",
    "sub_category": "Mirai-UDP Flooding",
    "ground_truth_label": "Anomaly",
    "is_correct": true
  }
}
```

---

## 6. CRUD Analysis

This project is **read-only** (no database writes from the web application):

| Operation | Implementation |
|---|---|
| **Create** | Models and results created offline by training notebook; never via web API |
| **Read** | All API endpoints and routes read from pre-existing disk artifacts |
| **Update** | Not implemented |
| **Delete** | Not implemented |

The only write operation in the web layer would be Flask session state (no sessions used in practice since no auth).
