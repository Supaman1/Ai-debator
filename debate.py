from config import THINKER, CODER_A, CODER_B, CODER_C, CODER_D
from router import call_llm

def run_debate_round(user_request: str) -> str:
    """
    Executes a 6-phase debate loop passing state and critiques across the 5 models.
    """
    # -------------------------------------------------------------
    # TURN 1: Thinker (Gemini Flash) - System Architecture & Plan
    # -------------------------------------------------------------
    print("--- [Turn 1/6] Thinker (Gemini): Architecting Plan ---")
    thinker_system = "You are the Lead Systems Architect. Break down the user prompt into modular logic, edge cases, and architectural requirements."
    plan = call_llm(THINKER, thinker_system, user_request)

    # -------------------------------------------------------------
    # TURN 2: Coder A (Llama 3.3 70B) - Initial Code Draft
    # -------------------------------------------------------------
    print("--- [Turn 2/6] Coder A (Llama 3.3): Writing Initial Implementation ---")
    coder_a_system = (
        "You are the Lead Implementation Engineer. Write complete, functional Python code based on the Architect's plan. "
        "Explain your logic briefly, then output all executable code inside a ```python ... ``` block."
    )
    draft_code = call_llm(CODER_A, coder_a_system, f"Architect Plan:\n{plan}")

    # -------------------------------------------------------------
    # TURN 3: Coder B (DeepSeek R1 Distill) - Deep Logic & Edge-Case Review
    # -------------------------------------------------------------
    print("--- [Turn 3/6] Coder B (DeepSeek R1): Analyzing Logic & Edge Cases ---")
    coder_b_system = (
        "You are a Strict Code Auditor & Security Specialist. Analyze Coder A's implementation for logical flaws, "
        "unhandled edge cases, boundary errors, or missing checks. Be critical and list specific fixes."
    )
    security_review = call_llm(CODER_B, coder_b_system, f"Coder A Output:\n{draft_code}")

    # -------------------------------------------------------------
    # TURN 4: Coder C (Qwen 2.5 32B) - Algorithm & Data Structure Optimization
    # -------------------------------------------------------------
    print("--- [Turn 4/6] Coder C (Qwen 2.5): Inspecting Algorithms & Syntax ---")
    coder_c_system = (
        "You are an Algorithm & Data Structures Specialist. Review the code draft and Coder B's critique. "
        "Identify syntax issues, type mismatches, or computational efficiency bottlenecks."
    )
    algo_review = call_llm(CODER_C, coder_c_system, f"Draft Code:\n{draft_code}\n\nSecurity Review:\n{security_review}")

    # -------------------------------------------------------------
    # TURN 5: Coder D (Mistral 7B) - Clean Code & Dynamic Timeout Assignment
    # -------------------------------------------------------------
    print("--- [Turn 5/6] Coder D (Mistral 7B): Refactoring & Setting Dynamic Timeout ---")
    coder_d_system = (
        "You are the Code Optimization Specialist. \n"
        "1. On the FIRST line of your response, output 'TIMEOUT: <seconds>' (e.g. TIMEOUT: 10). Estimate required execution time based on code complexity.\n"
        "2. Refactor the implementation combining the best fixes from Coder B and Coder C.\n"
        "3. Put ALL refactored code inside a ```python ... ``` block."
    )
    optimized_output = call_llm(
        CODER_D, 
        coder_d_system, 
        f"Draft Code:\n{draft_code}\n\nEdge-case Review:\n{security_review}\n\nAlgorithm Review:\n{algo_review}"
    )

    # -------------------------------------------------------------
    # TURN 6: Thinker (Gemini Flash) - Synthesis into Final Candidate Code
    # -------------------------------------------------------------
    print("--- [Turn 6/6] Thinker (Gemini): Merging Final Synthesis ---")
    thinker_synthesis_system = (
        "You are the Synthesizer. Review the full debate log and output the final, polished code. "
        "Keep Mistral's 'TIMEOUT: <seconds>' tag on line 1, and ensure the complete executable Python code is strictly inside a ```python ... ``` block."
    )
    final_synthesis = call_llm(
        THINKER, 
        thinker_synthesis_system, 
        f"Original Draft:\n{draft_code}\n\nRefactored Output & Critiques:\n{optimized_output}"
    )

    return final_synthesis
