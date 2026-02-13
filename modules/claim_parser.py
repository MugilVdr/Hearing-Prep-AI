import json

# Feature extractor
def extract_features(claim_text):
    keywords = [
        "mechanism", "model", "configuration", "agent", "system",
        "data source", "validation", "optimization", "deployment",
        "feedback", "repository", "component", "processor", "memory"
    ]

    found = []
    claim_lower = claim_text.lower()

    for key in keywords:
        if key in claim_lower:
            found.append(key)

    return found


# Load risky words from JSON
def detect_risky_words(claim_text):

    with open("data/risk_terms.json", "r") as file:
        data = json.load(file)

    risky_terms = data["risk_terms"]

    claim_lower = claim_text.lower()
    detected = [word for word in risky_terms if word in claim_lower]

    return detected
