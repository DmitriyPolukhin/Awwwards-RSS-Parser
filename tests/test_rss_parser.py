import unittest
from unittest.mock import patch, MagicMock
from rss_parser import fetch_rss_feed

class TestRssParser(unittest.TestCase):

    @patch('rss_parser.feedparser.parse')
    def test_fetch_rss_feed_success(self, mock_parse):
        # Configure the mock_parse return_value
        mock_entry1 = MagicMock()
        mock_entry1.title = "Test Title 1"
        mock_entry1.link = "http://example.com/test1"
        mock_entry1.summary = "Test Summary 1"

        mock_entry2 = MagicMock()
        mock_entry2.title = "Test Title 2"
        mock_entry2.link = "http://example.com/test2"
        mock_entry2.summary = "Test Summary 2"

        mock_feed_data = MagicMock()
        mock_feed_data.entries = [mock_entry1, mock_entry2]
        mock_parse.return_value = mock_feed_data

        articles = fetch_rss_feed("dummy_url")

        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0]['title'], "Test Title 1")
        self.assertEqual(articles[0]['link'], "http://example.com/test1")
        self.assertEqual(articles[0]['summary'], "Test Summary 1")
        self.assertEqual(articles[1]['title'], "Test Title 2")
        self.assertEqual(articles[1]['link'], "http://example.com/test2")
        self.assertEqual(articles[1]['summary'], "Test Summary 2")

    @patch('rss_parser.feedparser.parse')
    def test_fetch_rss_feed_parsing_error(self, mock_parse):
        # Configure mock_parse to raise an exception
        mock_parse.side_effect = Exception("Simulated parsing error")

        # We also need to mock 'print' if we want to check its output,
        # but the primary check is the return value.
        # For now, we'll just check the return value as per instructions.
        # @patch('builtins.print')
        # def test_fetch_rss_feed_parsing_error(self, mock_print, mock_parse):
        
        articles = fetch_rss_feed("dummy_url")

        self.assertEqual(articles, [])
        # If we were mocking print:
        # mock_print.assert_called_with("Error fetching RSS feed: Simulated parsing error")

if __name__ == '__main__':
    unittest.main()
