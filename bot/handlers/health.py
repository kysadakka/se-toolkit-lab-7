"""Handler for /health command."""

import sys
from pathlib import Path

# Add bot directory to path for imports when running as script
bot_dir = Path(__file__).parent.parent
if str(bot_dir) not in sys.path:
    sys.path.insert(0, str(bot_dir))

from config import load_config


def handle_health(user_input: str = "") -> str:
    """Handle the /health command.
    
    Args:
        user_input: The raw user input (ignored for /health)
        
    Returns:
        Health status text
    """
    config = load_config()
    
    # For now, return a simple status message
    # Task 2 will implement actual backend health checks
    lms_url = config.get("LMS_API_URL", "not configured")
    
    return (
        "✅ Bot is running\n"
        f"📡 LMS API URL: {lms_url}\n"
        "ℹ️ Backend health check will be implemented in Task 2"
    )
