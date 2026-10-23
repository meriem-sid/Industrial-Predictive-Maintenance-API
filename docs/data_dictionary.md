
# C-MAPSS Data Dictionary

## 1. Dataset Overview

The NASA C-MAPSS dataset contains simulated turbofan engine
operating data used for predictive maintenance and Remaining
Useful Life (RUL) prediction.

Each row in the train and test files represents one engine
(`unit`) at one operating cycle (`cycle`).

## 2. General Columns

| Column | Description | Units |
|---|---|---|
| `unit` | Engine identifier | — |
| `cycle` | Operating cycle number | cycles |
| `setting_1` | First operating setting | — |
| `setting_2` | Second operating setting | — |
| `setting_3` | Third operating setting | — |

## 3. Sensor Dictionary

| Column | Symbol | Description | Units |
|---|---|---|---|
| `sensor_1` | T2 | Total temperature at fan inlet | °R |
| `sensor_2` | T24 | Total temperature at LPC outlet | °R |
| `sensor_3` | T30 | Total temperature at HPC outlet | °R |
| `sensor_4` | T50 | Total temperature at LPT outlet | °R |
| `sensor_5` | P2 | Pressure at fan inlet | psia |
| `sensor_6` | P15 | Total pressure in bypass-duct | psia |
| `sensor_7` | P30 | Total pressure at HPC outlet | psia |
| `sensor_8` | Nf | Physical fan speed | rpm |
| `sensor_9` | Nc | Physical core speed | rpm |
| `sensor_10` | epr | Engine pressure ratio (P50/P2) | — |
| `sensor_11` | Ps30 | Static pressure at HPC outlet | psia |
| `sensor_12` | phi | Ratio of fuel flow to Ps30 | pps/psi |
| `sensor_13` | NRf | Corrected fan speed | rpm |
| `sensor_14` | NRc | Corrected core speed | rpm |
| `sensor_15` | BPR | Bypass ratio | — |
| `sensor_16` | farB | Burner fuel-air ratio | — |
| `sensor_17` | htBleed | Bleed enthalpy | — |
| `sensor_18` | Nf_dmd | Demanded fan speed | rpm |
| `sensor_19` | PCNfR_dmd | Demanded corrected fan speed | rpm |
| `sensor_20` | W31 | HPT coolant bleed | lbm/s |
| `sensor_21` | W32 | LPT coolant bleed | lbm/s |

### Abbreviations

- LPC: Low-Pressure Compressor
- HPC: High-Pressure Compressor
- LPT: Low-Pressure Turbine
- HPT: High-Pressure Turbine
- RUL: Remaining Useful Life
- °R: Degrees Rankine
- psia: Pounds per square inch absolute
- rpm: Revolutions per minute
- lbm/s: Pounds mass per second
- —: Dimensionless quantity or no physical unit

## 4. Dataset Files

### Training files (`train_FD001.txt` to `train_FD004.txt`)

Contain complete run-to-failure trajectories for training
engines. Each engine is observed until failure. These records
can be used to learn degradation patterns and construct RUL
targets for model training.

### Test files (`test_FD001.txt` to `test_FD004.txt`)

Contain partial operating trajectories for test engines.
Observations stop before failure, and the remaining useful
life must be predicted at the final observed cycle.

### RUL files (`RUL_FD001.txt` to `RUL_FD004.txt`)

Contain the true remaining useful life for each corresponding
test engine, in the same engine order as the test file.
Each file has one RUL value per test engine, representing
the number of additional cycles until failure after its final
observed cycle.

## 5. Dataset Structure

Each raw train and test file contains 26 columns:

- 2 engine and cycle identifiers
- 3 operating settings
- 21 sensor measurements

The dataset includes four subsets: FD001, FD002, FD003,
and FD004, which differ in operating conditions and failure
modes.
