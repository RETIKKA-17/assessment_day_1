# Assessment Day 1: Plain Chatbot vs. Rule-Based Workflow vs. AI Agent

This repository contains the complete implementation and comparative evaluation for the **Day 1 Assessment**:
*"Comparing a Plain Chatbot, a Rule-Based Workflow, and an AI Agent on a Scenario of Your Own"*

## Core Architecture
- **Core Concept**: `Agent = LLM + Tools + Loop`
- **LLM Provider**: Groq API (`llama-3.3-70b-versatile` via OpenAI-compatible endpoint)
- **Private Data Scenario**: Institutional college course fees (`CS101`: Rs. 12,000, `AI202`: Rs. 18,000, `DS303`: Rs. 15,000)

---

## Systems Implemented

1. **System 1: Plain Chatbot (`chatbot.py`)**
   - Direct LLM inference without tool calling or private data access.
   - Demonstrates epistemic limits and potential hallucinations on private facts while handling creative writing naturally.

2. **System 2: Rule-Based Workflow (`workflow.py`)**
   - Deterministic Python if/else logic accessing local `COURSE_FEES`.
   - Perfectly handles supported queries, but collapses on slight phrasing changes or creative requests.

3. **System 3: AI Agent (`agent.py`)**
   - Autonomous multi-step loop (`LLM + Tools + Loop`).
   - Dynamically selects and executes tools (`get_course_fee`, safe AST `calculator`) and records observable traces.

4. **Challenge Scenario (`challenge.py`)**
   - Evaluates budget-constrained course pairing (`Rs. 30,000` limit).
   - Demonstrates rule-based workflow failure vs. agent autonomous multi-step reasoning.

5. **Detailed Evaluation Report (`analysis.md`)**
   - Complete 10-section comparative analysis covering scenario, systems, full comparison table, results, suitability, conclusion, and tool traces.

---

## Setup & Running

1. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a local `.env` file (strictly excluded by `.gitignore`):
   ```env
   GROQ_API_KEY=your_actual_groq_api_key_here
   MODEL=llama-3.3-70b-versatile
   ```

4. **Verify Setup**:
   ```bash
   python check_setup.py
   ```

5. **Run Systems**:
   ```bash
   python chatbot.py
   python workflow.py
   python agent.py
   python challenge.py
   ```
