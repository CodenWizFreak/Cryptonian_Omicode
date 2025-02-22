import openai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiChatbot:
    def __init__(self):
        openai.api_key = os.getenv("GEMINI_API_KEY")

    def get_response(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]