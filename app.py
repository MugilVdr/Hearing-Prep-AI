import streamlit as st
import random

# Import from modules
from modules.claim_parser import extract_features, detect_risky_words
from modules.question_engine import get_question
from modules.evaluator import evaluate_answer
from modules.legal_engine import analyze_indian_patent_compliance
from modules.patentsview_api import search_patentsview
from modules.google_patents import search_google_patents
from modules.similarity_engine import rank_similarity
from modules.legal_reasoner import generate_objection



# ===============================
# PRIOR ART COMBINATION ENGINE
# ===============================
def generate_prior_art_combination():
    d1 = "an adaptive monitoring agent system"
    d2 = "machine learning optimization with automatic deployment"

    return (
        f"D1 discloses {d1}. "
        f"D2 discloses {d2}. "
        "It would have been obvious to combine D1 with D2 to achieve predictable improvement. "
        "Therefore the invention lacks inventive step."
    )


# ===============================
# BASIC EXAMINER ATTACK
# ===============================
def generate_examiner_attack(mode):
    if mode == "Novelty":
        return "Claim lacks novelty over known adaptive systems."
    elif mode == "Inventive Step":
        return "Claim appears obvious as combination of known monitoring and optimization systems."
    else:
        return "Claim lacks clarity due to functional terminology."


# ===============================
# STREAMLIT UI
# ===============================

st.title("⚖️ Patent Hearing Prep Simulator")

claim = st.text_area("Paste your patent claim")

if claim:

    # -------------------------------
    # Feature Extraction
    # -------------------------------
    st.subheader("Extracted Claim Features:")
    features = extract_features(claim)
    for f in features:
        st.write("- " + f)

    # -------------------------------
    # Risky Word Detection
    # -------------------------------
    detected = detect_risky_words(claim)
    if detected:
        st.warning("Risky drafting terms detected:")
        for d in detected:
            st.write("- " + d)

    # -------------------------------
    # Indian Patent Act Compliance
    # -------------------------------
    st.subheader("Indian Patent Act Compliance Check")

    legal_issues = analyze_indian_patent_compliance(claim)

    if legal_issues:
        for issue in legal_issues:
            st.error(f"Potential Issue under {issue['section']}")
            st.write("Reason:", issue["reason"])
            st.info("Suggested Defense Strategy:")
            st.write(issue["defense"])
    else:
        st.success("No immediate Indian Patent Act objections detected.")

# ===============================
# 🔍 PRIOR ART INTERNET SEARCH
# ===============================


if st.button("Search Prior Art & Generate Objection"):

    pv_results = search_patentsview(claim)
    google_results = search_google_patents(claim)

    all_results = pv_results + google_results

    if not all_results:
        st.error("No prior art found.")
    else:
        # Rank by similarity
        ranked = rank_similarity(claim, all_results)

        # Generate controller-style objections
        objections = generate_objection(claim, ranked)

        st.subheader("Top Prior Art Documents:")
        for art in ranked:
            st.write(f"**{art['source']} - {art['number']}**")
            st.write(f"Title: {art['title']}")
            st.write(f"Abstract: {art['abstract']}")
            st.write(f"Similarity Score: {round(art['similarity'], 2)}")
            st.divider()

        st.header("Controller Style Objections")
        for obj in objections:
            st.write(obj)



# ===============================
# HEARING SIMULATION
# ===============================

mode = st.selectbox(
    "Select Objection Type",
    ["Novelty", "Inventive Step", "Clarity"]
)

if st.button("Start Hearing"):

    question = get_question(mode)
    st.session_state["question"] = question

    if mode == "Inventive Step":
        attack = generate_prior_art_combination()
    else:
        attack = generate_examiner_attack(mode)

    st.session_state["attack"] = attack


if "question" in st.session_state:

    st.subheader("Examiner Rejection:")
    st.write(st.session_state["attack"])

    st.subheader("Examiner Question:")
    st.write(st.session_state["question"])

    answer = st.text_area("Your Response")

    if st.button("Submit Answer"):

        score, feedback = evaluate_answer(answer)

        st.subheader("Score:")
        st.write(f"{score} / 10")

        if score >= 8:
            st.success("Strong argument! Well structured.")
        elif score >= 5:
            st.warning("Moderate argument. Improve structure.")
        else:
            st.error("Weak argument. Needs more technical reasoning.")

        if feedback:
            st.subheader("Suggestions:")
            for item in feedback:
                st.write("- " + item)
