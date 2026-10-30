import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path, override=True)

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
print(f"Key loaded: {api_key[:15] if api_key else 'NONE'}...")

def create_embedding(text: str):
    return [0.0] * 768

def generate_response(user_message: str, context: list = []):
    if not api_key:
        return "API Key not loaded"

    from google import genai
    client = genai.Client(api_key=api_key)

    # 2026 ke naye models - aapke account ke liye
    models_to_try = [
        "gemini-3-flash-preview",
        "gemini-3.8-flash",
        "gemini-3.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-flash-latest",
        "gemini-2.0-flash",
    ]

    for model_name in models_to_try:
        try:
            print(f"Trying {model_name}")
            resp = client.models.generate_content(
                model=model_name,
                contents=user_message
            )
            print(f"SUCCESS with {model_name}!")
            return resp.text
        except Exception as e:
            print(f"{model_name} failed: {str(e)[:300]}")
            continue

    return "All models failed"