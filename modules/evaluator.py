def evaluate_answer(answer):

    score = 0
    feedback = []

    if len(answer) > 50:
        score += 2
    else:
        feedback.append("Expand your explanation.")

    technical_words = ["feature", "technical", "effect", "structure", "element"]
    if any(word in answer.lower() for word in technical_words):
        score += 3
    else:
        feedback.append("Include technical terminology.")

    comparison_words = ["different", "distinguish", "compared", "whereas"]
    if any(word in answer.lower() for word in comparison_words):
        score += 3
    else:
        feedback.append("Compare your claim with prior art.")

    if "because" in answer.lower():
        score += 2
    else:
        feedback.append("Explain reasoning clearly (use 'because').")

    return score, feedback
