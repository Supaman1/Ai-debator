import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Extract API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_KEY")
GROQ_API_KEY = os.getenv("GROQ_KEY")            # Handles Llama 3.3, DeepSeek R1 Distill, and Qwen 2.5
OPENROUTER_API_KEY = os.getenv("OPENROUTER_KEY") # Handles Mistral

# 1. Thinker / Architect
THINKER = {
    "provider": "google",
    "model": "gemini-2.5-flash",
    "api_key": GOOGLE_API_KEY
}

# 2. Coder A (Logic Specialist)
CODER_A = {
    "provider": "groq",
    "model": "llama-3.3-70b-versatile",
    "api_key": GROQ_API_KEY1
}

# 3. Coder B (Deep Reasoning & Edge Cases)
CODER_B = {
    "provider": "groq",
    "model": "deepseek-r1-distill-llama-70b",
    "api_key": GROQ_API_KEY2
}

# 4. Coder C (Algorithms & Syntax)
CODER_C = {
    "provider": "groq",
    "model": "qwen-2.5-32b",
    "api_key": GROQ_API_KEY3
}

# 5. Coder D (Optimization & Dynamic Timeout)
CODER_D = {
    "provider": "openrouter",
    "model": "mistralai/mistral-7b-instruct:free",
    "api_key": OPENROUTER_API_KEY
}
