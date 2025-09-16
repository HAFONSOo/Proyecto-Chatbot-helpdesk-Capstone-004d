import os
import requests
import json

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"  # ejemplo para OpenAI

def ask_openai(prompt, system="Eres un asistente de helpdesk amable"):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4o-mini",  # ajusta según plan
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 600,
    }
    resp = requests.post(OPENAI_URL, headers=headers, json=data, timeout=15)
    resp.raise_for_status()
    r = resp.json()
    # ajustar según estructura real
    return r["choices"][0]["message"]["content"]
