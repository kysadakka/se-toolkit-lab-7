"""Handler for /scores command."""


def handle_scores(user_input: str = "") -> str:
    """Handle the /scores command.
    
    Args:
        user_input: The raw user input, may contain lab name (e.g., "/scores lab-04")
        
    Returns:
        Score information text
    """
    # Parse lab name from input if provided
    parts = user_input.strip().split()
    lab_name = parts[1] if len(parts) > 1 else None
    
    if lab_name:
        # Placeholder - Task 2 will fetch from backend
        return (
            f"📊 Scores for {lab_name}:\n\n"
            "Status: Not yet graded\n"
            "Max Points: 100\n"
            "Your Score: --\n\n"
            "Real scores will be fetched from the LMS in Task 2."
        )
    else:
        return (
            "📊 Score Lookup\n\n"
            "Please specify a lab name:\n"
            "  /scores lab-04\n\n"
            "Or ask naturally: 'show my score for lab-04'"
        )
