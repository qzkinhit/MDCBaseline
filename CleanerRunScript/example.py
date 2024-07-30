import argparse
from util.readData import load_data_csv
from util.saveData import save_data_csv


def Horizon(df):
    """一个示例，实际这个函数应该在cleaner目录下的某个函数中"""
    # Example data cleaning operations
    df.dropna(inplace=True)  # Drop rows with missing values
    df.drop_duplicates(inplace=True)  # Drop duplicate rows
    return df


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run Activeclean data cleaning script.')
    parser.add_argument('--input', type=str, required=True, help='Path to the input CSV file.')
    parser.add_argument('--rule_text', type=str, required=True, help='Path to the input rule file.')
    parser.add_argument('--output', type=str, required=True, help='Path to the output CSV file.')

    # Parse arguments
    args = parser.parse_args()

    # Run the main function
    # Load the data
    print(f"Loading data from {args.input}")
    df = load_data_csv(args.input)

    # Perform data cleaning
    print("Cleaning data")
    df_cleaned = Horizon(df)

    # Save the cleaned data
    print(f"Saving cleaned data to {args.output}")
    save_data_csv(df_cleaned, args.output)
