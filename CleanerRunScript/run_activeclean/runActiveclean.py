import argparse
from Cleaner.Activeclean.activeclean import run
from util.readData import load_data_csv
from util.saveData import save_data_csv


def Activeclean(data):
    pre_txt = run(data)
    return pre_txt


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run Activeclean data cleaning script.')
    parser.add_argument('--input', default='IMDB/imdb_features.p', type=str, help='Path to the input CSV file.')
    parser.add_argument('--output', default='output.csv', type=str, help='Path to the output CSV file.')

    # Parse arguments
    args = parser.parse_args()

    # Run the main function
    # Load the data
    print(f"Loading data from {args.input}")

    # Perform data cleaning
    print("Cleaning data")
    pre_txt = Activeclean(args.input)

    # Write results
    with open('../../results/activeclean/'+args.output, 'w', encoding='utf-8') as f:
        f.write(pre_txt)
        f.close()

