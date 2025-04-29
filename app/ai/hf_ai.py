import os  # For working with environment variables
import requests  # For sending HTTP requests
from dotenv import load_dotenv  # For loading environment variables from a .env file

# Load environment variables from a .env file
load_dotenv()

# Retrieve the Hugging Face API key from environment variables
HF_API_KEY = os.getenv("HF_API_KEY")

def style_prompt(user_prompt, style=None, mode="chat"):
    """This function customizes the user prompt based on the requested style and mode."""
    
    # For "quote" mode, generate a specific quote request
    if mode == "quote":
        return f"Give a deep, original quote about the topic: '{user_prompt}'. Keep it under 25 words."

    # A dictionary mapping styles to their corresponding prompt structures
    styles = {
        "kid": f"Imagine you're a 7-year-old child who loves asking questions. Explain in a fun and simple way: {user_prompt}",
        "teacher": f"Explain this like a physics teacher to high school students: {user_prompt}",
        "pirate": f"Talk like a pirate and explain: {user_prompt}",
        "poet": f"Write a short, touching poem about: {user_prompt}",
        "scientist": f"Explain scientifically and clearly: {user_prompt}",
        "robot": f"Respond like a logical robot without emotions: {user_prompt}",
        "storyteller": f"Turn this into a creative short story: {user_prompt}",
        "programmer": f"Explain this to a beginner programmer: {user_prompt}",
        "philosopher": f"Analyze this deeply like a philosopher: {user_prompt}",
        "journalist": f"Summarize the topic like a news article: {user_prompt}",
        "comedian": f"Answer with humor like a stand-up comedian: {user_prompt}"
    }

    # Return the customized prompt based on the selected style, or the original user prompt if no style is selected
    return styles.get(style, user_prompt)

def hf_response(prompt, style=None, mode="chat"):
    """This function sends a request to the Hugging Face API to get a response."""
    
    # Prepare the prompt with the requested style and mode
    styled_prompt = style_prompt(prompt, style, mode)

    # Headers for the HTTP request, including the authorization token and content type
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    # The payload to send in the POST request, including the styled prompt and parameters for AI generation
    payload = {
        "inputs": styled_prompt,  # The text prompt for AI
        "parameters": {
            "max_new_tokens": 150,  # Maximum number of tokens in the generated response
            "temperature": 0.7  # Controls randomness of the response (higher = more random)
        }
    }

    # Send the POST request to the Hugging Face API
    response = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-small",  # Hugging Face model endpoint
        headers=headers,
        json=payload
    )

    try:
        # Parse the JSON response from the API
        result = response.json()

        # Check if the response is a list (expected result type)
        if isinstance(result, list):
            return result[0].get("generated_text", "No response generated.")
        # Check if the response contains an error
        elif "error" in result:
            return f"Error from AI: {result['error']}"
        else:
            return "Unexpected AI response."
    except Exception as e:
        # Return an error message if the response could not be parsed
        return f"Parsing error: {e}"