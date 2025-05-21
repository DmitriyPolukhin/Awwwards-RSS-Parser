import json
import logging
import os  # Though os might not be strictly necessary, it's good practice to include if dealing with file paths.

from rss_parser import fetch_rss_feed
from telegram_messege import send_digest

# Configuration
RSS_URL = "https://www.awwwards.com/blog/feed/"
SENT_ARTICLES_FILE = "sent_articles.json"

# Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# State Management Functions
def load_sent_articles(filepath: str) -> set:
    """
    Loads the set of sent article links from a JSON file.

    Args:
        filepath: The path to the JSON file.

    Returns:
        A set of article links if the file exists and is valid, otherwise an empty set.
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            return set(data)
    except FileNotFoundError:
        logging.warning(f"Sent articles file '{filepath}' not found. Starting with an empty set.")
        return set()
    except json.JSONDecodeError:
        logging.warning(f"Error decoding JSON from '{filepath}'. Starting with an empty set.")
        return set()
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading sent articles from '{filepath}': {e}")
        return set()

def save_sent_articles(filepath: str, article_links: set):
    """
    Saves the set of article links to a JSON file.

    Args:
        filepath: The path to the JSON file.
        article_links: A set of article links to save.
    """
    try:
        with open(filepath, 'w') as f:
            json.dump(list(article_links), f, indent=4)  # Convert set to list for JSON serialization
        logging.info(f"Sent articles saved to '{filepath}'.")
    except IOError:
        logging.error(f"Could not write sent articles to file '{filepath}'.")
    except Exception as e:
        logging.error(f"An unexpected error occurred while saving sent articles to '{filepath}': {e}")

# Main Logic
def main():
    """
    Main function for the Awwwards RSS Bot.
    Fetches new articles, filters out already sent ones, and sends a digest.
    """
    logging.info("Starting Awwwards RSS Bot...")

    # Load previously sent articles
    sent_article_links = load_sent_articles(SENT_ARTICLES_FILE)
    logging.info(f"Loaded {len(sent_article_links)} sent articles.")

    # Fetch new articles from RSS feed
    logging.info(f"Fetching articles from RSS feed: {RSS_URL}")
    fetched_articles = fetch_rss_feed(RSS_URL)

    if not fetched_articles:
        logging.info("No articles fetched from the RSS feed. Exiting.")
        return

    # Filter out already sent articles
    new_articles_to_send = []
    for article in fetched_articles:
        # Assuming each article dictionary has a 'link' key
        if 'link' in article and article['link'] not in sent_article_links:
            new_articles_to_send.append(article)

    # Send notifications for new articles
    if new_articles_to_send:
        logging.info(f"Found {len(new_articles_to_send)} new articles to send.")
        try:
            # Assuming send_digest returns True on success, False otherwise
            # or raises an exception on failure, which should be handled by telegram_messege.py
            send_digest(new_articles_to_send) # send_digest should handle its own success/failure logging
            logging.info("Digest sent successfully.")
            
            # Update the set of sent articles with the new ones
            for article in new_articles_to_send:
                sent_article_links.add(article['link'])
            save_sent_articles(SENT_ARTICLES_FILE, sent_article_links)

        except Exception as e:
            # This is a general catch-all. Ideally, send_digest would raise specific exceptions.
            logging.error(f"Failed to send digest or save sent articles: {e}")
            # Depending on the error, you might choose not to save sent_articles_links
            # if the digest failed to send. For now, we attempt to save anyway if some articles were processed.

    else:
        logging.info("No new articles found to send.")

    logging.info("Awwwards RSS Bot finished.")

# Entry point for the script
if __name__ == "__main__":
    main()
