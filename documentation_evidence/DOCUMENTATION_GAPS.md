# Documentation Gaps

## Critical Gaps (Report Cannot Be Completed Without These)

### GAP-01 — Student Personal Details [BLOCKING: Title Page + Certificate]
| Field | Status | Action Required |
|---|---|---|
| Student name(s) | MISSING | User must supply |
| Register number(s) | MISSING | User must supply |
| Department name | MISSING | User must supply |
| Supervisor name | MISSING | User must supply |
| Academic year | MISSING | User must supply |
| Programme (B.Tech, specialization) | MISSING | User must supply |

---

### GAP-02 — Institutional Template [BLOCKING: Formatting]
| Item | Status | Action Required |
|---|---|---|
| SASTRA report format PDF/DOCX | NOT FOUND in workspace | User must obtain from department |
| Page margins | UNVERIFIED | Check actual SASTRA guidelines |
| Font specification | UNVERIFIED | Check actual SASTRA guidelines |
| Abstract word limit | UNVERIFIED | Check actual SASTRA guidelines |
| Watermark or cover design | UNVERIFIED | Check actual SASTRA guidelines |

---

### GAP-03 — Literature Survey Sources [BLOCKING: Chapter 2]
| Status | Detail |
|---|---|
| Only 1 primary reference in workspace | Houkan et al. 2024 (base paper PDF) |
| 5–8 additional papers needed | IIoT security, NIDS survey, PCA/MRMR papers |
| IoTID20 full citation missing | Need Ullah & Mahmoud paper DOI, volume, pages |
| MRMR original paper citation missing | Peng et al. 2005 — needs verification |

---

### GAP-04 — Web Application UI Screenshots [BLOCKING: Results Chapter]
| Needed Screenshot | Status |
|---|---|
| Dashboard page (KPI cards) | NOT CAPTURED — needs browser |
| Live demo — Anomaly detection result | NOT CAPTURED |
| Live demo — Decision Tree traversal path | NOT CAPTURED |
| Live demo — Benign Normal flow result | NOT CAPTURED |
| Benchmarks table page | NOT CAPTURED |
| Confusion matrix modal | NOT CAPTURED |
| Feature reduction page | NOT CAPTURED |
| Methodology page | NOT CAPTURED |

**To capture:** Run `python app.py` and take browser screenshots of each page.

---

### GAP-05 — Exact Python and Package Versions [LOW PRIORITY]
| Item | Status |
|---|---|
| Python version | Not verified (no `python --version` output saved) |
| Flask version | Not in requirements.txt (no requirements.txt found) |
| scikit-learn version | 1.6.1 (stated in methodology.html — VERIFIED) |
| NumPy version | Not verified |
| pandas version | Not verified |
| joblib version | Not verified |

**Action:** Run `pip freeze` in project environment and record output.

---

### GAP-06 — Base Paper Full Citation Details [MEDIUM PRIORITY]
| Item | Status | Action |
|---|---|---|
| DOI | Not extracted | Open basepaper PDF, copy from header |
| Volume and issue number | Not extracted | Check IEEE Xplore for Houkan et al. 2024 |
| Page numbers | Not extracted | Check IEEE Xplore |

---

### GAP-07 — ROC Curves Missing [LOW PRIORITY]
| Status | Detail |
|---|---|
| output/results/roc_curves/ | EMPTY — no ROC curve images generated |
| Prediction CSV files | Available for all 108 experiments |
| Resolution | ROC curves can be generated from `preds_*.csv` files using scikit-learn |

---

### GAP-08 — Jupyter Notebook Internal Details [LOW PRIORITY]
| Status | Detail |
|---|---|
| IoT_Intrusion_Detection_Reproduction.ipynb | File present (454 KB) but not read (binary IPYNB format) |
| MRMR library used | Unknown — could be `mrmr-selection`, `pymrmr`, or custom implementation |
| Exact preprocessing steps | Inferred from artifacts; direct notebook reading would confirm |
| Training loop structure | Inferred from artifact naming; notebook would confirm |

**Action:** Open the notebook in Jupyter and document the cell structure.

---

## Non-Critical Gaps (Can Note as Limitations in Report)

| GAP-ID | Description | Report Treatment |
|---|---|---|
| GAP-09 | No cross-validation | Acknowledge as limitation in Chapter 6 |
| GAP-10 | SVM Kernel poor performance explanation | Discuss as finding in Chapter 5 |
| GAP-11 | Duplicate rows kept | Acknowledge in Dataset section |
| GAP-12 | No automated test suite | Acknowledge in limitations |
| GAP-13 | Class imbalance not addressed | Acknowledge as limitation + future scope |

---

## Summary Table

| Gap ID | Severity | Blocks | Can Report Section Be Drafted Without It? |
|---|---|---|---|
| GAP-01 | CRITICAL | Title page, certificate, declaration | NO |
| GAP-02 | CRITICAL | All formatting | NO — but content can be written first |
| GAP-03 | CRITICAL | Chapter 2 (Literature Survey) | NO |
| GAP-04 | HIGH | Chapter 5 (UI demonstration) | PARTIAL — can write around it |
| GAP-05 | LOW | Technology stack table | PARTIAL |
| GAP-06 | MEDIUM | Reference list | PARTIAL — can cite without page numbers |
| GAP-07 | LOW | Results | Optional — can omit ROC curves |
| GAP-08 | LOW | Methodology details | PARTIAL — inferred details are sufficient |
