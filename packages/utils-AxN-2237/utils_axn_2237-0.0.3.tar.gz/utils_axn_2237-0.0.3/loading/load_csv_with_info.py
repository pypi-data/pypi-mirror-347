loading csv
import pandas as pd

def read_csv_with_info(filepath):
    """
    Reads a CSV file and displays basic information.

    Parameters:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    try:
        df = pd.read_csv(filepath)

        print(f"\n Successfully loaded: {filepath}")
        print(f"\n Shape: {df.shape[0]} rows × {df.shape[1]} columns\n")
        print(" Column names:", df.columns.tolist())
        print("\n Preview of data:")
        print(df.head())
        print("\n Data types:")
        print(df.dtypes)
        return df

    except FileNotFoundError:
        print(f" File not found: {filepath}")
    except Exception as e:
        print(f" Error reading the file: {e}")
