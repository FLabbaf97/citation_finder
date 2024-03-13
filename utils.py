import re
import pandas as pd

class URLFetchError(Exception):
    pass

# Function for getting tags from the document
def get_tags(doc):
    paper_tag = doc.select('[data-lid]')
    cite_tag = doc.select('a[href*="cites"]')
    link_tag = doc.find_all('h3', {"class": "gs_rt"})
    author_tag = doc.find_all("div", {"class": "gs_a"})

    return paper_tag, cite_tag, link_tag, author_tag

# Function for getting paper titles
def get_papertitle(paper_tag):
    paper_names = []

    for tag in paper_tag:
        paper_names.append(tag.select('h3')[0].get_text())

    return paper_names

# Function for getting citation count
def get_citecount(cite_tag):
    cite_count = []
    for i in cite_tag:
        cite = i.text
        if i is None or cite is None:
            cite_count.append(0)
        else:
            tmp = re.search(r'\d+', cite)
            if tmp is None:
                cite_count.append(0)
            else:
                cite_count.append(int(tmp.group()))

    return cite_count

# Function for getting link information
def get_link(link_tag):
    links = []

    for i in range(len(link_tag)):
        links.append(link_tag[i].a['href'])

    return links

# Function for getting author, year, and publication information
def get_author_year_publi_info(authors_tag):
    years = []
    publication = []
    authors = []
    for i in range(len(authors_tag)):
        authortag_text = (authors_tag[i].text).split()
        year = int(re.search(r'\d+', authors_tag[i].text).group())
        years.append(year)
        publication.append(authortag_text[-1])
        author = authortag_text[0] + ' ' + re.sub(',', '', authortag_text[1])
        authors.append(author)

    return years, publication, authors

# Function for saving results to CSV
def save_results_to_csv(dataframe, save_path):
    try:
        dataframe.to_csv(save_path, index=False)
        print(f"Results saved to '{save_path}'")
    except Exception as e:
        print(f"Error occurred while saving results: {e}")
