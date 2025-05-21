import os
import logging
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get credentials from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # e.g., "@your_channel" or chat ID number


def send_digest(articles, bot_token=None, chat_id=None):
    """
    Send articles digest to Telegram chat
    
    Args:
        articles (list): List of articles to send, each with 'title', 'link', and 'summary'
        bot_token (str, optional): Telegram bot token. Defaults to environment variable.
        chat_id (str, optional): Telegram chat ID. Defaults to environment variable.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Use provided credentials or fall back to environment variables
        bot_token = bot_token or BOT_TOKEN
        chat_id = chat_id or CHAT_ID
        
        if not bot_token or not chat_id:
            logger.error("Missing Telegram credentials. Set BOT_TOKEN and CHAT_ID in .env file.")
            return False

        bot = Bot(token=bot_token)
        
        for article in articles:
            message = f"{article['title']}\n{article['link']}\n\n{article['summary']}"
            bot.send_message(chat_id=chat_id, text=message)
        
        logger.info(f"Successfully sent {len(articles)} articles to Telegram")
        return True
    
    except TelegramError as e:
        logger.error(f"Telegram error: {e}")
        return False
    except Exception as e:
        logger.error(f"Error sending digest to Telegram: {e}")
        return False


# Example usage
if __name__ == "__main__":
    # This will only run when the file is executed directly
    # For testing purposes, you could include a small example here
    test_articles = [
        {
            "title": "Test Article",
            "link": "https://example.com",
            "summary": "This is a test article to verify the Telegram message functionality."
        }
    ]
    send_digest(test_articles)
