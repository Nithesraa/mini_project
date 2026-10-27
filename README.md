# Enhancing Security in Industrial IoT Networks: Machine Learning Solutions for Feature Selection and Reduction

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-brightgreen.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-ML%20Pipeline-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

An open-source experimental reproduction study and interactive web-based benchmarking suite for Industrial Internet of Things (IIoT) Network Intrusion Detection Systems (NIDS).

This project reproduces and extends the research published in IEEE Access (2024):  
> **"Enhancing Security in Industrial IoT Networks: Machine Learning Solutions for Feature Selection and Reduction"**  
> *M. T. Houkan et al., IEEE Access, 2024.*

---

## 🚀 Key Highlights

- **Dimensionality Reduction for Edge IIoT:**
  - Evaluates both **PCA** (unsupervised linear reduction) and **MRMR** (Minimum Redundancy Maximum Relevance supervised selection) against full 79-feature baselines.
  - Achieves up to **84.8% feature space reduction** with negligible impact on detection accuracy ($\le 0.03\%$ delta).
- **Comprehensive Experimental Grid (108 Models):**
  - **2 Detection Tasks:** Binary (Normal vs. Attack) & Multiclass (DoS, MITM ARP Spoofing, Mirai, Normal, Scan).
  - **9 Feature Configurations:** Baseline (79), MRMR (4, 12, 23, 50), and PCA (4, 12, 23, 50).
  - **6 Machine Learning Algorithms:** Decision Tree, K-Nearest Neighbors (KNN), Gaussian SVM, Neural Network (MLP), SVM Kernel (Random Fourier Features), and Kernel Logistic Regression.
- **Interactive Flask Dashboard & Live Demo:**
  - Real-time flow inference simulation on authentic test vectors.
  - Dynamic Decision Tree path extraction and explainability.
  - Interactive benchmark comparison table and telemetry visualizer.

---

## 📁 Repository Structure

```text
mini_project/
├── app.py                           # Flask web application entrypoint
├── config.py                        # Centralized configuration & artifact paths
├── requirements.txt                 # Python project dependencies
├── IoT_Intrusion_Detection_Reproduction.ipynb  # End-to-end ML notebook
├── basepaper/                       # IEEE reference publication
├── data_presets/                    # Authentic network flow preset vectors for demo
│   └── attack_presets.json
├── documentation_evidence/          # Detailed architectural and experimental documentation
├── routes/                          # Flask Blueprints (API & Web views)
│   ├── api_routes.py
│   └── main_routes.py
├── services/                        # Business logic & inference engine
│   ├── benchmark_service.py
│   ├── explain_service.py
│   ├── feature_catalog.py
│   ├── inference_service.py
│   └── model_service.py
├── static/                          # Frontend CSS styling and JavaScript
├── templates/                       # Jinja2 HTML dashboard templates
├── output/                          # Experimental outputs and visualizations
│   ├── checkpoints/                 # Progress and benchmark cache
│   ├── eda/                         # Exploratory data analysis charts
│   ├── feature_engineering/         # MRMR ranking CSVs and PCA variance curves
│   └── results/                     # Confusion matrices & ROC curves
└── Data/                            # Dataset directory (IoTID20 CSV)
```

---

## 🛠️ Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone Repository
```bash
git clone https://github.com/Nithesraa/mini_project.git
cd mini_project
```

### 3. Create a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Interactive Web Dashboard
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

### 6. Run the Reproduction Notebook
To explore or rerun the full data preprocessing, feature engineering, and training pipeline:
```bash
jupyter notebook IoT_Intrusion_Detection_Reproduction.ipynb
```

---

## 📊 Dataset Note
Experiments use the **IoT Network Intrusion Dataset (IoTID20)** containing 79 network traffic flow features and labeled attack categories.  
Due to GitHub's 100 MB file size limit, large raw CSV datasets and heavy binary model checkpoints (>2 GB) are excluded via `.gitignore`. You can place the dataset in `Data/IoT Network Intrusion Dataset.csv` when running full retraining.

---

## 📜 Citation
If you find this reproduction or benchmark suite useful, please reference:
```bibtex
@article{houkan2024enhancing,
  title={Enhancing Security in Industrial IoT Networks: Machine Learning Solutions for Feature Selection and Reduction},
  author={Houkan, M. T. and others},
  journal={IEEE Access},
  year={2024},
  publisher={IEEE}
}
```
