import pandas as pd


def load_data_csv(input_path):
    """Load data from the input CSV file."""
    return pd.read_csv(input_path)

