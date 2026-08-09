from config import THINKER, CODER_A, CODER_B, CODER_C, CODER_D, CODER_E
from router import call_llm

def run_debate_round(user_request: str) -> str:
    """
    Executes a 7-phase debate loop passing state and critiques across 6 models.
    """
    # TURN 1: Thinker Architect
    print("--- [Turn 1/7] Thinker (Gemini 2.5): Architecting Plan ---")
    plan = call_llm(THINKER, "You are the Lead Systems Architect. Break down the user prompt into modular logic, edge cases, and requirements.", user_request)

    # TURN 2: Coder A (Llama 3.3)
    print("--- [Turn 2/7] Coder A (Llama 3.3): Writing Initial Implementation ---")
    draft_code = call_llm(CODER_A, "You are the Lead Implementation Engineer. Write Python code based on the plan inside a ```python ... ``` block.", f"Architect Plan:\n{plan}")

    # TURN 3: Coder B (DeepSeek R1)
    print("--- [Turn 3/7] Coder B (DeepSeek R1): Analyzing Logic & Edge Cases ---")
    security_review = call_llm(CODER_B, "You are a Strict Code Auditor. Analyze Coder A's implementation for logical flaws, unhandled edge cases, and missing checks.", f"Coder A Output:\n{draft_code}")

    # TURN 4: Coder C (Qwen 2.5)
    print("--- [Turn 4/7] Coder C (Qwen 2.5): Inspecting Algorithms & Syntax ---")
    algo_review = call_llm(CODER_C, "You are an Algorithm Specialist. Review the code draft and Coder B's critique for syntax issues and bottlenecks.", f"Draft Code:\n{draft_code}\n\nSecurity Review:\n{security_review}")

    # TURN 5: Coder D (Gemini 2.0 Flash)
    print("--- [Turn 5/7] Coder D (Gemini 2.0): Cross-Examining Logical Consistency ---")
    google_review = call_llm(CODER_D, "You are a Peer Reviewer. Cross-examine the draft code and previous reviews to verify type safety, standard library usage, and clean execution.", f"Draft Code:\n{draft_code}\n\nCritiques:\n{security_review}\n{algo_review}")

    # TURN 6: Coder E (Mistral 7B)
    print("--- [Turn 6/7] Coder E (Mistral 7B): Refactoring & Setting Dynamic Timeout ---")
    optimized_output = call_llm(
        CODER_E, 
        "Output 'TIMEOUT: <seconds>' on line 1, refactor the code combining all critiques, and place code inside ```python ```.", 
        f"Draft Code:\n{draft_code}\n\nCritiques:\n{security_review}\n{algo_review}\n{google_review}"
    )

    # TURN 7: Thinker Synthesizer
    print("--- [Turn 7/7] Thinker (Gemini 2.5): Merging Final Synthesis ---")
    final_synthesis = call_llm(
        THINKER, 
        "You are the Synthesizer. Output the final polished code. Keep 'TIMEOUT: <seconds>' on line 1, and place code strictly inside ```python ```.", 
        f"Original Draft:\n{draft_code}\n\nRefactored Output & All Critiques:\n{optimized_output}"
    )

    return final_synthesis
    
