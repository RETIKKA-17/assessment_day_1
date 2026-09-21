"""
SYSTEM 3: AI AGENT
Demonstrates: Agent = LLM + Tools + Loop
- Uses Groq LLM as the reasoning engine.
- Integrates Python tools: get_course_fee (for private data) and calculator (safe AST math).
- Runs an iterative execution loop:
    1. LLM evaluates the state and chooses whether to call a tool or reply.
    2. Python executes the chosen tool and captures the observation.
    3. The observation is sent back to the LLM.
    4. The loop continues until a final answer is synthesized.
- Observable trace is printed (step N: tool(args) -> result).
- No hidden chain-of-thought is displayed.
"""

import json
import sys
from config import get_groq_client, MODEL
from tools import TOOLS, execute_tool

QUESTIONS = [
    "What is the fee for AI202?",
    "What is the total fee for CS101 and AI202 after a 10% scholarship?",
    "Is DS303 more expensive than CS101, and by how much?",
    "Write a two-line welcome message for new AI students."
]

AGENT_SYSTEM_PROMPT = (
    "You are an intelligent college advisory AI Agent. You have access to tools:\n"
    "1. get_course_fee: Retrieve the official private course fee (e.g. CS101, AI202, DS303).\n"
    "2. calculator: Perform exact arithmetic calculations (sums, discounts, differences).\n\n"
    "STRICT GUIDELINES:\n"
    "- You must NEVER guess or fabricate course fees. Always use get_course_fee for course fee information.\n"
    "- Always use the calculator tool for arithmetic (such as applying scholarships or calculating differences).\n"
    "- If a query is a general text request (e.g. writing a welcome message) and requires NO private fee lookup or calculation, do NOT call any tools; respond directly."
)


def run_agent_loop(client, question: str, max_iterations: int = 8) -> str:
    """
    Executes the Agent loop: LLM -> Tool Call -> Tool Execution -> Observation -> Next Decision.
    """
    messages = [
        {"role": "system", "content": AGENT_SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    step_counter = 1
    has_printed_trace_header = False

    for _ in range(max_iterations):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.0,
        )

        message = response.choices[0].message

        # Check if the LLM decided to invoke any tools
        if message.tool_calls:
            if not has_printed_trace_header:
                print("Observable Tool Trace:")
                has_printed_trace_header = True

            # Append the assistant's tool-call request to dialogue history
            messages.append(message)

            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                try:
                    func_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    func_args = {}

                # Execute tool using Python
                tool_output = execute_tool(func_name, func_args)

                # Print observable trace: step N: func_name(args) -> result
                print(f"step {step_counter}: {func_name}({func_args}) -> {tool_output}")
                step_counter += 1

                # Send observation back to the LLM
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": func_name,
                    "content": str(tool_output),
                })
        else:
            # LLM concluded reasoning and produced the final answer
            if not has_printed_trace_header:
                print("Observable Tool Trace: (None - direct language response)")
            final_content = message.content or ""
            return final_content.strip()

    return "Agent Error: Exceeded maximum iterations without reaching final answer."


def run_agent():
    print("=" * 60)
    print("SYSTEM 3: AI AGENT")
    print("=" * 60)
    print("Properties: LLM + Tools + Loop.")
    print("Reasoning engine (Groq) dynamically invokes Python tools.\n")

    try:
        client = get_groq_client()
    except RuntimeError as err:
        print(f"Cannot initialize Agent: {err}")
        return

    for i, question in enumerate(QUESTIONS, start=1):
        print(f"Question {i}:")
        print(f"Q: {question}")
        try:
            answer = run_agent_loop(client, question)
            print(f"A: {answer}\n")
        except Exception as e:
            print(f"A: [Execution Error: {e}]\n")


if __name__ == "__main__":
    run_agent()
