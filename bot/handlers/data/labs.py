"""Handler for /labs command."""

import sys
from pathlib import Path

# Add bot directory to path for imports when running as script
bot_dir = Path(__file__).parent.parent
if str(bot_dir) not in sys.path:
    sys.path.insert(0, str(bot_dir))

from services.lms_client import client


def handle_labs(user_input: str = "") -> str:
    """Handle the /labs command.
    
    Args:
        user_input: The raw user input (ignored for /labs)
        
    Returns:
        List of available labs
    """
    try:
        items = client.get_items()
        
        # Filter items where type is 'lab' (adjust based on your API response)
        labs = [item for item in items if item.get('type') == 'lab']
        
        if not labs:
            return "No labs found in the system."
        
        result = "📋 **Available Labs:**\n\n"
        for lab in labs:
            result += f"• {lab.get('title', 'Unknown')}\n"
        return result
    except Exception as e:
        return f"❌ Failed to fetch labs: {str(e)}"