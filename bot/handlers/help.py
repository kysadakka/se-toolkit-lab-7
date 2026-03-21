"""Handler for /help command."""


def handle_help(user_input: str = "") -> str:
    """Handle the /help command.
    
    Args:
        user_input: The raw user input (ignored for /help)
        
    Returns:
        Help text with available commands
    """
    return (
        "📚 Available Commands:\n\n"
        "/start - Welcome message\n"
        "/help - Show this help message\n"
        "/health - Check bot and backend status\n"
        "/labs - List available labs\n"
        "/scores [lab] - View your scores for a specific lab\n\n"
        "You can also ask questions in natural language, e.g.:\n"
        "• 'what labs are available?'\n"
        "• 'show my score for lab-04'"
    )
