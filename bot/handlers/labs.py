"""Handler for /labs command."""


def handle_labs(user_input: str = "") -> str:
    """Handle the /labs command.
    
    Args:
        user_input: The raw user input (ignored for /labs)
        
    Returns:
        List of available labs
    """
    # Placeholder - Task 2 will fetch from backend
    return (
        "📋 Available Labs:\n\n"
        "• lab-01: Introduction to Python\n"
        "• lab-02: Data Structures\n"
        "• lab-03: Algorithms\n"
        "• lab-04: Web Development\n"
        "• lab-05: Database Design\n"
        "• lab-06: API Development\n"
        "• lab-07: Bot Integration\n\n"
        "Use /scores [lab-name] to view your score for a specific lab."
    )
