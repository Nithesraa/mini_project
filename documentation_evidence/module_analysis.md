# Module-by-Module Analysis

## Module 1: app.py — Application Factory

| Property | Detail |
|---|---|
| File | `app.py` (27 lines) |
| Pattern | Flask Application Factory pattern |
| Objective | Create and configure the Flask application instance |
| Inputs | None (reads config.py constants and environment variables) |
| Outputs | Configured Flask app object with both blueprints registered |

### Responsibilities
- Creates Flask instance with template and static folder paths
- Sets SECRET_KEY, DEBUG, and MAX_CONTENT_LENGTH from config
- Registers `main_bp` and `api_bp` blueprints
- Runs dev server on 127.0.0.1:5000 when executed directly

### Security Considerations
- SECRET_KEY loaded from environment variable with fallback (config.py)
- DEBUG=False in config (overridden to True in `app.run()` call — for dev only)
- 16 MB upload limit enforced

---

## Module 2: config.py — Path and Configuration Constants

| Property | Detail |
|---|---|
| File | `config.py` (29 lines) |
| Objective | Centralize all filesystem paths and server configuration |
| Pattern | Module-level constants (no class) |

### Path Definitions (Verified)
- `BASE_DIR` → project root
- `OUTPUT_DIR` → `output/`
- `CHECKPOINTS_DIR` → `output/checkpoints/`
- `MODELS_DIR` → `output/models/`
- `RESULTS_DIR` → `output/results/`
- `CM_DIR` → `output/results/confusion_matrices/`
- `ROC_DIR` → `output/results/roc_curves/`
- `FE_DIR` → `output/feature_engineering/`
- `EDA_DIR` → `output/eda/`
- `PREPROCESSED_DATA_PATH` → `output/checkpoints/preprocessed_data.npz`
- `PREPROCESSED_META_PATH` → `output/checkpoints/preprocessed_meta.pkl`
- `PCA_RESULT_PATH` → `output/checkpoints/pca_result.pkl`
- `MRMR_BINARY_RANKINGS_PATH` → `output/feature_engineering/mrmr_binary_rankings.csv`
- `MRMR_MULTI_RANKINGS_PATH` → `output/feature_engineering/mrmr_multiclass_rankings.csv`
- `RESULTS_CACHE_PATH` → `output/checkpoints/results_cache.json`
- `PRESETS_FILE_PATH` → `data_presets/attack_presets.json`

---

## Module 3: routes/main_routes.py — Page Routes Blueprint

| Property | Detail |
|---|---|
| File | `routes/main_routes.py` (74 lines) |
| Blueprint name | `main_bp` (no URL prefix) |
| Objective | Serve all HTML pages and static pre-rendered image assets |

### Routes (All GET, No Authentication)
| Route | Handler | Template | Notes |
|---|---|---|---|
| `GET /` | `index()` | `index.html` | Calls `benchmark_service.get_summary_kpis()` |
| `GET /demo` | `demo()` | `demo.html` | No server-side data |
| `GET /benchmarks` | `benchmarks()` | `benchmarks.html` | Calls `benchmark_service.get_all_results()` and `get_summary_kpis()` |
| `GET /features` | `features()` | `features.html` | Loads MRMR rankings + PCA artifact |
| `GET /methodology` | `methodology()` | `methodology.html` | Static content |
| `GET /assets/cm/<filename>` | `serve_cm()` | — | Serves confusion matrix PNGs from CM_DIR |
| `GET /assets/results/<filename>` | `serve_result_img()` | — | Serves result chart images from RESULTS_DIR |
| `GET /assets/eda/<filename>` | `serve_eda_img()` | — | Serves EDA images from EDA_DIR |
| `GET /assets/fe/<filename>` | `serve_fe_img()` | — | Serves feature engineering images from FE_DIR |

### PCA Component Data Processing (features route)
For PCA display, the route extracts `explained_variance_ratio_` and `cumulative_variance` from the loaded `pca_result.pkl` artifact and constructs a component list with percentage values for Jinja2 templating.

---

## Module 4: routes/api_routes.py — REST API Blueprint

| Property | Detail |
|---|---|
| File | `routes/api_routes.py` (111 lines) |
| Blueprint name | `api_bp` (url_prefix=`/api`) |
| Objective | Provide JSON REST API for live inference, preset loading, and metric filtering |
| Authentication | None (read-only endpoints) |

### Endpoint Details

#### GET /api/presets
- Reads `data_presets/attack_presets.json`
- Returns: `{status, presets: [{id, name, expected_binary, expected_multiclass, badge_color, description, raw_features, normalized_features}]}`
- **Note:** Heavy `normalized_vector` is NOT returned here (only for `/api/predict` consumption)

#### POST /api/predict
- Request JSON: `{preset_id, task, method, n_features, model_name}`
- Input validation:
  - task must be in ["binary", "multiclass"]
  - method must be in ["baseline", "mrmr", "pca"]
  - n_features: if baseline → forced to 79; if mrmr/pca → must be in {4, 12, 23, 50} or defaults to 12
- Loads `normalized_vector` (79-dim) from preset
- Calls `inference_service.run_inference()`
- Appends `ground_truth` comparison (preset expected label vs. model output label)
- Returns comprehensive inference + explanation payload

#### GET /api/metrics
- Query params: `task`, `method`, `model_name`, `n_features`
- Delegates to `benchmark_service.filter_results()`
- Returns: `{status, count, results: [...]}`

### Input Validation (Verified from code)
- Invalid `task` → 400 error with message
- Invalid `method` → 400 error with message
- Missing preset → 500 error
- Model load failure → 500 error (FileNotFoundError wrapped in try/except)

---

## Module 5: services/model_service.py — Model Loading and Cache

| Property | Detail |
|---|---|
| File | `services/model_service.py` (92 lines) |
| Pattern | Singleton (`model_service = ModelService()`) |
| Objective | Load, cache, and serve trained ML model files with LRU eviction |

### Key Methods
| Method | Description |
|---|---|
| `__init__(max_cached_models=5)` | Initializes LRU cache (OrderedDict), calls `_load_metadata()` |
| `_load_metadata()` | Loads `preprocessed_meta.pkl`, binary/multiclass MRMR CSVs at startup |
| `get_feature_cols()` | Returns 79-element feature name list from preprocessed_meta.pkl |
| `get_binary_classes()` | Returns `['Anomaly', 'Normal']` from LabelEncoder |
| `get_multiclass_classes()` | Returns `['DoS', 'MITM ARP Spoofing', 'Mirai', 'Normal', 'Scan']` |
| `get_mrmr_rankings(task)` | Returns ranked feature list for given task |
| `get_pca_artifact()` | Lazy-loads pca_result.pkl (cached after first load) |
| `get_model(experiment_id)` | LRU load from disk: `model_{exp_id}.joblib` |

### LRU Cache Logic (Verified)
- Cache capacity: max 5 models simultaneously
- When cache full: `popitem(last=False)` evicts least-recently-used entry (OrderedDict behavior)
- Cache hit: `move_to_end(experiment_id)` promotes to most-recently-used

### Experiment ID Format (Verified)
`{task}_{method}_{n_features}_{model_name_with_underscores}`

Example: `binary_mrmr_12_Decision_Tree` → file: `model_binary_mrmr_12_Decision_Tree.joblib`

---

## Module 6: services/benchmark_service.py — Results Cache Reader

| Property | Detail |
|---|---|
| File | `services/benchmark_service.py` (61 lines) |
| Pattern | Singleton (`benchmark_service = BenchmarkService()`) |
| Objective | Read and serve pre-computed benchmark results from JSON cache |
| Input | `output/checkpoints/results_cache.json` (108 result records) |

### Key Methods
| Method | Description |
|---|---|
| `_load_cache()` | Reads results_cache.json into `self.results` list at init |
| `get_all_results()` | Returns full list (108 records) |
| `filter_results(task, method, model_name, n_features)` | Filters results by any combination of parameters |
| `get_summary_kpis()` | Computes peak binary accuracy, max throughput, min FAR, total models |
| `get_confusion_matrix_filename(exp_id)` | Resolves CM filename from two candidate naming patterns |

### KPI Computation (Verified from code + data)
- `peak_binary_accuracy`: max accuracy across all binary results → **99.8972%** (binary_baseline_79_Decision_Tree)
- `max_throughput_obs_sec`: max throughput across all results → **~8,513,912 obs/sec** (Decision Tree baseline, from runtime analysis)
- `lowest_false_alarm_rate`: min FAR across binary results → **0.0074%** (binary_baseline_79_Decision_Tree)
- `max_feature_reduction`: hardcoded string "84.8%" (79→12 features = 84.81% reduction)

---

## Module 7: services/inference_service.py — Inference Orchestrator

| Property | Detail |
|---|---|
| File | `services/inference_service.py` (108 lines) |
| Pattern | Singleton |
| Objective | Execute end-to-end prediction on a 79-dimensional input vector |

### Processing Steps (Verified from code, lines 17–105)
1. **Experiment ID formatting:** `f"{task}_{method}_{n_features}_{model_name.replace(' ', '_')}"`
2. **Model loading:** `model_service.get_model(exp_id)` (LRU cached)
3. **Feature extraction:** Choose reduction path:
   - `baseline`: `X_sub = vector_79` (all 79 features)
   - `mrmr`: `rankings[:n_features]` → column index slice of vector_79
   - `pca`: `full_pca.transform(vector_79)[:, :n_features]`
4. **Prediction:** `model.predict(X_sub)[0]` with `time.perf_counter()` latency measurement
5. **Probability extraction:** `model.predict_proba(X_sub)` if supported; else `{pred_label: 1.0}`
6. **Explanation:** Delegates to `explain_service.explain_prediction()`
7. **Returns** structured JSON with telemetry, configuration, prediction, reduction_summary, explanations

### Output Fields (All verified from code)
- `status`: "success"
- `telemetry.latency_ms`: wall-clock latency of `model.predict()` call in milliseconds
- `telemetry.timestamp`: ISO 8601 UTC timestamp
- `configuration`: {task, method, n_features, model_name, experiment_id}
- `prediction`: {predicted_class_index, predicted_label, confidence_score, class_probabilities}
- `reduction_summary`: {method, original_features: 79, active_features: k, compression_pct}
- `decision_tree_explanation`, `neural_network_explanation`, `pca_telemetry`, `feature_table`

---

## Module 8: services/explain_service.py — Explainability Engine

| Property | Detail |
|---|---|
| File | `services/explain_service.py` (212 lines) |
| Objective | Generate model-specific and configuration-specific explanations |

### Explanation Components (Verified from code)

#### Decision Tree Path (lines 34–92)
- **Applicable when:** `hasattr(model, 'tree_')` — i.e., scikit-learn DecisionTreeClassifier
- **Method:** `model.apply(X_sub)` → leaf node; `model.decision_path(X_sub).indices` → node sequence
- **Per step:** feature name, threshold, sample value, raw value, branch taken (Left/Right)
- **Leaf info:** leaf_node_id, leaf_samples, leaf_purity_pct, class_counts per leaf

#### Neural Network Disclaimer (lines 95–108)
- **Applicable when:** "Neural Network" or "MLP" in model_name
- Returns fixed architectural disclaimer about non-local attribution

#### PCA Telemetry (lines 111–146)
- **Applicable when:** method == "pca"
- Per component: coordinate value (z), explained_variance_pct, cumulative_variance_pct, top 3 original feature loadings (by absolute loading magnitude from `full_pca.components_`)

#### Feature Table (lines 149–202)
- For mrmr/baseline: actual feature names, raw values, normalized values, MRMR rank or "Baseline", Gini importance if Decision Tree
- For pca: PC1..PCk with coordinate values, explained variance, top loadings

---

## Module 9: services/feature_catalog.py — Feature Metadata

| Property | Detail |
|---|---|
| File | `services/feature_catalog.py` (468 lines) |
| Objective | Authoritative definitions for all 79 network flow features |
| Structure | `FEATURE_CATEGORIES` dict (9 categories) + `FEATURE_DEFINITIONS` dict (79 entries) |

### Feature Categories (9 groups, all verified)
1. Endpoint & Protocol (3 features): Src_Port, Dst_Port, Protocol
2. Flow Duration & Rates (5 features): Flow_Duration, Flow_Byts/s, Flow_Pkts/s, Fwd_Pkts/s, Bwd_Pkts/s
3. Packet Counts & Volumetric Byte Aggregates (4 features)
4. Directional Packet Length Statistics (17 features)
5. Inter-Arrival Time (IAT) Statistics (14 features)
6. TCP Flags & Control Signaling (12 features)
7. Header & Window State Indicators (5 features)
8. Bulk Transfer & Subflow Aggregates (11 features)
9. Active & Idle Timing States (8 features)

**Total: 79 features — matches preprocessed_meta.pkl** (confirmed via comment in catalog header)

---

## Module 10: data_presets/attack_presets.json — Attack Preset Library

| Property | Detail |
|---|---|
| File | `data_presets/attack_presets.json` (35,594 bytes) |
| Objective | Provides authentic held-out test-set network flow vectors for live demo |
| Structure | JSON array of preset objects |

### Known Presets (from demo.html)
| ID | Name | Binary Label | Multiclass Label |
|---|---|---|---|
| `mirai_udp` | Mirai UDP Flooding | Anomaly | Mirai |
| `dos_syn` | DoS SYN Flooding | Anomaly | DoS |
| `benign_normal` | Benign Industrial Normal | Normal | Normal |
| `port_scan` | Port & OS Scanning | Anomaly | Scan |
| `mitm_arp` | MITM ARP Spoofing | Anomaly | MITM ARP Spoofing |

### Preset Object Structure (from api_routes.py)
- `id`: string identifier
- `name`: display name
- `expected_binary`: ground truth binary label
- `expected_multiclass`: ground truth multiclass label
- `badge_color`: UI display tag
- `description`: human-readable description
- `sub_category`: fine-grained attack sub-type
- `raw_features`: dict of feature_name → raw network measurement value
- `normalized_features`: dict of feature_name → MinMax normalized value
- `normalized_vector`: list of 79 float values (MinMax scaled, in feature order)

---

## Module 11: static/js/demo.js — Live Demo Frontend

| Property | Detail |
|---|---|
| File | `static/js/demo.js` (12,128 bytes) |
| Objective | Handle all user interactions on the demo page |

### Responsibilities (Inferred from demo.html analysis)
- Fetch `/api/presets` on page load to confirm available presets
- Listen for preset button clicks, task/method/n_features/model selector changes
- On "Execute Intrusion Analysis" click: POST to `/api/predict` with current configuration
- Render threat banner (ANOMALY/NORMAL) with color coding
- Render ground truth match badge
- Render class probability bar chart
- Render Decision Tree path steps (when DT selected)
- Render PCA component table (when PCA selected)
- Render feature table
- Toggle panel visibility (DT panel ↔ MLP panel based on model; PCA panel based on method)

---

## Module 12: IoT_Intrusion_Detection_Reproduction.ipynb — Training Pipeline

| Property | Detail |
|---|---|
| File | `IoT_Intrusion_Detection_Reproduction.ipynb` (~454 KB) |
| Objective | Complete offline training pipeline for all 108 experiments |
| Status | EXECUTED — all 108 model artifacts confirmed present in output/ |

### Implemented Stages (Inferred from artifacts)
1. Data ingestion from `Data/IoT Network Intrusion Dataset.csv`
2. EDA: class distribution charts, correlation heatmap, dataset_info.txt
3. Preprocessing: column dropping, infinite value replacement, MinMax scaling, label encoding
4. Checkpoint saving: `preprocessed_data.npz`, `preprocessed_meta.pkl`
5. MRMR computation: binary and multiclass rankings → CSV files
6. PCA fitting: all 79 components → `pca_result.pkl`, variance charts
7. Nested loop: for task × feature_config × classifier → train, evaluate, save model, save CM, save preds
8. Results aggregation to `results_cache.json`
9. Summary charts: `accuracy_vs_features_binary.png`, `efficiency_frontier_binary.png`
