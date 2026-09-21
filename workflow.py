"""
SYSTEM 2: RULE-BASED WORKFLOW
Demonstrates deterministic, hardcoded Python if/else logic.
- Directly accesses the private COURSE_FEES data.
- Does NOT use an LLM or machine learning.
- Successfully answers questions that match pre-programmed patterns.
- Rigid and brittle: fails when phrasing changes or when asked creative/generative questions.
"""

import re
from tools import COURSE_FEES

QUESTIONS = [
    "What is the fee for AI202?",
    "What is the total fee for CS101 and AI202 after a 10% scholarship?",
    "Is DS303 more expensive than CS101, and by how much?",
    "Write a two-line welcome message for new AI students."
]


def process_rule_based_workflow(question: str) -> str:
    """
    Processes a question using rigid pattern matching and if/else conditions.
    """
    q_lower = question.lower().strip()

    # Rule 1: Two-course sum with 10% scholarship
    # Specifically checks for multi-course inquiries with scholarship
    if "scholarship" in q_lower or "discount" in q_lower:
        found_courses = [c for c in COURSE_FEES if c.lower() in q_lower]
        if len(found_courses) >= 2:
            subtotal = sum(COURSE_FEES[c] for c in found_courses)
            discounted_total = int(subtotal * 0.9)
            return f"Rs. {discounted_total:,}"
        return "Unable to identify both courses for scholarship calculation."

    # Rule 2: Fee comparison between two courses (e.g., DS303 vs CS101)
    if "more expensive than" in q_lower or "cheaper than" in q_lower:
        match_comp = re.search(r"is ([a-zA-Z]{2}\d{3}) more expensive than ([a-zA-Z]{2}\d{3})", q_lower)
        if match_comp:
            c1 = match_comp.group(1).upper()
            c2 = match_comp.group(2).upper()
            if c1 in COURSE_FEES and c2 in COURSE_FEES:
                diff = COURSE_FEES[c1] - COURSE_FEES[c2]
                if diff > 0:
                    return f"Yes, by Rs. {diff:,}"
                elif diff < 0:
                    return f"No, {c1} is cheaper by Rs. {abs(diff):,}"
                else:
                    return f"No, both courses have the same fee (Rs. {COURSE_FEES[c1]:,})"

    # Rule 3: Single course fee lookup
    # Pattern: "fee for <course>" or "what is the fee of <course>"
    match_single = re.search(r"fee (?:for|of) ([a-zA-Z]{2}\d{3})", q_lower)
    if match_single:
        course = match_single.group(1).upper()
        if course in COURSE_FEES:
            return f"Rs. {COURSE_FEES[course]:,}"
        return f"Course '{course}' not found in fee records."

    # Rule 4: Welcome message generation (Unsupported)
    # The rule engine cannot generate creative natural language
    if "welcome message" in q_lower or "write" in q_lower:
        return "[RULE ERROR] Unsupported query: Rule-based systems cannot generate creative natural language text."

    # Fallback for unprogrammed wording or tasks
    return "[RULE ERROR] Unrecognized query format. No matching programmed rule found."


def run_workflow():
    print("=" * 60)
    print("SYSTEM 2: RULE-BASED WORKFLOW")
    print("=" * 60)
    print("Properties: Uses deterministic if/else Python rules + private dictionary.")
    print("No LLM used. Zero hallucination, but highly rigid and fragile.\n")

    for i, question in enumerate(QUESTIONS, start=1):
        print(f"Question {i}:")
        print(f"Q: {question}")
        answer = process_rule_based_workflow(question)
        print(f"A: {answer}\n")

    # Demonstrate fragility to wording change
    print("-" * 60)
    print("DEMONSTRATION OF RULE RIGIDITY & WORDING FRAGILITY:")
    print("-" * 60)
    rephrased = "Could you tell me how much I need to pay for enrollment in AI202?"
    print(f"Q (Rephrased): {rephrased}")
    rephrased_answer = process_rule_based_workflow(rephrased)
    print(f"A: {rephrased_answer}")
    print("Explanation: The underlying fee data exists, but because the sentence doesn't match")
    print("the hardcoded regex ('fee for <course>'), the rule-based workflow fails completely.\n")


if __name__ == "__main__":
    run_workflow()
