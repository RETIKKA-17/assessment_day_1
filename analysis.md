# Day 1 Assessment
## Comparing a Plain Chatbot, a Rule-Based Workflow, and an AI Agent

## 1. Scenario

In modern enterprise and educational architectures, software systems frequently interact with domain-specific, proprietary, and confidential datasets that reside behind organizational firewalls. In this assessment, we analyze an institutional private course-fee environment for an academic department. The institution maintains an internal schedule of tuition rates across three core academic courses:

- **CS101** = Rs. 12,000
- **AI202** = Rs. 18,000
- **DS303** = Rs. 15,000

This fee information is strictly private and localized. It is stored directly within an internal Python data dictionary (`COURSE_FEES`) rather than in public web domains or public training datasets. Large Language Models (LLMs) trained on general internet corpora possess no foundational knowledge of these specific institutional rates. Assuming that a public or foundation model inherently knows these private numbers constitutes a serious architectural flaw. 

To rigorously benchmark how different software architectures manage this private data, four standardized test questions and one unprogrammed challenge question are evaluated across all systems:

1. **Question 1 (Direct Retrieval):** *"What is the fee for AI202?"* (Ground Truth: Rs. 18,000)
2. **Question 2 (Multi-Step Calculation with Discount):** *"What is the total fee for CS101 and AI202 after a 10% scholarship?"* (Ground Truth: Rs. 27,000)
3. **Question 3 (Comparative Arithmetic):** *"Is DS303 more expensive than CS101, and by how much?"* (Ground Truth: Yes, by Rs. 3,000)
4. **Question 4 (Creative Language Generation):** *"Write a two-line welcome message for new AI students."* (Ground Truth: A contextual, two-line welcoming message)
5. **Challenge Question (Budget Optimization & Unprogrammed Pairing):** *"I can pay Rs. 30,000. Which two courses can I take together within this budget?"* (Ground Truth: CS101 + DS303 = Rs. 27,000, as taking CS101 and AI202 totals Rs. 30,000, but pairing CS101 and DS303 comfortably satisfies the budget with a remainder).

---

## 2. Plain Chatbot

The Plain Chatbot architecture relies entirely on an isolated Large Language Model (in this implementation, Groq's high-speed inference engine accessing `llama-3.3-70b-versatile`). When an inquiry arrives, the user's prompt is dispatched directly to the LLM via its completion API without augmenting the context with institutional data or granting access to external callable functions.

Because the system prompt deliberately withholds the private `COURSE_FEES` dictionary and provides no tool-calling capability, the LLM must rely solely on its static pre-trained weights. When confronted with queries regarding private course numbers, an LLM exhibits one of two behaviors:
1. **Hallucination:** It may invent an arbitrary or plausible-sounding monetary figure based on probabilistic token associations, producing an incorrect, misleading answer with high semantic confidence.
2. **Epistemic Abstention:** A well-aligned or instruction-tuned model may acknowledge that it lacks access to internal or proprietary college fee schedules and decline to quote a definitive price.

In contrast, when presented with general language-generation tasks—such as Question 4's request for an encouraging two-line welcome message for incoming artificial intelligence students—the plain chatbot excels. Natural language fluency, stylistic tone adaptation, and creative synthesis are native competencies of foundation models.

The primary architectural limitation of the Plain Chatbot in this scenario is its epistemic boundary: it cannot inspect, query, verify, or calculate private numbers. Without integration into an external environment, raw LLMs cannot serve as reliable back-office systems for private institutional records.

---

## 3. Rule-Based Workflow

The Rule-Based Workflow represents the traditional software engineering approach to deterministic business logic. It operates entirely without machine learning models, semantic embeddings, or LLM inference. Instead, the workflow consists of explicit Python code, conditional `if/else` logic, and regular expression pattern matchers that directly access the in-memory `COURSE_FEES` dictionary.

When an incoming query strictly adheres to pre-programmed linguistic syntax, the rule-based workflow delivers flawless, instantaneous, and deterministic precision:
- For Question 1, detecting the pattern `fee for <course>` immediately pulls `AI202` from `COURSE_FEES` and outputs `Rs. 18,000`.
- For Question 2, encountering the `scholarship` trigger extracts the recognized course codes, sums their fees, computes the 10% deduction, and returns `Rs. 27,000`.
- For Question 3, evaluating `more expensive than` calculates the mathematical difference between `DS303` (15,000) and `CS101` (12,000) and returns `Yes, by Rs. 3,000`.

However, the defining limitation of the Rule-Based Workflow is its absolute rigidity and zero semantic understanding. If a human user phrases Question 1 naturally as *"Could you tell me how much I need to pay for enrollment in AI202?"*, the regex parser fails to match the hardcoded pattern `fee (?:for|of)`, collapsing into an unhandled rule error despite the data being present in memory. Furthermore, for Question 4 (writing a creative welcome message), the rule system is fundamentally incapable of generating novel human language, returning a rigid error indicating that text composition is unsupported. The workflow cannot adapt to unseen permutations or complex multi-variable objectives without software engineers writing new code for every edge case.

---

## 4. AI Agent

The AI Agent embodies the modern autonomous paradigm: **Agent = LLM + Tools + Loop**. Rather than treating the LLM as an isolated oracle or relying on brittle deterministic rules, the agent architecture couples the semantic reasoning capacity of the LLM with executable Python tools mediated by a dynamic execution loop.

In our implementation, the agent has access to two explicit Python functions:
1. `get_course_fee(course_code)`: A tool that queries the private `COURSE_FEES` dictionary.
2. `calculator(expression)`: A safe arithmetic evaluator implemented via Python's Abstract Syntax Tree (`ast`) module that prohibits dangerous `eval()` execution.

The iterative agent loop operates through a disciplined cyclical state machine:
```
User Query Received
       ↓
Groq LLM Reasoning
       ↓
Tool Selection (LLM chooses tool & formats JSON arguments)
       ↓
Tool Execution (Python executes function safely in local runtime)
       ↓
Observation (Output string returned to LLM as role: 'tool')
       ↓
Another Decision (LLM checks if more data/math is required)
       ↓
Final Answer Generated (LLM delivers grounded response to user)
```

For Question 2, the agent does not guess the fees or attempt mental arithmetic. Instead, the LLM emits a tool call for `get_course_fee('CS101')`, receives `12000`, emits a second tool call for `get_course_fee('AI202')`, receives `18000`, and then emits a tool call to `calculator('(12000 + 18000) * 0.9')`, receiving `27000`. Only after receiving these observations does it formulate its final natural-language response.

Crucially, the agent exhibits adaptive restraint. When presented with Question 4 (the creative welcome message), the LLM recognizes that no institutional fee lookup or mathematical calculation is necessary. It bypasses tool invocations entirely and generates the welcome message directly. The agent architecture successfully bridges natural language comprehension, dynamic decision-making, and verifiable mathematical accuracy without exposing internal reasoning traces.

---

## 5. Comparison Table

| Basis for comparison | Plain chatbot | Rule-based workflow | AI agent |
|---|---|---|---|
| **Flexibility** | High conversational flexibility; easily handles diverse phrasing and creative writing, but cannot inspect private state. | Extremely low; fails immediately when query syntax deviates from programmed regex or when creative composition is requested. | Very high; seamlessly interprets varied natural language phrasing while dynamically selecting appropriate programmatic actions. |
| **Decision-making** | Probabilistic next-token prediction; lacks goal-directed planning or the ability to choose programmatic subroutines. | Deterministic and rigid; follows hardcoded decision trees and cannot make autonomous deductions on unseen scenarios. | Dynamic and deliberate; decides whether external information is required, which tool to call, and when the goal has been satisfied. |
| **Tool usage** | Zero tool usage; cannot execute code, query APIs, perform calculations, or interact with external runtime environments. | Implicit tool execution only via fixed procedural routines; lacks runtime tool selection or schema-driven invocation. | Explicit, schema-driven tool usage; selects and executes `get_course_fee` and `calculator` based on real-time task needs. |
| **Private-data access** | No access; private dictionary is excluded from prompt context, leading to abstention or factual hallucination. | Direct access; can read the local `COURSE_FEES` dictionary directly through static variable references. | Mediated access; securely queries private `COURSE_FEES` exclusively through controlled `get_course_fee` tool calls. |
| **Multi-step task handling** | Poor; prone to cascading arithmetic errors or fabricating missing steps when computing complex multi-tier discounts. | Moderate for pre-programmed paths; executes step-by-step logic flawlessly only if the exact sequence was hardcoded beforehand. | Superior; autonomously breaks complex queries into iterative steps (retrieval &rarr; intermediate calculation &rarr; final synthesis). |
| **Automation** | Limited to automated text generation; cannot automate end-to-end operational workflows involving live computations. | High for narrow, static operations; reliably automates fixed lookups without human intervention or token overhead. | High and generalized; automates dynamic multi-tool workflows across both structured calculations and unstructured user dialogues. |
| **Reliability** | Unreliable for institutional facts and arithmetic; output cannot be trusted without manual external verification. | Highly reliable for exact matching cases, but completely unreliable when inputs vary or novel requirements emerge. | Highly reliable; combines verifiable factual grounding from tools with the contextual robustness of modern language models. |

---

## 6. Results

The three systems were tested against the standardized test suite and the unprogrammed challenge question. Below is a detailed discussion of the observed behaviors across all questions:

### Question 1: *"What is the fee for AI202?"*
- **Plain Chatbot:** Lacking access to internal records, the chatbot either hallucinated an arbitrary tuition fee or politely stated that it did not possess the internal fee structure of the institution.
- **Rule-Based Workflow:** Successfully intercepted the keyword pattern `fee for AI202`, looked up the key in `COURSE_FEES`, and returned `Rs. 18,000`.
- **AI Agent:** Recognized that private data was required, generated a tool call to `get_course_fee(course_code='AI202')`, received the observation `18000`, and synthesized a verified final response of `Rs. 18,000`.

### Question 2: *"What is the total fee for CS101 and AI202 after a 10% scholarship?"*
- **Plain Chatbot:** Unable to obtain ground-truth figures, it either guessed random figures and produced erroneous math or stated an inability to calculate private scholarship rates.
- **Rule-Based Workflow:** Successfully matched the programmed scholarship rule, extracted both course identifiers, computed `(12000 + 18000) * 0.9`, and returned `Rs. 27,000`.
- **AI Agent:** Systematically broke the inquiry into three observable tool calls: fetched `CS101` (12,000), fetched `AI202` (18,000), submitted the discounted arithmetic string to `calculator`, and accurately returned `Rs. 27,000`.

### Question 3: *"Is DS303 more expensive than CS101, and by how much?"*
- **Plain Chatbot:** Guessed relationships without basis or declined to compare private course catalogs.
- **Rule-Based Workflow:** Matched the comparison regex, computed `15000 - 12000`, and correctly answered `Yes, by Rs. 3,000`.
- **AI Agent:** Called `get_course_fee('DS303')` (15,000), called `get_course_fee('CS101')` (12,000), executed `calculator('15000 - 12000')` (3,000), and delivered a verified comparative answer confirming DS303 is more expensive by Rs. 3,000.

### Question 4: *"Write a two-line welcome message for new AI students."*
- **Plain Chatbot:** Succeeded effortlessly, outputting an inspiring, high-quality two-line welcome greeting.
- **Rule-Based Workflow:** Failed completely, outputting `[RULE ERROR] Unsupported query: Rule-based systems cannot generate creative natural language text.`
- **AI Agent:** Recognized that this task required pure linguistic creativity without fee data or math. It executed zero tool calls and produced a tailored two-line welcome message immediately.

### Challenge Question: *"I can pay Rs. 30,000. Which two courses can I take together within this budget?"*
- **Plain Chatbot:** Hallucinated combinations or gave generic financial planning advice without grounding in the real catalog.
- **Rule-Based Workflow:** Crashed into its fallback handler (`[RULE ERROR] Unrecognized query format. No matching programmed rule found.`) because budget-constrained combinatorial pairing was never explicitly coded into its `if/else` logic.
- **AI Agent:** Demonstrated autonomous multi-step reasoning. It retrieved the necessary fees across the course catalog, tested potential pairs via calculation, determined that CS101 (Rs. 12,000) + DS303 (Rs. 15,000) equals Rs. 27,000 (well within the Rs. 30,000 ceiling), and clearly explained the recommended enrollment pair to the user.

---

## 7. Suitability Analysis

When assessing which architectural approach is most suitable for this private course-fee environment, the **AI Agent** emerges as the superior comprehensive solution, but key engineering trade-offs must be acknowledged.

### Evaluation by Architecture Criteria:
- **Flexibility:** The AI Agent handles varied human conversational inputs, handles spelling variations, and parses complex intent without requiring rigid syntax.
- **Decision-Making:** The agent autonomously determines whether an action requires institutional retrieval, numerical computation, or simple conversational response.
- **Tool Usage:** Encapsulating sensitive capabilities inside discrete, typed tools ensures modularity and safety.
- **Private-Data Access:** Sensitive databases remain secure behind functional interfaces; private data is provided to the LLM solely on demand for the active context rather than baked into permanent model weights.
- **Multi-Step Task Handling:** The agent handles non-trivial compound logic (such as searching, filtering, and budget matching) through an iterative loop.
- **Automation & Reliability:** By offloading arithmetic to a deterministic AST calculator and institutional facts to a verified lookup function, the agent eliminates hallucination while preserving end-to-end conversational automation.

### Architectural Trade-Offs:
1. **Computational Cost & Latency:** While a rule-based script executes in microseconds with negligible CPU cycles, the AI Agent requires multiple LLM inference calls across its iterative loop, introducing network latency and API token costs.
2. **Deterministic Guarantees:** A rule-based system guarantees 100% deterministic behavior for its supported subset. In mission-critical environments where variations in wording cannot be tolerated and queries are rigidly formatted (e.g., standard protocol decoders), rule-based pipelines offer zero variance.
3. **Engineering Overhead:** Building robust agents requires strict schema definitions, safe execution sandboxes (e.g., forbidding `eval()`), and loop termination guardrails.

Therefore, the AI Agent is optimal when user interactions are open-ended, multi-step, and require both conversational flexibility and access to private operational backends.

---

## 8. Conclusion

Each of the three architectural paradigms occupies a distinct and valuable role in real-world software engineering:

### 1. Plain Chatbot
Appropriate when the application primarily requires open-ended natural language generation, summarization, brainstorming, tone transformation, or general educational Q&A where private real-time data and strict arithmetic precision are not required.
*Real-World Examples:* Creative copywriting assistants, general language translators, customer service chatbots providing general FAQ responses, and brainstorming partners.

### 2. Rule-Based Workflow
Appropriate when the domain problem is completely bounded, strictly structured, predictable, and requires zero-latency, deterministic execution with zero tolerance for probabilistic variance.
*Real-World Examples:* Fixed compliance validation engines, payroll tax bracket calculators, transactional banking debit/credit processors, and data transformation ETL pipelines with rigid schemas.

### 3. AI Agent
Appropriate when real-world tasks demand dynamic reasoning, multi-turn decision-making, access to private or mutable enterprise databases, and the ability to combine discrete software tools to solve novel or multi-step challenges.
*Real-World Examples:* Enterprise customer support agents resolving warranty claims, automated financial portfolio rebalancing assistants, intelligent travel itinerary planners with live flight/hotel APIs, and autonomous DevOps remediation bots diagnosing production outages.

---

## 9. Agent Tool Trace

Below is the observable tool execution trace generated by System 3 (AI Agent) when answering Question 2:
*"What is the total fee for CS101 and AI202 after a 10% scholarship?"*

```text
Observable Tool Trace:
step 1: get_course_fee({'course_code': 'CS101'}) -> 12000
step 2: get_course_fee({'course_code': 'AI202'}) -> 18000
step 3: calculator({'expression': '(12000 + 18000) * 0.9'}) -> 27000
```

### Demonstration of Core Concept: `Agent = LLM + Tools + Loop`

1. **LLM (Reasoning Engine):** The Groq LLM reads the user prompt, determines that `CS101` and `AI202` are specific course codes whose fees are unknown, and formulates a structured request to call the `get_course_fee` tool for `CS101`.
2. **Tools (Deterministic Capabilities):** Python executes `get_course_fee('CS101')` against the private `COURSE_FEES` dictionary and safely returns `12000`. The model receives this observation and immediately invokes `get_course_fee('AI202')`, yielding `18000`.
3. **Loop (Iterative State Machine):** The agent loop feeds each tool observation back into the dialogue context as a `tool` role message. Seeing both fees in its context, the LLM determines that the final answer requires a 10% scholarship calculation. Rather than risking arithmetic hallucination, the loop executes a third iteration using `calculator('(12000 + 18000) * 0.9')`, returning `27000`.
4. **Final Synthesis:** With all factual observations collected, the LLM terminates the tool-calling loop and generates the verified final answer: *"The total fee for CS101 and AI202 after a 10% scholarship is Rs. 27,000."*

No hidden internal thoughts or chain-of-thought tokens are leaked; only observable, verified tool transactions are recorded.

---

## 10. How to Run

Follow these instructions to set up the environment and run the assessment scripts locally on Windows:

### Step 1: Create and Activate Virtual Environment
Open PowerShell inside the `assessment_day_1` directory:
```powershell
# Navigate into the assessment directory
cd assessment_day_1

# Create the Python virtual environment
python -m venv .venv

# Activate the virtual environment on Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# (If using Windows Command Prompt, run: .\.venv\Scripts\activate.bat)
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables (.env)
Create a `.env` file inside the `assessment_day_1/` directory.

> [!CAUTION]
> **CRITICAL SECURITY REQUIREMENT:**
> The `.env` file contains your private `GROQ_API_KEY`. It must **NEVER** be committed or pushed to GitHub. The project's `.gitignore` is already pre-configured to strictly ignore `.env` files.

Inside `assessment_day_1/.env`, add:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
MODEL=llama-3.3-70b-versatile
```

### Step 4: Verify Environment Setup
```powershell
python check_setup.py
```
This script validates your Python environment, verifies dependencies, confirms the presence of `GROQ_API_KEY`, and sends a live ping test to the Groq API.

### Step 5: Run the System Scripts
Execute each system script to observe their respective outputs:
```powershell
# Run System 1: Plain Chatbot (shows limitation on private data)
python chatbot.py

# Run System 2: Rule-Based Workflow (shows deterministic rules & fragility)
python workflow.py

# Run System 3: AI Agent (shows LLM + Tools + Loop in action)
python agent.py

# Run Challenge Comparison (shows Workflow failure vs. Agent success on unprogrammed budget pairing)
python challenge.py
```
