"""Handler for /labs command."""

import sys
from pathlib import Path

bot_dir = Path(__file__).parent.parent
if str(bot_dir) not in sys.path:
    sys.path.insert(0, str(bot_dir))

from services.lms_client import client


def handle_labs(user_input: str = "") -> str:
    """Handle the /labs command."""
    try:
        items = client.get_items()
        labs = [item for item in items if item.get('type') == 'lab']
        
        if not labs:
            return "No labs found in the system."
        
        result = "📋 **Available Labs:**\n\n"
        for lab in labs:
            result += f"• {lab.get('title', 'Unknown')}\n"
        return result
    except Exception as e:
        return f"❌ Failed to fetch labs: {str(e)}"