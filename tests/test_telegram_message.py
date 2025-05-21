import unittest
from unittest.mock import patch, MagicMock, call
import os
from telegram.error import TelegramError # Import TelegramError

# Important: Import the function from the module with the typo in its filename
from telegram_messege import send_digest 

class TestTelegramMessage(unittest.TestCase):

    @patch('telegram_messege.Bot')
    def test_send_digest_success(self, mock_bot_constructor):
        # Configure the mock Bot instance
        mock_bot_instance = MagicMock()
        mock_bot_constructor.return_value = mock_bot_instance

        sample_articles = [
            {"title": "Article 1", "link": "http://example.com/1", "summary": "Summary 1"},
            {"title": "Article 2", "link": "http://example.com/2", "summary": "Summary 2"}
        ]

        result = send_digest(sample_articles, bot_token="fake_token", chat_id="fake_chat_id")

        mock_bot_constructor.assert_called_once_with(token="fake_token")
        self.assertEqual(mock_bot_instance.send_message.call_count, len(sample_articles))

        expected_calls = []
        for article in sample_articles:
            message_text = f"<b>{article['title']}</b>\n<a href='{article['link']}'>Read more</a>\n{article['summary']}"
            expected_calls.append(
                call(chat_id="fake_chat_id", text=message_text, parse_mode='HTML')
            )
        
        mock_bot_instance.send_message.assert_has_calls(expected_calls, any_order=False)
        self.assertTrue(result)

    @patch('telegram_messege.Bot')
    def test_send_digest_telegram_error(self, mock_bot_constructor):
        # Configure the mock Bot instance to raise TelegramError
        mock_bot_instance = MagicMock()
        mock_bot_instance.send_message.side_effect = TelegramError("Simulated API error")
        mock_bot_constructor.return_value = mock_bot_instance
        
        sample_articles = [
            {"title": "Article 1", "link": "http://example.com/1", "summary": "Summary 1"}
        ]

        # We also need to mock 'logging.error' if we want to check its output.
        # @patch('telegram_messege.logging.error')
        # def test_send_digest_telegram_error(self, mock_logging_error, mock_bot_constructor):

        result = send_digest(sample_articles, bot_token="fake_token", chat_id="fake_chat_id")

        mock_bot_constructor.assert_called_once_with(token="fake_token")
        mock_bot_instance.send_message.assert_called_once() # Check it was called
        self.assertFalse(result)
        # If logging was mocked:
        # mock_logging_error.assert_called_with(f"Failed to send message for article 'Article 1': Simulated API error")


    @patch.dict(os.environ, {}, clear=True)
    @patch('telegram_messege.logging.error') # Mock logger to check output
    def test_send_digest_missing_credentials(self, mock_logging_error):
        # No need to mock Bot here as it shouldn't be called if credentials are None
        
        result_token_none = send_digest([], bot_token=None, chat_id="fake_chat_id")
        self.assertFalse(result_token_none)
        mock_logging_error.assert_any_call("BOT_TOKEN or CHAT_ID is not set. Please check your .env file or environment variables.")

        # Reset mock for next call if necessary, or use separate tests
        mock_logging_error.reset_mock() 
        
        result_chat_id_none = send_digest([], bot_token="fake_token", chat_id=None)
        self.assertFalse(result_chat_id_none)
        mock_logging_error.assert_any_call("BOT_TOKEN or CHAT_ID is not set. Please check your .env file or environment variables.")


if __name__ == '__main__':
    unittest.main()
