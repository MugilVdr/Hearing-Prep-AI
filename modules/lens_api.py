import requests

LENS_API_TOKEN = "YOUR_LENS_API_KEY"

def search_lens(query_text, max_results=5):
    url = "https://api.lens.org/patent/search"

    headers = {
        "Authorization": f"Bearer {LENS_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "query": {
            "match": {
                "abstract": query_text
            }
        },
        "size": max_results
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return []

    data = response.json()

    results = []
    for p in data.get("data", []):
        results.append({
            "source": "Lens",
            "number": p.get("lens_id"),
            "title": p.get("title"),
            "abstract": p.get("abstract")
        })

    return results
