import argparse
from Cleaner.Activeclean.activeclean import run
from util.readData import load_data_csv
from util.saveData import save_data_csv


def Activeclean(data):
    clean_data = run(data)
    return clean_data


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run Activeclean data cleaning script.')
    parser.add_argument('--input', default='imdb_features.p', type=str, help='Path to the input CSV file.')
    parser.add_argument('--rule_text', default=None, type=str, help='Path to the input rule file.')
    parser.add_argument('--output', default='output.csv', type=str, help='Path to the output CSV file.')

    # Parse arguments
    args = parser.parse_args()

    # Run the main function
    # Load the data
    print(f"Loading data from {args.input}")

    # Perform data cleaning
    print("Cleaning data")
    cleaned = Activeclean(args.input)
