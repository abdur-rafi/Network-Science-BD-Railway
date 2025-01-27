import requests
import networkx as nx
import time
from datetime import datetime, timedelta
from typing import List, Dict

# Set up CrossRef API URL and save interval (in minutes)
CROSSREF_BASE_URL = "https://api.crossref.org/works"
SAVE_INTERVAL_MINUTES = 10  # Save every 10 minutes

# Function to search for articles in the field of "network science" with pagination
def search_articles(query: str, start: int = 0, rows: int = 10) -> List[Dict]:
    print(f"Fetching articles with query: '{query}', starting from row {start}...")
    params = {
        "query": query,
        "rows": rows,
        "offset": start,
        "filter": "type:journal-article",
        "sort": "relevance",
        "order": "desc"
    }
    response = requests.get(CROSSREF_BASE_URL, params=params)
    if response.status_code == 200:
        articles = response.json().get("message", {}).get("items", [])
        print(f"Retrieved {len(articles)} articles.")
        return articles
    else:
        print("Failed to retrieve articles.")
        return []

# Function to get articles citing a given DOI
def get_citing_articles(doi: str) -> List[str]:
    print(f"Retrieving articles citing DOI: {doi}...")
    citing_dois = []
    try:
        response = requests.get(f"https://opencitations.net/index/coci/api/v1/citations/{doi}")
        if response.status_code == 200:
            citations = response.json()
            citing_dois = [citation["citing"] for citation in citations]
            print(f"Found {len(citing_dois)} articles citing DOI: {doi}.")
        else:
            print(f"Failed to retrieve citations for DOI: {doi}")
    except Exception as e:
        print(f"Error retrieving citations for DOI: {doi}: {e}")
    return citing_dois

# Function to process each batch of articles
def process_articles_batch(citation_graph: nx.DiGraph, articles: List[Dict]) -> None:
    # Add articles as nodes to the graph
    print("Adding articles as nodes to the graph...")
    for article in articles:
        doi = article.get("DOI")
        title = article.get("title", ["Unknown Title"])[0]
        authors = [author.get("given", "") + " " + author.get("family", "") for author in article.get("author", [])]
        authors_str = "; ".join(authors)
        
        # Add node with title and authors as metadata
        citation_graph.add_node(doi, title=title, authors=authors_str)
        print(f"Added node for article: '{title}' (DOI: {doi}), Authors: {authors_str}")
    
    # Add citations as edges to the graph
    print("Adding citations as edges to the graph...")
    for article in articles:
        doi = article.get("DOI")
        citing_dois = get_citing_articles(doi)
        for citing_doi in citing_dois:
            # Add edge from citing_doi to original doi (citing -> cited)
            citation_graph.add_edge(citing_doi, doi)
            print(f"Added edge from '{citing_doi}' -> '{doi}'")
        # Sleep briefly to avoid rate limits
        time.sleep(1)

# Main process to fetch and process articles in batches
def main():
    query = "network science"
    citation_graph = nx.DiGraph()  # Directed graph for citations
    start = 0
    rows_per_page = 10
    last_save_time = datetime.now()

    # Fetch and process articles in batches of 10
    while True:
        articles = search_articles(query=query, start=start, rows=rows_per_page)
        if not articles:
            print("No more articles found.")
            break
        
        # Process the current batch of articles
        process_articles_batch(citation_graph, articles)
        
        # Increment start to fetch the next batch of articles
        start += rows_per_page

        # Periodically save the graph based on time interval
        current_time = datetime.now()
        if current_time - last_save_time >= timedelta(minutes=SAVE_INTERVAL_MINUTES):
            # Save the graph
            filename = f"citation_network_{current_time.strftime('%Y%m%d_%H%M%S')}.gexf"
            nx.write_gexf(citation_graph, filename)
            print(f"Citation network saved as '{filename}'")
            # Update last save time
            last_save_time = current_time

        # Sleep briefly to avoid rate limits
        time.sleep(1)

    # Final save after all processing
    nx.write_gexf(citation_graph, "citation_network_final.gexf")
    print("Final citation network saved as 'citation_network_final.gexf'")

if __name__ == "__main__":
    main()
