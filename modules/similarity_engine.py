from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_similarity(claim_text, prior_art_list):

    documents = [claim_text]

    for doc in prior_art_list:
        documents.append(doc["abstract"])

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

    scored_results = []
    for idx, score in enumerate(similarities[0]):
        prior_art_list[idx]["similarity"] = float(score)
        scored_results.append(prior_art_list[idx])

    ranked = sorted(scored_results, key=lambda x: x["similarity"], reverse=True)

    return ranked[:3]
