# Phygn Technical Architecture and Scientific Libraries

## 0. Purpose

This document defines the recommended technical architecture and libraries for autonomous Frontera C validation work.

---

## 1. Core stack

Required:

```txt
pandas
numpy
scikit-learn
scipy
pydantic
pytest
matplotlib
```

For PDFs:

```txt
pymupdf
pdfplumber
pypdf
```

Optional:

```txt
plotly
networkx
rich
typer
```

Not currently recommended:

```txt
tensorflow
pytorch
```

Reason:

```txt
Current bottleneck is evidence, dataset quality, benchmarking and controls, not neural-network capacity.
```

---

## 2. Architecture

Recommended modules:

```txt
phyng/provenance/
phyng/source_identity/
phyng/source_download/
phyng/observable_location/
phyng/targeted_ytrue/
phyng/dataset_expansion/
phyng/benchmarking/
phyng/model_registry/
phyng/controls/
phyng/ablation/
phyng/claim_permission/
phyng/campaigns/
```

---

## 3. Benchmarking module

```txt
phyng/benchmarking/
  datasets.py
  metrics.py
  baselines.py
  controls.py
  cross_validation.py
  leakage.py
  reports.py
```

### datasets.py

Use Pandas to:

```txt
load y_true JSON
normalize units
validate columns
preserve provenance
export canonical DataFrame
```

### metrics.py

Use NumPy/SciPy for:

```txt
MAE
RMSE
MAPE
max_abs_error
residuals
PredictiveGain
confidence/bootstrap if justified
```

### baselines.py

Use Scikit-Learn:

```txt
DummyRegressor
LinearRegression
Ridge
Lasso
PolynomialFeatures
Pipeline
StandardScaler
```

### cross_validation.py

Use Scikit-Learn:

```txt
LeaveOneOut
KFold
GroupKFold by source_id
Leave-one-source-out
```

### controls.py

Implement:

```txt
shuffled targets
shuffled conditions
random/null predictor
monotonic controls
parameter-count fairness
source leakage controls
```

### leakage.py

Detect:

```txt
same-source leakage
direct fitting leakage
condition/value leakage
duplicate y_true
model reading y_true columns
interpolation masquerading as prediction
```

---

## 4. Data schemas

All artifacts should be validated with Pydantic.

Required schema families:

```txt
SourceIdentity
SourceObject
ObservableLocation
YTrueRecord
DatasetQuality
ModelDefinition
PredictionRecord
ErrorMetricRecord
ControlResult
AblationResult
ClaimPermission
CampaignResult
```

---

## 5. Testing

Every campaign must include tests for:

```txt
input loading
schema validity
permission gates
blocked claims
no forbidden artifacts
deduplication
no fabricated provenance
report generation
```

For benchmark phases also test:

```txt
metric correctness
baseline reproducibility
cross-validation grouping
leakage flags
control dominance detection
```

---

## 6. Why no deep learning yet

Do not use PyTorch/TensorFlow until:

```txt
accepted_ytrue_count is large enough
multi-source train/test split exists
simple baselines are saturated
controls cannot explain the signal
nonlinear structure is genuinely needed
```

Deep learning before that would likely create:

```txt
overfit
leakage
false authority
uninterpretable curve-fitting
```

---

## 7. Final principle

```txt
Pandas and NumPy prepare the evidence.
Scikit-Learn tries to destroy the predictive illusion.
Deep learning waits until the data deserves it.
```
