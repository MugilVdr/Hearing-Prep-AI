def generate_objection(claim_text, top_prior):

    objections = []

    for art in top_prior:

        if art["similarity"] > 0.4:
            objections.append(f"""
Novelty Objection:

Claim appears anticipated by {art['source']} Patent {art['number']}.

The prior art discloses similar subject matter:
{art['title']}

Similarity Score: {round(art['similarity'],2)}

Therefore, claim lacks novelty under Section 2(1)(j) of Indian Patent Act.
""")

        else:
            objections.append(f"""
Inventive Step Concern:

Claim shares overlapping features with {art['source']} Patent {art['number']}.

Further clarification required on technical advancement over cited prior art.
""")

    return objections
