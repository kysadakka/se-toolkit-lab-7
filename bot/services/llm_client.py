"""LLM client for intent routing."""
import sys
from pathlib import Path

bot_dir = Path(__file__).parent.parent
if str(bot_dir) not in sys.path:
    sys.path.insert(0, str(bot_dir))

from openai import OpenAI
from config import load_config

config = load_config()
LLM_API_KEY = config.get("LLM_API_KEY")
LLM_API_BASE_URL = config.get("LLM_API_BASE_URL", "http://localhost:42005/v1")
LLM_API_MODEL = config.get("LLM_API_MODEL", "coder-model")

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=LLM_API_KEY,
            base_url=LLM_API_BASE_URL
        )
        self.model = LLM_API_MODEL

    def chat(self, messages, tools=None):
        """Send messages to LLM and return response."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto" if tools else None
            )
            return response.choices[0].message
        except Exception as e:
            raise Exception(f"LLM error: {str(e)}")

llm_client = LLMClient()
