"""
CHALLENGE SCRIPT: Comparing Workflow vs. AI Agent on an Unprogrammed Scenario

Question:
"I can pay Rs. 30,000. Which two courses can I take together within this budget?"

Expected Outcome:
- Rule-Based Workflow: Fails immediately because this complex pairing logic was never programmed into its rules.
- AI Agent: Autonomously looks up course fees, computes combination costs using the calculator tool,
  and identifies valid combinations within budget (specifically CS101 + DS303 = Rs. 27,000).
"""

from workflow import process_rule_based_workflow
from agent import run_agent_loop
from config import get_groq_client

CHALLENGE_QUESTION = "I can pay Rs. 30,000. Which two courses can I take together within this budget?"


def run_challenge():
    print("=" * 70)
    print("DAY 1 ASSESSMENT - CHALLENGE QUESTION COMPARISON")
    print("=" * 70)
    print(f"Target Challenge Question:\n\"{CHALLENGE_QUESTION}\"\n")

    # 1. Rule-Based Workflow Attempt
    print("-" * 70)
    print("1. RULE-BASED WORKFLOW EVALUATION:")
    print("-" * 70)
    workflow_answer = process_rule_based_workflow(CHALLENGE_QUESTION)
    print(f"Workflow Answer:\n{workflow_answer}")
    print("\nObservation: The rule-based system fails because its hardcoded pattern")
    print("matching only accounts for single lookups, specific scholarships, and direct comparisons.")
    print("It cannot synthesize combinations or handle budget optimization without new code.\n")

    # 2. AI Agent Attempt
    print("-" * 70)
    print("2. AI AGENT EVALUATION (LLM + Tools + Loop):")
    print("-" * 70)
    try:
        client = get_groq_client()
        agent_answer = run_agent_loop(client, CHALLENGE_QUESTION)
        print(f"\nFinal Agent Answer:\n{agent_answer}")
        print("\nObservation: The agent dynamically queried the course fees, performed arithmetic")
        print("evaluations via the calculator tool, and produced a reasoned answer.")
    except Exception as e:
        print(f"Agent Execution Note: {e}")
        print("To run the AI Agent, ensure GROQ_API_KEY is configured in your .env file.")

    print("=" * 70)


if __name__ == "__main__":
    run_challenge()
