# Report Structure Mapping

## Mapping of Project Evidence to Required Report Chapters

> Template basis: Assumed SASTRA B.Tech Mini-Project Report Format (6 chapters + prelim pages).
> Evidence verified from workspace files unless marked [PLACEHOLDER].

---

## PRELIMINARY PAGES

### Title Page [PLACEHOLDER — User Must Supply]
| Required | Status |
|---|---|
| Project title | **VERIFIED:** "Enhancing Security in Industrial IoT Networks: Machine Learning Solutions for Feature Selection and Reduction" (or a variant) |
| Student name(s) | MISSING — User must supply |
| Register number(s) | MISSING — User must supply |
| Department | MISSING — User must supply |
| Institution | SASTRA Deemed University (assumed) |
| Supervisor name | MISSING — User must supply |
| Academic year | MISSING — User must supply |

---

### Bonafide Certificate [PLACEHOLDER — Must Be Obtained from Department]
| Required | Status |
|---|---|
| Supervisor signature | Cannot be generated — physical document required |
| HOD signature | Cannot be generated — physical document required |

---

### Declaration [Template Required]
Content: Student declaration that the project is original and not submitted elsewhere.
**Status:** Standard template — user must obtain from department.

---

### Acknowledgements [Optional / User-Written]
Typically: Supervisor, department, IoTID20 dataset authors, Houkan et al. authors.

---

### Abstract [CAN BE DRAFTED NOW]
Available facts for abstract:
- Problem: IIoT edge gateways cannot process 79+ network features in real-time
- Solution: PCA and MRMR dimensionality reduction applied to IoTID20 dataset
- Dataset: 625,783 network flows, 86 attributes, 5 attack classes
- Method: 2 tasks × 9 feature configs × 6 classifiers = 108 experiments
- Key result: MRMR-12 achieves 99.864% accuracy (0.033% drop) with 84.81% feature reduction and 8.25M obs/s throughput — 98.3% training time reduction vs. baseline
- Flask web application for interactive live inference and explainability

---

### Table of Contents, List of Figures, List of Tables
Generated from report content after all chapters are written. **Status:** Cannot draft yet.

---

## CHAPTER 1: INTRODUCTION

| Section | Evidence Available | Source Files | Draftable? |
|---|---|---|---|
| 1.1 Background | IIoT security, edge constraints | index.html (motivation paragraph) | YES |
| 1.2 Problem Statement | 79+ features, MATLAB-only original | index.html, methodology.html | YES |
| 1.3 Existing System & Limitations | Baseline model sizes, training times | results_cache.json, index.html | YES |
| 1.4 Proposed System & Advantages | MRMR-12 compression ratio, accuracy retention | index.html KPI block, benchmark_service.py KPIs | YES |
| 1.5 Objectives | 9 specific objectives identified | project_overview.md | YES |
| 1.6 Scope and Boundaries | Online vs. offline scope defined | project_overview.md | YES |
| 1.7 Report Organization | Follows from chapter list | — | YES (last) |

---

## CHAPTER 2: LITERATURE SURVEY

| Section | Evidence Available | Source Files | Draftable? |
|---|---|---|---|
| 2.1 IIoT Security Background | Partial — code motivation paragraphs | index.html | PARTIAL — needs external references |
| 2.2 Network Intrusion Detection Systems | Not available in workspace | — | NO — needs REF-06, REF-07 |
| 2.3 Dimensionality Reduction Methods | PCA formulation, MRMR formula | features.html | PARTIAL — needs original papers |
| 2.4 ML Classifiers for NIDS | Methodology table | methodology.html | PARTIAL |
| 2.5 Related Works | Only REF-01 (base paper) available | basepaper/ | PARTIAL — needs 4–6 more papers |
| 2.6 Summary & Gap Identified | Gap stated in index.html (MATLAB reproducibility) | index.html | YES (once refs added) |

**Blocker:** Literature Survey is the weakest chapter. At minimum 5–8 additional related papers must be identified and reviewed before writing.

---

## CHAPTER 3: SYSTEM ANALYSIS AND DESIGN

| Section | Evidence Available | Source Files | Draftable? |
|---|---|---|---|
| 3.1 Existing System Analysis | Baseline MATLAB, KNN 273 MB model | methodology.html, output/models | YES |
| 3.2 Proposed System Overview | Flask app, 108 experiments, live demo | project_overview.md, app.py, routes/ | YES |
| 3.3 Functional Requirements | 13 verified FRs | project_overview.md | YES |
| 3.4 Non-Functional Requirements | 5 verified NFRs | project_overview.md | YES |
| 3.5 System Architecture Diagram | Flask architecture, Mermaid diagrams | system_architecture.md | YES |
| 3.6 Dataset Description | IoTID20, 625,783 rows, class dist. | dataset_info.txt, index.html | YES |
| 3.7 Module Architecture | All 12 modules analyzed | module_analysis.md | YES |
| 3.8 ER/Database Design | Flat-file data store (no RDBMS) | database_and_api_analysis.md | YES |
| 3.9 Data Flow Diagram | Full DFD in system_architecture.md | system_architecture.md | YES |

---

## CHAPTER 4: IMPLEMENTATION / METHODOLOGY

| Section | Evidence Available | Source Files | Draftable? |
|---|---|---|---|
| 4.1 Development Environment | Flask, Python, scikit-learn 1.6.1 | technology_stack.md | YES (but versions incomplete) |
| 4.2 Data Preprocessing | MinMax scaling, inf replacement, stratified split | methodology.html, dataset_info.txt | YES |
| 4.3 PCA Implementation | Full PCA, cumulative variance verification | features.html, pca_cumulative_variance.png, pca_explained_variance.csv | YES |
| 4.4 MRMR Implementation | Formula, top-12 rankings for binary+multiclass | features.html, mrmr_*_rankings.csv | YES |
| 4.5 ML Algorithm Implementation | 6 classifiers, MATLAB-sklearn translation | methodology.html | YES |
| 4.6 Training Pipeline | 108 experiments, Jupyter notebook | IoT_Intrusion_Detection_Reproduction.ipynb | YES (inferred from artifacts) |
| 4.7 Flask Application Implementation | All 5 routes, 3 API endpoints, 5 services | routes/, services/, templates/ | YES |
| 4.8 Live Inference Pipeline | InferenceService, ExplainService | inference_service.py, explain_service.py | YES |
| 4.9 Decision Tree Explainability | decision_path() traversal algorithm | explain_service.py lines 34–92 | YES |
| 4.10 Attack Preset Design | 5 authentic test-set presets | attack_presets.json, api_routes.py | YES |
| 4.11 Code Listings | Key excerpts identified | algorithm_and_code_analysis.md | YES |

---

## CHAPTER 5: RESULTS AND DISCUSSION

| Section | Evidence Available | Source Files | Draftable? |
|---|---|---|---|
| 5.1 Dataset Analysis Results | Class distributions, correlation heatmap | output/eda/ | YES (with figures) |
| 5.2 PCA Verification Results | 4 checkpoints verified vs. paper | features.html verification table | YES |
| 5.3 MRMR Feature Rankings | Top-12 binary + multiclass rankings | mrmr_*_rankings.csv | YES |
| 5.4 Binary Classification Results (all 54) | 54 records in results_cache.json | testing_and_results.md, results_cache.json | YES |
| 5.5 Multiclass Classification Results (all 54) | 54 records in results_cache.json | results_cache.json | YES |
| 5.6 Key KPI Comparisons | Peak accuracy, throughput, FAR, compression | benchmark_service.py, testing_and_results.md | YES |
| 5.7 MRMR vs. PCA vs. Baseline Comparison | All result data available | results_cache.json, accuracy_vs_features_binary.png | YES |
| 5.8 Confusion Matrix Analysis | 108 CM PNGs generated | output/results/confusion_matrices/ | YES (select key ones) |
| 5.9 Efficiency Frontier Analysis | efficiency_frontier_binary.png | output/results/ | YES |
| 5.10 Web Application Demonstration | Screenshots needed | Screenshot inventory section | PARTIAL — screenshots needed |
| 5.11 Discussion | All quantitative evidence available | testing_and_results.md | YES |

---

## CHAPTER 6: CONCLUSION AND FUTURE SCOPE

| Section | Evidence Available | Source Files | Draftable? |
|---|---|---|---|
| 6.1 Conclusion | All key findings verified | testing_and_results.md, limitations_and_future_scope.md | YES |
| 6.2 Objective Achievement Summary | All 9 objectives achieved | project_overview.md | YES |
| 6.3 Future Scope | Identified gaps and extensions | limitations_and_future_scope.md | YES |

---

## REFERENCES SECTION

| Status | Details |
|---|---|
| REF-01 ready | Houkan et al. 2024 — DOI needed from PDF |
| REF-02 partial | IoTID20 — Ullah & Mahmoud, need full IEEE citation |
| REF-03 to REF-05 | Need verification |
| REF-06 to REF-16 | Need to be researched |

---

## APPENDICES (Recommended)

| Appendix | Content | Status |
|---|---|---|
| Appendix A | Complete 108-experiment result table | Can be generated from results_cache.json |
| Appendix B | Source code listings (key files) | Files available |
| Appendix C | Full 79-feature catalog with definitions | Available from feature_catalog.py |
| Appendix D | Attack preset specifications | Available from attack_presets.json |
| Appendix E | Binary and Multiclass MRMR rankings | Available from CSV files |

---

## Summary — Chapter Draftability

| Chapter | Draftable Now? | Blocker |
|---|---|---|
| Preliminary pages | PARTIAL | Student details, supervisor, certificate template needed |
| Abstract | YES | Ready |
| Chapter 1 — Introduction | YES | Ready |
| Chapter 2 — Literature Survey | NO | 5–8 additional papers needed |
| Chapter 3 — System Analysis | YES | Ready |
| Chapter 4 — Implementation | YES | Python/library versions incomplete |
| Chapter 5 — Results | MOSTLY YES | UI screenshots still needed |
| Chapter 6 — Conclusion | YES | Ready |
| References | PARTIAL | Full citation details for REF-01; REF-06 to REF-16 unresearched |
| Appendices | YES | All data available |
