"""
Setup verification script for Day 1 Assessment.
Verifies:
1. Python environment and required modules (openai, python-dotenv).
2. Presence of GROQ_API_KEY.
3. Live Groq API connection and model response.
"""

import sys
import os

print("=" * 60)
print("DAY 1 ASSESSMENT - SETUP CHECK")
print("=" * 60)

# 1. Verify Python Version
print(f"[1/4] Python Version: {sys.version.split()[0]} ... OK")

# 2. Verify Dependencies
print("[2/4] Checking Python packages (openai, python-dotenv)...")
missing_pkgs = []
try:
    import openai
except ImportError:
    missing_pkgs.append("openai")

try:
    import dotenv
except ImportError:
    missing_pkgs.append("python-dotenv")

if missing_pkgs:
    print(f"      ERROR: Missing package(s): {', '.join(missing_pkgs)}")
    print("      Please run: pip install -r requirements.txt")
    sys.exit(1)
print("      Packages installed successfully ... OK")

# 3. Verify Environment Variables & Configuration
print("[3/4] Checking configuration and GROQ_API_KEY...")
try:
    from config import get_groq_client, MODEL, GROQ_BASE_URL
except Exception as e:
    print(f"      ERROR loading config.py: {e}")
    sys.exit(1)

api_key = os.getenv("GROQ_API_KEY")
if not api_key or not api_key.strip():
    print("      ERROR: GROQ_API_KEY is not set.")
    print("      To fix this:")
    print("      1. Create a .env file in the assessment_day_1/ directory.")
    print("      2. Add: GROQ_API_KEY=your_actual_groq_api_key")
    print("      3. (Optional) Add: MODEL=llama-3.3-70b-versatile")
    sys.exit(1)

# Mask key for secure display
masked_key = api_key[:4] + "..." + api_key[-4:] if len(api_key) > 8 else "***"
print(f"      GROQ_API_KEY detected ({masked_key}) ... OK")
print(f"      Base URL: {GROQ_BASE_URL}")
print(f"      Target Model: {MODEL}")

# 4. Test Live Connection to Groq
print("[4/4] Testing live connection to Groq API...")
try:
    client = get_groq_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "Hello! Reply with the single word 'READY' if you can read this."}
        ],
        max_tokens=20,
    )
    reply_text = response.choices[0].message.content.strip()
    print(f"      Groq response: \"{reply_text}\"")
    print("\n" + "=" * 60)
    print("SUCCESS: Environment and Groq API connection are fully verified!")
    print("=" * 60)
except Exception as e:
    print(f"      ERROR during API call: {e}")
    print("\nPlease verify your GROQ_API_KEY and network connectivity.")
    sys.exit(1)
