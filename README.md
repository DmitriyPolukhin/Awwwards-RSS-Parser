# Awwwwards RSS Parser

This project is a Python-based RSS parser for Awwwwards website that monitors and processes RSS feeds. It includes functionality to parse RSS feeds and send updates via Telegram.

## Features

- RSS feed parsing from Awwwwards
- Telegram integration for notifications
- JSON-based state management
- Automated feed monitoring

## Project Structure

- `awwwwards_bot.py`: Main script for RSS parsing, state management, and Telegram bot functionality.
- `rss_parser.py`: Module for RSS feed parsing functionality.
- `telegram_messege.py`: Module for Telegram messaging integration.
- `sent_articles.json`: Stores unique identifiers (e.g., links) of articles that have already been processed and sent, to prevent duplicates.

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment:
   - Windows: `.venv\Scriptsctivate`
   - Unix/MacOS: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Configuration

To configure the Telegram bot, you need to create a `.env` file in the root directory of the project. This file should contain your Telegram Bot Token and Chat ID.

Create a file named `.env` and add the following lines, replacing the placeholder values with your actual credentials:

```env
BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID="YOUR_TELEGRAM_CHAT_ID_OR_CHANNEL_USERNAME"
```

The `telegram_messege.py` module will load these variables to send messages.

## Usage

To run the bot, navigate to the project directory in your terminal and execute the main script:

```bash
python awwwwards_bot.py
```

When executed, the bot performs the following actions:
1.  Fetches the latest articles from the Awwwards blog RSS feed.
2.  Checks against `sent_articles.json` to identify new articles.
3.  Sends a digest of these new articles to the configured Telegram chat or channel.
4.  Updates `sent_articles.json` with the links of the articles that were sent.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
