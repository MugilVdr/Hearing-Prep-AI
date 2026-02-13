import random

def get_question(mode):

    novelty_q = [
        "Which feature distinguishes your claim from D1?",
        "Identify the novel technical element.",
        "Is every element disclosed in prior art?"
    ]

    inventive_q = [
        "Why is this not obvious to a skilled person?",
        "What technical effect arises from your feature?",
        "Why can't D1 be combined with D2?"
    ]

    clarity_q = [
        "What do you mean by 'optimized'?",
        "Is this term measurable?",
        "Is the scope clearly defined?"
    ]

    if mode == "Novelty":
        return random.choice(novelty_q)
    elif mode == "Inventive Step":
        return random.choice(inventive_q)
    else:
        return random.choice(clarity_q)
