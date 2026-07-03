# Phygn v5.7 — Benchmarking Stack Hardening

## 0. Purpose

v5.7 formalizes the benchmark/data stack used for future model comparison, controls and leakage tests.

---

## 1. Required dependencies

Add or document:

```txt
pandas
numpy
scikit-learn
scipy
pydantic
pytest
matplotlib
```

Optional but useful:

```txt
pdfplumber
pymupdf
pypdf
```

---

## 2. Required package

Create or update:

```txt
phyng/benchmarking/
  __init__.py
  datasets.py
  metrics.py
  baselines.py
  controls.py
  cross_validation.py
  leakage.py
  reports.py
```

---

## 3. datasets.py

Responsibilities:

```txt
load accepted y_true JSON
convert to pandas DataFrame
validate required columns
normalize observable class names
normalize units
preserve provenance columns
export canonical CSV/JSON if needed
```

Required functions:

```python
load_ytrue_dataset(path: str | Path) -> pd.DataFrame
validate_ytrue_dataframe(df: pd.DataFrame) -> dict
normalize_units(df: pd.DataFrame) -> pd.DataFrame
```

---

## 4. metrics.py

Responsibilities:

```txt
MAE
RMSE
MAPE with zero handling
max_abs_error
residual table
PredictiveGain smoke-test calculation
```

Required functions:

```python
mae(y_true: np.ndarray, y_pred: np.ndarray) -> float
rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float
safe_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float | None
max_abs_error(y_true: np.ndarray, y_pred: np.ndarray) -> float
predictive_gain(error_base: float, error_candidate: float) -> float | None
```

---

## 5. baselines.py

Responsibilities:

```txt
DummyRegressor mean/median
LinearRegression
Ridge
Lasso
simple exponential transforms if implemented safely
```

Use Scikit-Learn where appropriate.

Required model metadata:

```txt
model_id
model_family
parameter_count
fitted_or_not
leakage_risk
input_features
target_variable
```

---

## 6. controls.py

Responsibilities:

```txt
negative control models
shuffled target tests
random/null predictors
monotonic interpolation controls where explicitly marked high leakage
parameter fairness checks
```

No control may be hidden if it beats the candidate.

---

## 7. cross_validation.py

Responsibilities:

```txt
LeaveOneOut
KFold if N allows
GroupKFold by source_id if multi-source
leave-one-source-out evaluation
```

Rule:

```txt
Out-of-source performance is stronger than in-source curve fit.
```

---

## 8. leakage.py

Responsibilities:

```txt
detect same-source leakage
detect direct fitting to all y_true
detect condition/value leakage
detect interpolation masquerading as prediction
detect high parameter-count controls
```

Required leakage labels:

```txt
LOW
MEDIUM
HIGH
BLOCKING
```

---

## 9. reports.py

Responsibilities:

```txt
markdown model comparison report
dataset quality report
control decision report
benchmark readiness report
```

---

## 10. Required tests

Add:

```txt
tests/test_benchmarking_datasets_v5_7.py
tests/test_benchmarking_metrics_v5_7.py
tests/test_benchmarking_baselines_v5_7.py
tests/test_benchmarking_controls_v5_7.py
tests/test_benchmarking_cross_validation_v5_7.py
tests/test_benchmarking_leakage_v5_7.py
```

---

## 11. Final principle

```txt
Pandas and NumPy prepare the evidence.
Scikit-Learn tries to destroy the predictive illusion.
```
