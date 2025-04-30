import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")

# Raise an error if the API key is missing
if not HF_API_KEY:
    raise ValueError("❌ HF_API_KEY not found in the .env file!")

def style_prompt(user_prompt, style=None, mode="chat", lang="en"):
    # Quote mode returns a short meaningful quote in the selected language
    if mode == "quote":
        return (
            f"Write a meaningful and short quote about: '{user_prompt}'." if lang == "en"
            else f"Mövzu haqqında mənalı və qısa bir sitat yaz: '{user_prompt}'."
        )

    # Predefined prompt styles for different personalities or tones
    styles = {
        "kid": f"Imagine you're a 7-year-old kid. Explain it in a fun and simple way: {user_prompt}",
        "teacher": f"Explain like a high school physics teacher: {user_prompt}",
        "pirate": f"Talk like a pirate and explain: {user_prompt}",
        "poet": f"Write a short emotional poem about: {user_prompt}",
        "scientist": f"Explain scientifically and clearly: {user_prompt}",
        "robot": f"Respond like a logical robot with no emotions: {user_prompt}",
        "storyteller": f"Turn this into a short creative story: {user_prompt}",
        "programmer": f"Explain this to a beginner programmer: {user_prompt}",
        "philosopher": f"Analyze this deeply like a philosopher: {user_prompt}",
        "journalist": f"Summarize the topic like a news article: {user_prompt}",
        "comedian": f"Be funny like a stand-up comedian while explaining: {user_prompt}",
    }

    # Return the styled prompt or fallback to original
    return styles.get(style, user_prompt)

def hf_response(prompt, style=None, mode="chat", lang="en"):
    # Format the prompt according to style and language
    styled_prompt = style_prompt(prompt, style, mode, lang)

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": styled_prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.5
        }
    }

    try:
        # Send POST request to Hugging Face Inference API
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-base",
            headers=headers,
            json=payload,
            timeout=20
        )
        result = response.json()

        # Handle different possible response formats
        if isinstance(result, list):
            return result[0].get("generated_text", "⚠️ Empty response received.")
        elif isinstance(result, dict) and "generated_text" in result:
            return result["generated_text"]
        elif "error" in result:
            return f"❌ AI error: {result['error']}"
        else:
            return "⚠️ Unexpected response received."

    except requests.exceptions.Timeout:
        return "❌ Connection timed out."
    except Exception as e:
        return f"❌ Exception occurred: {str(e)}"