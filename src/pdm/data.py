
from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

COLUMNS = (
    ["unit", "cycle"]
    + [f"setting_{i}" for i in range(1, 4)]
    + [f"sensor_{i}" for i in range(1, 22)]
)

VALID_SUBSETS = {"FD001", "FD002", "FD003", "FD004"}


def load_cmapss(subset: str = "FD001", split: str = "train") -> pd.DataFrame:
    """Load a raw C-MAPSS file with named columns.

    subset: "FD001".."FD004"; split: "train" or "test".
    Returns one row per (unit, cycle).
    """

    if subset not in VALID_SUBSETS:
        raise ValueError(
            f"Invalid subset: {subset}. Choose FD001, FD002, FD003, or FD004."
        )

    if split not in {"train", "test"}:
        raise ValueError(
            f"Invalid split: {split}. Choose 'train' or 'test'."
        )

    path = DATA_DIR /"raw"/"CMAPSSData"/ f"{split}_{subset}.txt"

    df = pd.read_csv(path, sep=r"\s+", header=None)


    if df.shape[1] != len(COLUMNS):
        raise ValueError(
            f"Expected {len(COLUMNS)} columns, found {df.shape[1]} in {path}"
        )

    df.columns = COLUMNS

    return df
  

def load_rul(subset: str = "FD001") -> pd.DataFrame:
    """Load true RUL values for test engines."""

    if subset not in VALID_SUBSETS:
        raise ValueError(
            f"Invalid subset: {subset}. Choose FD001, FD002, FD003, or FD004."
        )

    path = DATA_DIR /"raw"/"CMAPSSData"/ f"RUL_{subset}.txt"

    rul = pd.read_csv(path, sep=r"\s+", header=None, names=["true_rul"])
    
   # Assumption: RUL values follow test-engine order, with units numbered from 1.
    rul.insert(0, "unit", range(1, len(rul) + 1))

    return rul



  
  
