"""
Enhanced Groq Neural Client with Structured JSON Extraction and Humanized Reasoning.
"""

import urllib.request
import json
import os
from typing import Dict, Any, List, Optional

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")  # Set via env var or .env. Never commit a real key.
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

class GroqClient:
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or GROQ_API_KEY
        self.model = model or GROQ_MODEL

    def extract_entities(self, query: str) -> List[str]:
        """Extracts normalized clinical and symptom keywords from raw colloquial user input."""
        prompt = f"""
Extract 1 to 3 core medical symptoms, diseases, drugs, or biological targets from this query: "{query}".
Return ONLY a JSON list of short strings (e.g. ["Fever", "Muscle Pain", "Influenza"]).
"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 150
        }
        try:
            req = urllib.request.Request(GROQ_API_URL, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=5) as res:
                if res.status == 200:
                    data = json.loads(res.read().decode("utf-8"))
                    text = data["choices"][0]["message"]["content"].strip()
                    if text.startswith("```"):
                        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
                    parsed = json.loads(text)
                    if isinstance(parsed, list):
                        return parsed
        except Exception as e:
            print(f"[Groq Entity Extractor] Fallback due to: {e}")
        return [query]

    def chat_completion(self, messages: List[Dict[str, str]], temperature: float = 0.3, max_tokens: int = 800) -> Optional[str]:
        """Calls Groq cloud endpoint with high-speed LLaMA 3.3 70B inference."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            req = urllib.request.Request(GROQ_API_URL, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=8) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[Groq Client Warning] Live API call failed: {e}.")
            return None
