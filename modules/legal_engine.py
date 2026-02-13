import json

def load_legal_rules():
    with open("legal_rules/indian_patent_act.json", "r") as file:
        return json.load(file)

def analyze_indian_patent_compliance(claim_text):
    rules = load_legal_rules()
    claim_lower = claim_text.lower()
    issues = []

    for section, content in rules.items():
        for keyword in content["trigger_keywords"]:
            if keyword in claim_lower:
                issues.append({
                    "section": section,
                    "reason": content["rejection_reason"],
                    "defense": content["defense_strategy"]
                })
                break

    return issues
