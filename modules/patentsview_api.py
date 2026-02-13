import requests

def search_patentsview(claim_text, max_results=5):
    """
    Search US patents via PatentsView API.
    Returns a list of dicts with 'number', 'title', 'abstract', 'source'
    """
    url = "https://api.patentsview.org/patents/query"

    # Build a simple text query
    query = {
        "q": {
            "_text_any": {
                "patent_title": claim_text,
            }
        },
        "f": ["patent_number", "patent_title", "patent_abstract"],
        "o": {"per_page": max_results}
    }

    try:
        response = requests.post(url, json=query)
        data = response.json()

        patents = []
        for p in data.get("patents", []):
            patents.append({
                "number": p.get("patent_number"),
                "title": p.get("patent_title"),
                "abstract": p.get("patent_abstract"),
                "source": "PatentsView",
                "similarity": 0  # placeholder, will rank later
            })
        return patents

    except Exception as e:
        print("PatentsView API error:", e)
        return []
