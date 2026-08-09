import os
import sys
from debate import run_debate_round
from sandbox import run_in_sandbox
from router import call_llm
from config import THINKER

MAX_RETRIES = 3

def main():
    print("=" * 60)
    print("  AI MULTI-AGENT DEBATE & EXECUTION ENGINE ACTIVE")
    print("=" * 60 + "\n")

    # Read prompt from GitHub Actions environment variable first, fallback to CLI input
    user_prompt = os.getenv("USER_PROMPT")
    if not user_prompt:
        try:
            user_prompt = input("Enter your coding task or requirement: ")
        except EOFError:
            print("Error: No input provided and running in non-interactive environment.")
            return

    if not user_prompt.strip():
        print("Empty prompt. Exiting.")
        return

    # -------------------------------------------------------------
    # PHASE 1: Run the 6-Model Debate Loop (7 Turns)
    # -------------------------------------------------------------
    print("\n>>> Phase 1: Initiating 6-Model Multi-Agent Debate...")
    code_candidate = run_debate_round(user_prompt)

    # -------------------------------------------------------------
    # PHASE 2: Execution & Automatic Repair Loop
    # -------------------------------------------------------------
    retry_count = 0
    while retry_count < MAX_RETRIES:
        print(f"\n>>> Phase 2: Running Execution Sandbox (Attempt {retry_count + 1}/{MAX_RETRIES})...")
        success, logs = run_in_sandbox(code_candidate)

        if success:
            print("\n" + "=" * 60)
            print("  SUCCESS: Code executed cleanly with zero errors!")
            print("=" * 60)
            print(f"\n--- Console Output / Logs ---\n{logs}")
            print(f"\n--- Final Executable Code ---\n{code_candidate}")
            return
        else:
            print(f"\n[!] Execution Failed or Crashed!")
            print(f"--- Error Traceback ---\n{logs.strip()}")

            retry_count += 1
            if retry_count < MAX_RETRIES:
                print(f"\n>>> Phase 3: Feeding Traceback to Thinker for Auto-Fix (Attempt {retry_count + 1})...")
                
                repair_system_prompt = (
                    "You are the Lead Repair Engineer. Analyze the execution traceback, locate the bug, "
                    "and fix the implementation. Ensure the first line keeps the 'TIMEOUT: <seconds>' tag "
                    "and the entire corrected Python code is strictly inside a ```python ... ``` block."
                )
                
                repair_user_prompt = f"""
The generated code failed inside the execution sandbox.

Original User Task:
{user_prompt}

Failing Response & Code:
{code_candidate}

Sandbox Error Log / Traceback:
{logs}

Instructions: Patch the bug or syntax error, handle the unhandled edge case, and return the fixed Python code block.
"""
                code_candidate = call_llm(
                    THINKER,
                    repair_system_prompt,
                    repair_user_prompt
                )

    print("\n" + "=" * 60)
    print(f"  FAILED: Could not achieve clean execution after {MAX_RETRIES} attempts.")
    print("  Last Error Log:")
    print(logs)
    print("=" * 60)

if __name__ == "__main__":
    main()
    
