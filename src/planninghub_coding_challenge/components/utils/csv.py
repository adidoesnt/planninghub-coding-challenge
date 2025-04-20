import pandas as pd

def read_csv(path: str) -> pd.DataFrame:
    try:
        print(f"[CSV] Reading CSV file: {path}")
        return pd.read_csv(path)
    except Exception as e:
        print(f"[CSV] Error reading CSV file: {e}")
        raise e
