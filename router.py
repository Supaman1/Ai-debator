import requests

def call_llm(provider_info: dict, system_prompt: str, user_prompt: str) -> str:
    """
    Unified router that receives a provider configuration dictionary from config.py
    and routes the request to Google, Groq, or OpenRouter.
    """
    provider = provider_info["provider"]
    model_name = provider_info["model"]
    api_key = provider_info["api_key"]

    if not api_key:
        return f"[Config Error]: Missing API Key for model '{model_name}' under provider '{provider}'."

    try:
        # --- 1. GOOGLE AI STUDIO ENDPOINT ---
        if provider == "google":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": f"System Context: {system_prompt}\n\nTask: {user_prompt}"}]
                    }
                ]
            }
            res = requests.post(url, json=payload, timeout=30)
            res.raise_for_status()
            data = res.json()
            return data['candidates'][0]['content']['parts'][0]['text']

        # --- 2. GROQ CLOUD ENDPOINT ---
        elif provider == "groq":
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }
            res = requests.post(url, headers=headers, json=payload, timeout=30)
            res.raise_for_status()
            return res.json()['choices'][0]['message']['content']

        # --- 3. OPENROUTER ENDPOINT ---
        elif provider == "openrouter":
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }
            res = requests.post(url, headers=headers, json=payload, timeout=30)
            res.raise_for_status()
            return res.json()['choices'][0]['message']['content']

        else:
            return f"[Router Error]: Unknown provider '{provider}'"

    except Exception as e:
        return f"[API Exception on {model_name}]: {str(e)}"
        
