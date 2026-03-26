"""Handler for /health command."""

import sys
from pathlib import Path

# Add bot directory to path for imports when running as script
bot_dir = Path(__file__).parent.parent
if str(bot_dir) not in sys.path:
    sys.path.insert(0, str(bot_dir))

from config import load_config
from services.lms_client import client


def handle_health(user_input: str = "") -> str:
    """Handle the /health command.

    Args:
        user_input: The raw user input (ignored for /health)

    Returns:
        Health status text
    """
    try:
        items = client.get_items()
        count = len(items)
        return f"✅ Backend is healthy. {count} items available."
    except Exception as e:
        error_msg = str(e)
        # Remove redundant "Backend error:" prefix if already in message
        if error_msg.startswith("Backend error:"):
            return f"❌ {error_msg}"
        return f"❌ Backend error: {error_msg}"