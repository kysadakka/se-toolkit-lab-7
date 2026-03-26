"""Handler for /scores command."""

import sys
from pathlib import Path

# Add bot directory to path for imports when running as script
bot_dir = Path(__file__).parent.parent
if str(bot_dir) not in sys.path:
    sys.path.insert(0, str(bot_dir))

from services.lms_client import client


def handle_scores(user_input: str = "") -> str:
    """Handle the /scores command.
    
    Args:
        user_input: The raw user input, should contain lab name like "lab-04"
        
    Returns:
        Pass rates for the specified lab
    """
    # Extract lab name from input (remove command and whitespace)
    parts = user_input.strip().split()
    lab_id = parts[1] if len(parts) > 1 else ""
    
    if not lab_id:
        return "❌ Please specify a lab: `/scores lab-04`"
    
    try:
        rates = client.get_pass_rates(lab_id)
        
        if not rates:
            return f"📊 No score data found for {lab_id}."
        
        result = f"📊 **Pass rates for {lab_id}:**\n\n"
        for task in rates:
            task_name = task.get('task', 'Unknown')
            avg_score = task.get('avg_score', 0)
            attempts = task.get('attempts', 0)
            result += f"• {task_name}: {avg_score}% ({attempts} attempts)\n"
        return result
    except Exception as e:
        return f"❌ Failed to fetch scores for {lab_id}: {str(e)}"