import pandas as pd

def add_rolling_features(df: pd.DataFrame, sensors: list[str], window: int) -> pd.DataFrame:
    """Return a copy with <sensor>_mean_<w> and <sensor>_std_<w> columns,
    computed per unit over the current and previous (window-1) cycles."""
    
    if window < 1:
      raise ValueError("window must be >= 1")

    missing = set(sensors) - set(df.columns)
    if missing:
      raise ValueError(f"Missing sensor columns: {sorted(missing)}")
    
    df_1=df.copy()
    df_1= df_1.sort_values(by=["unit", "cycle"])
    
    for sensor in sensors:

        # Rolling mean
        df_1[f"{sensor}_mean_{window}"] = (
            df_1.groupby("unit")[sensor]
            .transform(lambda s: s.rolling(window=window, min_periods=1).mean())
        )

        # Rolling standard deviation
        df_1[f"{sensor}_std_{window}"] = (
            df_1.groupby("unit")[sensor]
            .transform(lambda s: s.rolling(window=window, min_periods=1).std())
        )
    return df_1
