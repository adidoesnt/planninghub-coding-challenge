import pandas as pd

'''
Reads a CSV file and returns a pandas DataFrame.

Args:
    path (str): The path to the CSV file.

Returns:
    pd.DataFrame: A pandas DataFrame containing the data from the CSV file.
'''
def read_csv(path: str) -> pd.DataFrame:
    try:
        print(f"[CSV] Reading CSV file: {path}")
        return pd.read_csv(path)
    except Exception as e:
        print(f"[CSV] Error reading CSV file: {e}")
        raise e
