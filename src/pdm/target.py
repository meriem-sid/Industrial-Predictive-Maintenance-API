import pandas as pd

# Only use on training data: RUL requires each engine's final cycle,
# which is unknown for test engines because their histories end before failure.
def add_rul(df: pd.DataFrame, cap: int | None = None) -> pd.DataFrame:
    """Return a copy of a TRAINING DataFrame with an added 'rul' column.

    rul = max cycle of the unit - current cycle, optionally capped at `cap`.
    """
    new_df= df.copy()
    new_df['rul']= new_df.groupby('unit')['cycle'].transform("max") - new_df['cycle']
    
    if cap is not None:
        new_df["rul"] = new_df["rul"].clip(upper=cap)
    
    return new_df