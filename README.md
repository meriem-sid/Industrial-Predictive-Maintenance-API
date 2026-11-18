# Industrial Predictive Maintenance API

Prototype that predicts the **Remaining Useful Life (RUL)** of turbofan engines
from NASA's simulated C-MAPSS dataset, with the goal of serving predictions
through a REST API.

Current focus: subset **FD001** (one operating condition, one failure mode).

## Project structure

```
├── data/
│   ├── raw/CMAPSSData/      # raw NASA files (not tracked, see "Data")
│   └── processed/           # derived datasets
├── docs/
│   └── data_dictionary.md   # column and sensor definitions
├── models/                  # saved models (not tracked yet)
├── notebooks/
│   ├── 01_data_inspection.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_target_baseline.ipynb
│   └── 04_validation.ipynb  # in progress
├── reports/
│   └── results.md           # evaluation results
├── src/pdm/
│   ├── data.py              # load_cmapss(), load_rul()
│   ├── target.py            # add_rul() with optional cap
│   └── features.py          # add_rolling_features()
├── tests/
│   └── test_features.py     # leakage tests for rolling features
├── pyproject.toml
└── requirements.txt
```

## Setup

Requires Python 3.11+.

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (source .venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
pip install -e .                # makes `pdm` importable from notebooks and tests
```

## Data

1. Download the dataset: <https://data.nasa.gov/docs/legacy/CMAPSSData.zip>
2. Unzip it so the files sit directly in `data/raw/CMAPSSData/`
   (e.g. `data/raw/CMAPSSData/train_FD001.txt`).

See [docs/data_dictionary.md](docs/data_dictionary.md) for column and sensor descriptions.

## Usage

```python
from pdm.data import load_cmapss, load_rul
from pdm.target import add_rul
from pdm.features import add_rolling_features

train = load_cmapss("FD001", "train")
train = add_rul(train, cap=125)
train = add_rolling_features(train, sensors=["sensor_2", "sensor_3"], window=5)
```

Run the tests:

```bash
pytest
```

## Progress

### Done

- **Project setup** — package layout (`src/pdm`), `pyproject.toml`, pinned requirements.
- **Data loading** — `load_cmapss()` and `load_rul()` with subset/split validation
  and a column-count check.
- **Data inspection** (`01`) — shapes, dtypes, missing values, engine lifetimes,
  cycle continuity check, constant / near-constant columns.
- **EDA** (`02`) — sensor trends vs. cycles-before-failure, noise assessment,
  correlation and redundancy analysis.
  - Dropped as constant / uninformative: `setting_3`, `sensor_1`, `sensor_5`,
    `sensor_10`, `sensor_16`, `sensor_18`, `sensor_19`.
  - `sensor_9` and `sensor_14` are highly correlated (0.96) but trend
    inconsistently across engines — to be tested with and without them.
- **Target & baselines** (`03`) — `add_rul()` with optional cap (125 cycles);
  constant and age-based baselines evaluated on the official FD001 test set.
- **Feature engineering** — `add_rolling_features()` (per-engine rolling mean / std),
  with tests confirming no future leakage and no mixing between engines.

### Baseline results (FD001 test set, last cycle per engine)

| Baseline                 | MAE   | RMSE  |
|--------------------------|-------|-------|
| Age-based (capped)       | 28.01 | 36.79 |
| Age-based (uncapped)     | 32.05 | 40.20 |
| Constant (capped mean)   | 35.90 | 43.07 |
| Constant (uncapped mean) | 40.88 | 52.62 |

Full details in [reports/results.md](reports/results.md).

### In progress

- **Validation strategy** (`04`) — comparing `KFold` vs. `GroupKFold` (grouped by
  engine) with a scaled Ridge pipeline, to show why rows from the same engine
  must not appear in both train and validation folds.

## Next steps

1. Finish the validation notebook and adopt `GroupKFold` by engine as the standard CV.
2. Build the feature pipeline: selected sensors + rolling features (tune window size),
   with and without `sensor_9` / `sensor_14`.
3. Train and compare models (Ridge → Random Forest / gradient boosting) against
   the baselines, using capped RUL.
4. Evaluate the best model on the official FD001 test set and update `reports/results.md`.
5. Save the trained pipeline to `models/` and add a reusable predict function.
6. Build the API (e.g. FastAPI): a `/predict` endpoint taking an engine's sensor
   history and returning predicted RUL, plus a `/health` endpoint.
7. Add API tests, input validation, and containerize with Docker.
8. Extend to FD002–FD004 (multiple operating conditions → per-condition normalization).
