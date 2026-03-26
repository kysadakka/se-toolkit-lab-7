"""Configuration loading from environment variables."""

import os
from pathlib import Path
from dotenv import load_dotenv


def load_config() -> dict[str, str]:
    """Load configuration from environment variables.
    
    Looks for .env.bot.secret in production, falls back to .env.bot.example.
    Returns a dictionary with all configuration values.
    """
    # Determine the bot directory (where this config.py file is located)
    bot_dir = Path(__file__).parent.resolve()
    
    # Try to load from .env.bot.secret first (production), then .env.bot.example
    secret_env = bot_dir / ".env.bot.secret"
    example_env = bot_dir / ".env.bot.example"
    
    if secret_env.exists():
        load_dotenv(secret_env)
    elif example_env.exists():
        load_dotenv(example_env)
    
    return {
        "BOT_TOKEN": os.getenv("BOT_TOKEN", ""),
        "LMS_API_URL": os.getenv("LMS_API_URL", "http://localhost:42002"),
        "LMS_API_KEY": os.getenv("LMS_API_KEY", ""),
        "LLM_API_KEY": os.getenv("LLM_API_KEY", ""),
        "LLM_API_BASE_URL": os.getenv("LLM_API_BASE_URL", "http://localhost:42005/v1"),
        "LLM_API_MODEL": os.getenv("LLM_API_MODEL", "coder-model"),
    }

_config = load_config()

BOT_TOKEN = _config["BOT_TOKEN"]
LMS_API_URL = _config["LMS_API_URL"]
LMS_API_KEY = _config["LMS_API_KEY"]
LLM_API_KEY = _config["LLM_API_KEY"]
LLM_API_BASE_URL = _config["LLM_API_BASE_URL"]
LLM_API_MODEL = _config["LLM_API_MODEL"]