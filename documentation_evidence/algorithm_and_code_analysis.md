# Algorithm and Code Analysis

## 1. MRMR — Minimum Redundancy Maximum Relevance Feature Selection

### Purpose
Rank 79 network flow features in descending order of discriminative utility for intrusion detection, while suppressing features that are highly correlated with already-selected features. Computed separately for binary and multiclass targets.

### Mathematical Formulation (from features.html — verified)
```
max [ I(x_j ; y) - (1 / |S|) × Σ I(x_j ; x_i) ]
   where S is the set of already selected features
```
- `I(x_j ; y)` = mutual information between candidate feature x_j and the target y (Relevance)
- `(1/|S|) × Σ I(x_j ; x_i)` = mean mutual information between x_j and each already-selected feature (Redundancy)
- Greedy forward selection: iteratively add the feature maximizing (Relevance − Redundancy)

### Input
- 79-feature normalized training data matrix (438,048 × 79)
- Binary label vector (for binary MRMR) or 5-class label vector (for multiclass MRMR)

### Output
- Ranked list of 50 features (up to rank 50 preserved in CSV; full 79 computed)
- Evidence: `output/feature_engineering/mrmr_binary_rankings.csv`, `mrmr_multiclass_rankings.csv`

### Top 12 Binary MRMR Features (Verified from CSV)
| Rank | Feature | Domain Category |
|---|---|---|
| 1 | Dst_Port | Endpoint & Protocol |
| 2 | Init_Bwd_Win_Byts | Header & Window State |
| 3 | Fwd_Pkt_Len_Std | Directional Packet Length |
| 4 | ACK_Flag_Cnt | TCP Flags |
| 5 | Src_Port | Endpoint & Protocol |
| 6 | Fwd_Header_Len | Header & Window State |
| 7 | Pkt_Len_Std | Directional Packet Length |
| 8 | Bwd_Header_Len | Header & Window State |
| 9 | Protocol | Endpoint & Protocol |
| 10 | TotLen_Fwd_Pkts | Packet Counts & Bytes |
| 11 | Pkt_Len_Var | Directional Packet Length |
| 12 | Subflow_Fwd_Byts | Bulk Transfer |

### Top 12 Multiclass MRMR Features (Verified from CSV)
| Rank | Feature | Domain Category |
|---|---|---|
| 1 | SYN_Flag_Cnt | TCP Flags |
| 2 | Fwd_IAT_Tot | IAT Statistics |
| 3 | Protocol | Endpoint & Protocol |
| 4 | Flow_IAT_Min | IAT Statistics |
| 5 | Fwd_Pkt_Len_Std | Directional Packet Length |
| 6 | Flow_IAT_Mean | IAT Statistics |
| 7 | Dst_Port | Endpoint & Protocol |
| 8 | ACK_Flag_Cnt | TCP Flags |
| 9 | Idle_Min | Active & Idle Timing |
| 10 | Idle_Mean | Active & Idle Timing |
| 11 | Bwd_IAT_Mean | IAT Statistics |
| 12 | Init_Bwd_Win_Byts | Header & Window State |

### Implementation File
Computed in the Jupyter notebook (not visible in Flask services). Rankings loaded via `model_service._load_metadata()` from CSV.

---

## 2. PCA — Principal Component Analysis

### Purpose
Unsupervised linear dimensionality reduction. Projects 79 normalized features onto orthogonal axes of maximum variance. Evaluated at k ∈ {4, 12, 23, 50} components.

### Mathematical Definition
Given training data matrix X (n × 79), PCA finds:
1. Center: X̄ = mean(X, axis=0)
2. Covariance: Σ = X^T X / (n-1)
3. Eigenvectors W (loading matrix, 79×79) and eigenvalues λ
4. Transform: Z = (X - X̄) W

At inference: z_sample = (x_sample - X̄) W → select first k components.

### Verified PCA Explained Variance (from features.html)
| k | Computed Cumulative Variance | Paper Target | Delta |
|---|---|---|---|
| 4 | 88.77% | 88.74% | +0.03% |
| 12 | 99.16% | 99.12% | +0.04% |
| 23 | 99.91% | 99.90% | +0.01% |
| 50 | 100.00% | 99.99% | +0.01% |

**All four checkpoints verified against Houkan et al. 2024 paper targets** (within rounding tolerance).

### Implementation in Inference
File: `services/inference_service.py`, lines 33–37:
```python
elif method == "pca":
    pca_artifact = model_service.get_pca_artifact()
    full_pca = pca_artifact["full_pca"]
    X_sub = full_pca.transform(vector_79)[:, :n_features]
```

---

## 3. MATLAB-to-Scikit-Learn Algorithm Translation

### Decision Tree (Verified from methodology.html)
| Aspect | MATLAB | scikit-learn |
|---|---|---|
| Parameter | MaxNumSplits=100 | max_leaf_nodes=101 |
| Rationale | N splits → N+1 leaves | Exact mathematical equivalence |
| Split criterion | Gini index | criterion='gini' |

Key excerpt concept: `DecisionTreeClassifier(max_leaf_nodes=101, criterion='gini')`

### KNN (Verified)
| Aspect | MATLAB | scikit-learn |
|---|---|---|
| Neighbors | k=10 | n_neighbors=10 |
| Distance metric | Euclidean | metric='euclidean' (default) |
| Weighting | 1/d² | Custom function: w = 1/(d² + 1e-10) |
| Scaling | StandardScaler applied | Wrapped in Pipeline |

### Gaussian SVM (Verified)
| Aspect | MATLAB | scikit-learn |
|---|---|---|
| Kernel | RBF | kernel='rbf' |
| KernelScale | 2.2 | gamma = 1/(2 × 2.2²) ≈ 0.1033 |
| Cost | C=1.0 | C=1.0 |
| Multi-class | OvO | SVC uses OvO by default |

### Neural Network (Verified)
| Aspect | MATLAB | scikit-learn |
|---|---|---|
| Topology | 1 hidden layer, 25 neurons | hidden_layer_sizes=(25,) |
| Activation | ReLU | activation='relu' |
| Regularization | L2=0 | alpha=0.0 |
| Optimizer | Adam | solver='adam' (default) |
| Scaling | StandardScaler | Wrapped in Pipeline |

### SVM Kernel (Verified)
| Aspect | MATLAB | scikit-learn |
|---|---|---|
| Method | fitckernel (RFF expansion) | RBFSampler(n_components=400) + LinearSVC() |
| Components D | 400 Fourier features | n_components=400 |
| Multi-class | OvO | OneVsOneClassifier wrapper |

### Logistic Regression Kernel (Verified)
| Aspect | MATLAB | scikit-learn |
|---|---|---|
| Method | Kernelized LR | Nystroem(n_components=100) + LogisticRegression() |
| Kernel approx | — | Nystroem RBF (Rahimi & Recht) |
| Multi-class | OvO | OneVsOneClassifier wrapper |

---

## 4. Decision Tree Path Traversal (Explainability Algorithm)

### Purpose
Produce a step-by-step human-readable explanation of why the Decision Tree reached its prediction, for any input network flow.

### Algorithm (Verified from explain_service.py, lines 34–92)
```
Input: fitted DecisionTreeClassifier model, k-dimensional input X_sub

1. leaf_node_id = model.apply(X_sub)[0]          # Identify reached leaf
2. path_nodes = model.decision_path(X_sub).indices  # All nodes traversed

For each node in path_nodes (except leaf):
    feat_idx = tree.feature[node]
    threshold = tree.threshold[node]
    sample_val = X_sub[0, feat_idx]
    if sample_val <= threshold:
        branch = "Left" (condition True)
    else:
        branch = "Right" (condition False)
    Record: feature name, threshold, sample value, raw value, branch

At leaf node:
    val_dist = tree.value[reached_leaf][0]
    prob_dist = val_dist / sum(val_dist)
    purity_pct = max(prob_dist) × 100
    leaf_pred_class = argmax(prob_dist)
    Reconstruct class counts from weighted_n_node_samples × prob_dist

Output: path_steps (list of dicts), leaf info
```

### Key Properties
- Uses `model.decision_path()` — scikit-learn 1.6.1 documented API
- No hardcoded values — all thresholds and feature indices are runtime-introspected
- Adapts to both original feature names (mrmr/baseline) and PC labels (pca)
- For PCA models: feature labels become "PC1", "PC2", etc.

---

## 5. LRU Model Cache Algorithm

### Purpose
Avoid redundant disk I/O when multiple inference requests use the same model configuration.

### Algorithm (Verified from model_service.py, lines 67–88)
```python
def get_model(experiment_id):
    if experiment_id in cache:
        cache.move_to_end(experiment_id)   # Promote to MRU
        return cache[experiment_id]

    # Cache miss: load from disk
    model = joblib.load(f"output/models/model_{experiment_id}.joblib")

    if len(cache) >= max_cached:
        cache.popitem(last=False)          # Evict LRU entry

    cache[experiment_id] = model
    return model
```

- Data structure: `collections.OrderedDict` (insertion order preserved)
- Eviction: LRU (popitem(last=False))
- Capacity: 5 models (configurable at init)

---

## 6. Feature Vector Reduction Algorithms

### MRMR Slice (Verified from inference_service.py, lines 28–31)
```python
rankings = model_service.get_mrmr_rankings(task)
selected_features = rankings[:n_features]
col_indices = [feature_cols.index(f) for f in selected_features]
X_sub = vector_79[:, col_indices]
```
- Time complexity: O(n_features) index lookup + O(k) column slice

### PCA Transform (Verified from inference_service.py, lines 33–37)
```python
full_pca = pca_artifact["full_pca"]
X_sub = full_pca.transform(vector_79)[:, :n_features]
```
- Projects 1×79 vector to 1×79 PC space, then slices first k components
- Time complexity: O(79 × 79) matrix multiplication (negligible for single sample)

---

## 7. Representative Source Code Excerpts

### 7.1 Inference Pipeline Entry Point (inference_service.py, lines 17–44)
```python
exp_id = f"{task}_{method}_{n_features}_{model_name.replace(' ', '_')}"
model = model_service.get_model(exp_id)
feature_cols = model_service.get_feature_cols()

if method == "baseline":
    X_sub = vector_79.copy()
elif method == "mrmr":
    rankings = model_service.get_mrmr_rankings(task)
    selected_features = rankings[:n_features]
    col_indices = [feature_cols.index(f) for f in selected_features]
    X_sub = vector_79[:, col_indices]
elif method == "pca":
    pca_artifact = model_service.get_pca_artifact()
    full_pca = pca_artifact["full_pca"]
    X_sub = full_pca.transform(vector_79)[:, :n_features]

t0 = time.perf_counter()
pred_raw = model.predict(X_sub)[0]
latency_ms = (time.perf_counter() - t0) * 1000.0
```

### 7.2 MRMR Objective (features.html — displayed formula)
```
max [ I(x_j ; y) - (1 / |S|) Σ I(x_j ; x_i) ]
```

### 7.3 Gaussian SVM Gamma Derivation (methodology.html)
```
gamma = 1 / (2 × KernelScale²) = 1 / (2 × 2.2²) ≈ 0.1033
```

### 7.4 KNN Custom Weight Function (methodology.html)
```python
def w_custom(distances):
    return 1.0 / (distances ** 2 + 1e-10)  # Inverse squared distance
```
