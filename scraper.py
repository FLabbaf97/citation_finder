import requests
import re
import time
import logging
from bs4 import BeautifulSoup
from tqdm import tqdm
from utils import *


# Just a placeholder user-agent
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

# Function for getting information of the web page
def get_paperinfo(paper_url):
    # Download the page
    response = requests.get(paper_url, headers=headers)

    # Check successful response
    if response.status_code != 200:
        raise URLFetchError(response.status_code)

    # Parse using BeautifulSoup
    paper_doc = BeautifulSoup(response.text, 'html.parser')

    return paper_doc

# Function for getting citations count from a list of paper names
def fetch_citations(names, dataset = None):
    citations = []
    for name in tqdm(names, desc="Fetching citations", unit="paper"):
        url = f'https://scholar.google.com/scholar?q={name}'

        try:
            doc = get_paperinfo(url)
        except URLFetchError as e:
            logging.error(f"Failed to fetch URL '{paper_url}': {e}")
            citations.append(float('nan'))
            continue

        if doc is not None:
            paper_tag, cite_tag, link_tag, author_tag = get_tags(doc)
            papername = get_papertitle(paper_tag)
            year, publication, author = get_author_year_publi_info(author_tag)
            cite = get_citecount(cite_tag)
            link = get_link(link_tag)
            
            print(f"Title: {papername}")
            print(f"Year: {year}")
            print(f"Publication: {publication}")
            print(f"Author: {author}")
            print(f"Citations: {cite}")
            # print(f"Link: {link}")

            if len(cite) == 1:
                citations.append(cite[0])
            elif len(cite) > 1:
                # TODO: Implement a better way to select the correct paper
                print("multiple papers found")
                citations.append(cite[0])
            else:
                citations.append(float('nan'))
        else:
            citations.append(float('nan'))

        time.sleep(5) # Sleep for 5 seconds to avoid getting blocked

    return citations
