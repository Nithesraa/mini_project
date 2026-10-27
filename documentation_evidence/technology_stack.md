# Technology Stack

## Verified Technology Stack

> Evidence sources: `app.py`, `config.py`, `services/*.py`, `routes/*.py`, `templates/*.html`, `static/`, `output/models/` (joblib format), `output/feature_engineering/` (CSV files)

| Technology / Tool | Version | Purpose | Evidence Source |
|---|---|---|---|
| Python | Not verified (3.x assumed) | Primary programming language | app.py, services/ |
| Flask | Not verified | Web framework (routing, templating, blueprints) | app.py (`from flask import Flask`) |
| Jinja2 | Not verified (bundled with Flask) | HTML templating engine | templates/*.html |
| scikit-learn | 1.6.1 (stated) | ML training, inference, PCA, MRMR approximation | methodology.html explicitly states "Scikit-Learn 1.6.1" |
| joblib | Not verified | Model serialization and loading | services/model_service.py (`import joblib`) |
| NumPy | Not verified | Numerical array operations | services/inference_service.py, explain_service.py (`import numpy as np`) |
| pandas | Not verified | Feature ranking CSV loading | services/model_service.py (`import pandas as pd`) |
| Vanilla HTML/CSS/JavaScript | N/A | Frontend — no framework used | templates/, static/css/main.css, static/js/demo.js |
| Google Fonts (Inter, JetBrains Mono) | N/A | Web typography | templates/base.html |
| IoTID20 Dataset (CSV) | N/A | Input dataset | Data/IoT Network Intrusion Dataset.csv (~295 MB) |

---

## ML Algorithm Details (Verified from methodology.html and model files)

| Algorithm | MATLAB Reference | Scikit-Learn Implementation | Configuration |
|---|---|---|---|
| Decision Tree | MaxNumSplits=100, Gini index | `DecisionTreeClassifier(max_leaf_nodes=101, criterion='gini')` | max_leaf_nodes=101 (100 splits + 1 leaf) |
| KNN | k=10, Euclidean, 1/d² weights | `KNeighborsClassifier(n_neighbors=10, weights=custom)` + StandardScaler | Custom weight: w = 1/(d²+1e-10) |
| Gaussian SVM | RBF kernel, KernelScale=2.2, C=1.0 | `SVC(kernel='rbf', gamma=0.1033, C=1.0)` | gamma = 1/(2×2.2²) ≈ 0.1033 |
| Neural Network (MLP) | Single hidden layer, 25 neurons, ReLU | `MLPClassifier(hidden_layer_sizes=(25,), activation='relu', alpha=0.0)` + StandardScaler | Adam optimizer, no L2 regularization |
| SVM Kernel (Kernel Approximation) | fitckernel: RFF expansion | `OneVsOne(RBFSampler(n_components=400) + LinearSVC())` | D=400 Fourier features, OvO multi-class |
| Logistic Regression Kernel | Kernelized LR | `OneVsOne(Nystroem(n_components=100) + LogisticRegression())` | Nystroem RBF approximation, D=100 |

---

## Feature Reduction Methods

| Method | Type | Description | Configuration |
|---|---|---|---|
| Baseline | None | All 79 features used without reduction | k=79 |
| PCA | Unsupervised (linear) | Orthogonal projection onto maximum-variance axes | k ∈ {4, 12, 23, 50} |
| MRMR | Supervised (filter) | Forward greedy selection: maximize mutual info with target, minimize redundancy between selected features | k ∈ {4, 12, 23, 50} — separate rankings for binary vs. multiclass |

---

## Trained Artifact Inventory (Verified from filesystem)

| Artifact | Location | Count | Format |
|---|---|---|---|
| Trained ML models | output/models/ | 108 .joblib files | scikit-learn Pipeline/estimator |
| Preprocessed data | output/checkpoints/preprocessed_data.npz | 1 file (~57 MB) | NumPy compressed array |
| Preprocessing metadata | output/checkpoints/preprocessed_meta.pkl | 1 file (~2.4 KB) | joblib pickle |
| PCA result | output/checkpoints/pca_result.pkl | 1 file (~425 MB) | joblib pickle |
| MRMR binary rankings | output/feature_engineering/mrmr_binary_rankings.csv | 1 CSV (50 features ranked) | CSV |
| MRMR multiclass rankings | output/feature_engineering/mrmr_multiclass_rankings.csv | 1 CSV (50 features ranked) | CSV |
| Results cache | output/checkpoints/results_cache.json | 1 JSON (108 records) | JSON |
| Progress log | output/checkpoints/progress.json | 1 JSON | JSON |
| Confusion matrices | output/results/confusion_matrices/ | 110 PNG files | PNG |
| Prediction CSV files | output/results/predictions/ | 108 CSV files | CSV |
| EDA charts | output/eda/ | 8 files (PNG + CSV) | PNG, CSV |
| Feature engineering charts | output/feature_engineering/ | 4 files | PNG, CSV |
| Attack presets | data_presets/attack_presets.json | 1 JSON | JSON |

---

## Development Tools (Not verified — Commonly used)

| Tool | Purpose | Evidence |
|---|---|---|
| VS Code / PyCharm | IDE (not verified) | — |
| Jupyter Notebook | Initial EDA and training pipeline | IoT_Intrusion_Detection_Reproduction.ipynb present (454 KB) |
| Git | Version control (not verified) | No .git directory found during inspection |

---

## Deployment (Verified)

| Parameter | Value | Evidence |
|---|---|---|
| Server | Flask development server | app.py: `app.run(host="127.0.0.1", port=5000, debug=True)` |
| Host | 127.0.0.1 (localhost only) | app.py |
| Port | 5000 | app.py |
| Production WSGI | Not configured | config.py: DEBUG=False only, no Gunicorn/uWSGI config |
| Containerization | Not configured | No Dockerfile, requirements.txt, or docker-compose found |
| Cloud deployment | Not configured | No deployment config found |

---

## Environment Variables

| Variable | Purpose | Evidence |
|---|---|---|
| `SECRET_KEY` | Flask session secret | config.py: `os.environ.get("SECRET_KEY", "iiot-nids-secret-key-2024")` |

> **Security Note:** A default fallback value is hardcoded in config.py. For any non-local deployment, this must be overridden via the environment variable.

---

## Missing Information for Technology Stack

| Item | Why Needed | How to Obtain |
|---|---|---|
| Exact Python version | Precise reproducibility | `python --version` in environment |
| Exact package versions | Requirements documentation | `pip freeze > requirements.txt` |
| No requirements.txt found | Cannot verify exact library versions | Run `pip freeze` in project env |
| Jupyter notebook version | For notebook documentation | `jupyter --version` |
