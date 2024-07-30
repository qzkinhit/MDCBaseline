import pandas as pd

def save_data_csv(df, output_path):
    """Save the cleaned data to the output CSV file."""
    df.to_csv(output_path, index=False)
