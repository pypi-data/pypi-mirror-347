import pandas as pd

def read_csv_with_info(filepath, preview_rows=5, max_columns=10, global_max_columns=10, width=1000) -> pd.DataFrame:
    """
    Reads a CSV file and displays basic information.

    Parameters:
        filepath (str): Path to the CSV file.
        preview_rows (int): Number of rows to display in the preview.
        max_columns (int): Number of columns to show in the preview (inside option_context).
        global_max_columns (int): Number of columns to globally allow in pandas display.
        width (int): Width of the display (in characters).

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    try:
        pd.set_option('display.max_columns', global_max_columns)

        df = pd.read_csv(filepath)

        print("\n--- File Load Info ---")
        print(f"Successfully loaded: {filepath}")
        print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")

        print("\n--- Column Names ---")
        print(', '.join(df.columns))

        print("\n--- Data Types ---")
        print(df.dtypes.to_string())

        print(f"\n--- Preview (first {preview_rows} rows) ---")
        with pd.option_context('display.max_columns', max_columns, 'display.width', width):
            print(df.head(preview_rows))

        return df
    
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except Exception as e:
        print(f"Error reading the file: {e}")
