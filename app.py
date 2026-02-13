import streamlit as st
import random

# Import from modules
from modules.claim_parser import extract_features, detect_risky_words
from modules.question_engine import get_question
from modules.evaluator import evaluate_answer


# ===============================
# PRIOR ART COMBINATION (kept in app for now)
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

    # Feature extraction (from module)
    st.subheader("Extracted Claim Features:")
    features = extract_features(claim)
    for f in features:
        st.write("- " + f)

    # Risk detection (from JSON via module)
    detected = detect_risky_words(claim)
    if detected:
        st.warning("Risky drafting terms detected:")
        for d in detected:
            st.write("- " + d)

mode = st.selectbox(
    "Select Objection Type",
    ["Novelty", "Inventive Step", "Clarity"]
)

if st.button("Start Hearing"):

    # Get question from module
    question = get_question(mode)
    st.session_state["question"] = question

    # Generate examiner attack
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

        # Evaluate using module
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
