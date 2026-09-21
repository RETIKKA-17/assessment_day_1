"""
SYSTEM 1: PLAIN CHATBOT
Demonstrates a standalone LLM without tools or private data access.
- Communicates directly with Groq LLM.
- Does NOT have access to COURSE_FEES.
- Has NO tools or function calling enabled.
- Shows limitations on private data: either produces an incorrect answer (hallucination)
  or explicitly states that it does not know private institutional figures.
- Successfully handles general creative tasks (welcome message).
"""

import sys
from config import get_groq_client, MODEL

QUESTIONS = [
    "What is the fee for AI202?",
    "What is the total fee for CS101 and AI202 after a 10% scholarship?",
    "Is DS303 more expensive than CS101, and by how much?",
    "Write a two-line welcome message for new AI students."
]

SYSTEM_PROMPT = (
    "You are a helpful college assistant. Answer questions concisely and directly. "
    "Note: You do not have access to internal private fee databases unless provided."
)


def run_chatbot():
    print("=" * 60)
    print("SYSTEM 1: PLAIN CHATBOT")
    print("=" * 60)
    print("Properties: Raw LLM without tools or private database access.")
    print("Demonstrates limitation when private data is unavailable.\n")

    try:
        client = get_groq_client()
    except RuntimeError as err:
        print(f"Cannot initialize Chatbot: {err}")
        return

    for i, question in enumerate(QUESTIONS, start=1):
        print(f"Question {i}:")
        print(f"Q: {question}")
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": question}
                ],
                temperature=0.2,
                max_tokens=250,
            )
            answer = response.choices[0].message.content.strip()
            print(f"A: {answer}\n")
        except Exception as e:
            print(f"A: [API Error: {e}]\n")


if __name__ == "__main__":
    run_chatbot()
