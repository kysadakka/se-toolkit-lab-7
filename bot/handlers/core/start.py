"""Handler for /start command."""


def handle_start(user_input: str = "") -> str:
    """Handle the /start command.
    
    Args:
        user_input: The raw user input (ignored for /start)
        
    Returns:
        Welcome message text
    """
    return (
        "👋 Welcome to the SE Toolkit Bot!\n\n"
        "I can help you with:\n"
        "• Viewing your lab scores\n"
        "• Checking course information\n"
        "• Getting help with assignments\n\n"
        "Use /help to see all available commands."
    )
