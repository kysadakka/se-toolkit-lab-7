
#!/usr/bin/env python3
"""SE Toolkit Telegram Bot entry point.

Usage:
    uv run bot.py              # Run in Telegram mode (requires BOT_TOKEN)
    uv run bot.py --test "/start"  # Test mode - prints response to stdout
"""

import sys
import argparse
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import load_config
from handlers import (
    handle_start,
    handle_help,
    handle_health,
    handle_labs,
    handle_scores,
)

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def route_command(command: str, user_input: str = "") -> str:
    """Route a command to the appropriate handler.
    
    Args:
        command: The command name (e.g., "start", "help")
        user_input: The full user input string
        
    Returns:
        Response text from the handler
    """
    handlers = {
        "start": handle_start,
        "help": handle_help,
        "health": handle_health,
        "labs": handle_labs,
        "scores": handle_scores,
    }
    
    handler = handlers.get(command)
    if handler:
        return handler(user_input)
    return f"Unknown command: {command}. Use /help for available commands."


def run_test_mode(user_input: str) -> None:
    """Run the bot in test mode - call handlers directly without Telegram.
    
    Args:
        user_input: The input string to process (e.g., "/start" or "what labs are available")
    """
    user_input = user_input.strip()
    
    if not user_input:
        print("Error: No input provided. Usage: bot.py --test <input>")
        sys.exit(1)
    
    # Check if it's a command (starts with /)
    if user_input.startswith("/"):
        # Parse command and arguments
        parts = user_input[1:].split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        response = route_command(command, user_input)
    else:
        # Natural language input - for now, provide a default response
        # Task 3 will implement intent recognition
        response = (
            "🤖 I received your message: \"{}\"\n\n"
            "Natural language processing will be implemented in Task 3.\n"
            "For now, try using commands like /start, /help, /labs, or /scores.".format(user_input)
        )
    
    print(response)
    sys.exit(0)


# Telegram bot handlers
async def telegram_start(update: Update, context) -> None:
    """Telegram handler for /start command."""
    response = handle_start()
    await update.message.reply_text(response)


async def telegram_help(update: Update, context) -> None:
    """Telegram handler for /help command."""
    response = handle_help()
    await update.message.reply_text(response)


async def telegram_health(update: Update, context) -> None:
    """Telegram handler for /health command."""
    response = handle_health()
    await update.message.reply_text(response)


async def telegram_labs(update: Update, context) -> None:
    """Telegram handler for /labs command."""
    response = handle_labs()
    await update.message.reply_text(response)


async def telegram_scores(update: Update, context) -> None:
    """Telegram handler for /scores command."""
    # Get the full message text including arguments
    user_input = update.message.text if update.message else "/scores"
    response = handle_scores(user_input)
    await update.message.reply_text(response)


async def telegram_unknown(update: Update, context) -> None:
    """Handler for unknown commands."""
    response = "Unknown command. Use /help to see available commands."
    await update.message.reply_text(response)


def run_telegram_mode(config: dict) -> None:
    """Run the bot in Telegram mode.
    
    Args:
        config: Configuration dictionary with BOT_TOKEN and other settings
    """
    bot_token = config.get("BOT_TOKEN")
    
    if not bot_token:
        logger.error("BOT_TOKEN not configured. Set it in .env.bot.secret")
        sys.exit(1)
    
    logger.info("Starting bot in Telegram mode...")
    
    # Build the application
    application = Application.builder().token(bot_token).build()
    
    # Register command handlers
    application.add_handler(CommandHandler("start", telegram_start))
    application.add_handler(CommandHandler("help", telegram_help))
    application.add_handler(CommandHandler("health", telegram_health))
    application.add_handler(CommandHandler("labs", telegram_labs))
    application.add_handler(CommandHandler("scores", telegram_scores))
    
    # Handle unknown commands
    application.add_handler(MessageHandler(filters.COMMAND, telegram_unknown))
    
    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="SE Toolkit Telegram Bot")
    parser.add_argument(
        "--test",
        metavar="INPUT",
        help="Test mode: process input and print response to stdout (no Telegram connection)",
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config()
    
    if args.test:
        # Test mode - call handlers directly
        run_test_mode(args.test)
    else:
        # Telegram mode - run the actual bot
        run_telegram_mode(config)


if __name__ == "__main__":
    main()
