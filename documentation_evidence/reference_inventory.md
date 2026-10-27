# Reference Inventory

## 1. References Found in Workspace

### REF-01 — Base Reference Paper (Primary, Verified)

| Field | Value |
|---|---|
| Authors | Houkan et al. |
| Full Title | "Enhancing Security in Industrial IoT Networks: Machine Learning Solutions for Feature Selection and Reduction" |
| Journal | IEEE Access |
| Year | 2024 |
| File | `d:\Mini_Project\basepaper\Enhancing_Security_in_Industrial_IoT_Networks_Machine_Learning_Solutions_for_Feature_Selection_and_Reduction.pdf` (7.3 MB) |
| DOI | Not extracted (file not readable as text — binary PDF) |
| Status | **VERIFIED PRESENT in workspace** |
| Role in Project | This is the paper being reproduced. Every experiment, hyperparameter, and evaluation metric is based on this paper. |
| Mentioned in Code | `base.html` footer: "Base Reference: Houkan et al., 'Enhancing Security in Industrial IoT Networks...', IEEE Access, 2024" |
| Also mentioned | `index.html`: "This project replicates the experimental methodology of Houkan et al. (IEEE Access, 2024)" |

**Relevant Report Sections:** Abstract, Introduction (motivation), Literature Survey (primary reference), Methodology (MATLAB configuration mapping), Results (comparison with paper figures)

---

## 2. References Cited in Source Code / Templates (Not as separate files)

### REF-02 — IoTID20 Dataset

| Field | Value |
|---|---|
| Authors | Ullah & Mahmoud |
| Description | IoT Network Intrusion Dataset 2020 (IoTID20) |
| Reference Location | `index.html`: "Dataset: IoTID20 (Ullah & Mahmoud)" |
| Data file | `Data/IoT Network Intrusion Dataset.csv` (295 MB, 625,783 rows) |
| DOI / URL | Not provided in workspace |
| Status | Dataset is present and was used for training. Full citation details NOT in workspace |
| Suggested Citation | Ullah, I., & Mahmoud, Q. H. (2020). A Network Intrusion Detection System for IoT Using Machine Learning. In IEEE Access. (Need to verify exact citation from IEEE Xplore) |

**Relevant Report Sections:** Dataset Description (Chapter 3), Literature Survey

### REF-03 — MRMR Algorithm

| Field | Value |
|---|---|
| Concept | Minimum Redundancy Maximum Relevance feature selection |
| Mathematical formula | Shown in `features.html`: `max [ I(x_j ; y) - (1/|S|) Σ I(x_j ; x_i) ]` |
| Original Paper | Peng, H., Long, F., & Ding, C. (2005). Feature selection based on mutual information criteria of max-dependency, max-relevance, and min-redundancy. IEEE Transactions on Pattern Analysis and Machine Intelligence, 27(8), 1226–1238. |
| Status | Formula cited in app but no explicit paper reference stored in workspace |

**Relevant Report Sections:** Methodology — Feature Selection, Literature Survey

### REF-04 — Random Fourier Features (Kernel Approximation)

| Field | Value |
|---|---|
| Concept | Random Fourier Feature (RFF) approximation used in SVM Kernel implementation |
| Referenced in | `methodology.html`: "Nystroem RBF kernel approximation (Rahimi & Recht)" |
| Original Paper | Rahimi, A., & Recht, B. (2007). Random Features for Large-Scale Kernel Machines. In Advances in Neural Information Processing Systems (NIPS). |
| Status | Named reference only — paper not present in workspace |

**Relevant Report Sections:** Methodology — ML Algorithm Implementation

### REF-05 — scikit-learn

| Field | Value |
|---|---|
| Software | scikit-learn 1.6.1 (Python ML library) |
| Reference | Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825–2830. |
| Version Used | 1.6.1 (explicitly stated in methodology.html) |
| Status | Version confirmed; formal citation reference not present in workspace |

**Relevant Report Sections:** Methodology — Implementation Tools, Technology Stack

---

## 3. References to Be Researched (Not in Workspace)

The following references should be looked up and added to the report's reference list:

| REF ID | Topic | Why Needed |
|---|---|---|
| REF-06 | Industrial IoT security challenges (general background) | Introduction / Literature Survey |
| REF-07 | Network intrusion detection survey papers | Literature Survey |
| REF-08 | PCA original formulation (Pearson, 1901 or Hotelling, 1933) | Methodology — PCA |
| REF-09 | MRMR original paper (Peng et al. 2005) | Methodology — MRMR (confirm citation) |
| REF-10 | Decision Tree (CART algorithm — Breiman et al.) | Methodology — Classifiers |
| REF-11 | KNN algorithm (Cover & Hart, 1967) | Methodology — Classifiers |
| REF-12 | SVM (Vapnik et al.) | Methodology — Classifiers |
| REF-13 | MLP / backpropagation (Rumelhart et al. 1986) | Methodology — Classifiers |
| REF-14 | Logistic Regression background | Methodology — Classifiers |
| REF-15 | Flask web framework | Technology Stack |
| REF-16 | IoTID20 dataset DOI / IEEE Xplore link | Dataset description |

---

## 4. Citation Format Note

**IEEE citation format** is assumed (as is standard for SASTRA B.Tech engineering reports and because the base paper is from IEEE Access). Example format:

```
[1] M. T. Houkan et al., "Enhancing Security in Industrial IoT Networks: Machine Learning Solutions for Feature Selection and Reduction," IEEE Access, vol. XX, pp. XXXX–XXXX, 2024.
```

The DOI, volume, and page numbers of REF-01 must be extracted from the PDF file or IEEE Xplore.

---

## 5. Summary: References Available vs. Needed

| Category | Count | Status |
|---|---|---|
| References verified in workspace (PDF present) | 1 (REF-01) | Ready for citation |
| References cited in code but no full details in workspace | 4 (REF-02 to REF-05) | Partial — need DOI/page verification |
| References needed but not yet identified | 11 (REF-06 to REF-16) | Must be researched before writing Literature Survey |

**Critical Gap:** A complete Literature Survey cannot be drafted until REF-06 through REF-16 are identified and verified.
