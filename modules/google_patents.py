import requests
from bs4 import BeautifulSoup

def search_google_patents(claim_text, max_results=5):
    """
    Scrape Google Patents search results.
    Returns a list of dicts with 'number', 'title', 'abstract', 'source'
    """
    base_url = "https://patents.google.com/xhr/query"
    params = {
        "q": claim_text,
        "num": max_results
    }

    patents = []

    try:
        response = requests.get(f"https://patents.google.com/?q={claim_text}")
        soup = BeautifulSoup(response.text, "html.parser")

        # Each patent card
        cards = soup.find_all("tr", class_="result")[:max_results]
        for card in cards:
            title = card.find("span", class_="title")
            number = card.find("span", class_="patent-number")
            abstract = card.find("span", class_="abstract")

            patents.append({
                "number": number.text if number else "N/A",
                "title": title.text if title else "N/A",
                "abstract": abstract.text if abstract else "N/A",
                "source": "Google Patents",
                "similarity": 0
            })

    except Exception as e:
        print("Google Patents scrape error:", e)

    return patents
