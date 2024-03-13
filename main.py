import argparse
import logging
import pandas as pd
from scraper import fetch_citations
from utils import save_results_to_csv

def main(dataset_path, save_path):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Read dataset
    try:
        database = pd.read_csv(dataset_path)
    except FileNotFoundError:
        logging.error(f"Dataset file '{dataset_path}' not found.")
        return

    names = database['title'].tolist()

    # Fetch citations
    citations = fetch_citations(names)

    # Add citations to the dataset
    database['citations'] = citations

    # Save results to CSV
    save_results_to_csv(database, save_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch citations for papers in a dataset.")
    parser.add_argument("--dataset_path", type=str, help="Path to the dataset CSV file")
    parser.add_argument("--save_path", type=str, help="Path to save the results CSV file")
    args = parser.parse_args()

    main(args.dataset_path, args.save_path)
