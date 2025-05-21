import unittest
from unittest.mock import patch, MagicMock, call
import json
import os

# Import the module to be tested
import awwwwards_bot 
from awwwwards_bot import main, load_sent_articles, save_sent_articles # import specific functions

# It's good practice to define a test-specific file to avoid conflicts
TEST_SENT_ARTICLES_FILE = "test_sent_articles.json"

class TestAwwwwardsBot(unittest.TestCase):

    def setUp(self):
        """
        Set up for test methods.
        This method is called before each test method.
        """
        self.test_sent_articles_file = TEST_SENT_ARTICLES_FILE
        # Ensure no old test file is present
        if os.path.exists(self.test_sent_articles_file):
            os.remove(self.test_sent_articles_file)

    def tearDown(self):
        """
        Clean up after test methods.
        This method is called after each test method.
        """
        if os.path.exists(self.test_sent_articles_file):
            os.remove(self.test_sent_articles_file)

    def test_load_sent_articles_file_not_found(self):
        """
        Test loading sent articles when the file does not exist.
        """
        # Patching SENT_ARTICLES_FILE within the awwwwards_bot module for the scope of this test
        # if load_sent_articles directly used the global.
        # However, load_sent_articles takes filepath as an argument, so we can pass it directly.
        loaded_links = load_sent_articles("non_existent_file.json")
        self.assertEqual(loaded_links, set())
        # Optional: Test for logging warning. Requires mocking logging.
        # with patch('awwwwards_bot.logging.warning') as mock_log_warning:
        #     load_sent_articles("non_existent_file.json")
        #     mock_log_warning.assert_called_with(
        #         "Sent articles file 'non_existent_file.json' not found. Starting with an empty set."
        #     )

    def test_load_and_save_articles(self):
        """
        Test saving articles and then loading them back.
        """
        expected_links_set = {"http://example.com/link1", "http://example.com/link2"}
        
        # save_sent_articles expects a set (as per current awwwwards_bot.py)
        save_sent_articles(self.test_sent_articles_file, expected_links_set)
        
        loaded_links_set = load_sent_articles(self.test_sent_articles_file)
        self.assertEqual(loaded_links_set, expected_links_set)

    def test_load_sent_articles_json_decode_error(self):
        """
        Test loading sent articles from a malformed JSON file.
        """
        with open(self.test_sent_articles_file, 'w') as f:
            f.write("this is not json")
        
        loaded_links = load_sent_articles(self.test_sent_articles_file)
        self.assertEqual(loaded_links, set())
        # Optional: Test for logging warning
        # with patch('awwwwards_bot.logging.warning') as mock_log_warning:
        #     load_sent_articles(self.test_sent_articles_file)
        #     self.assertTrue(mock_log_warning.called)


    @patch('awwwwards_bot.SENT_ARTICLES_FILE', TEST_SENT_ARTICLES_FILE) # Ensure main uses the test file
    @patch('awwwwards_bot.save_sent_articles')
    @patch('awwwwards_bot.load_sent_articles')
    @patch('awwwwards_bot.send_digest')
    @patch('awwwwards_bot.fetch_rss_feed')
    def test_main_flow_new_articles(self, mock_fetch_rss, mock_send_digest, 
                                    mock_load_sent, mock_save_sent):
        """
        Test the main flow when there are new articles to send.
        """
        mock_load_sent.return_value = {"link1"} # Previously sent
        
        fetched_articles_data = [
            {'title': 'Article 1', 'link': 'link1', 'summary': 'Summary 1'}, # Already sent
            {'title': 'Article 2', 'link': 'link2', 'summary': 'Summary 2'}, # New
            {'title': 'Article 3', 'link': 'link3', 'summary': 'Summary 3'}  # New
        ]
        mock_fetch_rss.return_value = fetched_articles_data
        
        mock_send_digest.return_value = True # Simulate successful send

        main()

        mock_fetch_rss.assert_called_once_with(awwwwards_bot.RSS_URL)
        mock_load_sent.assert_called_once_with(TEST_SENT_ARTICLES_FILE)
        
        expected_articles_to_send = [
            {'title': 'Article 2', 'link': 'link2', 'summary': 'Summary 2'},
            {'title': 'Article 3', 'link': 'link3', 'summary': 'Summary 3'}
        ]
        mock_send_digest.assert_called_once_with(expected_articles_to_send)
        
        # The save_sent_articles function in awwwwards_bot.py expects a set
        expected_saved_links_set = {"link1", "link2", "link3"}
        mock_save_sent.assert_called_once_with(TEST_SENT_ARTICLES_FILE, expected_saved_links_set)


    @patch('awwwwards_bot.SENT_ARTICLES_FILE', TEST_SENT_ARTICLES_FILE)
    @patch('awwwwards_bot.save_sent_articles')
    @patch('awwwwards_bot.load_sent_articles')
    @patch('awwwwards_bot.send_digest')
    @patch('awwwwards_bot.fetch_rss_feed')
    def test_main_flow_no_new_articles(self, mock_fetch_rss, mock_send_digest, 
                                       mock_load_sent, mock_save_sent):
        """
        Test the main flow when there are no new articles.
        """
        mock_load_sent.return_value = {"link1", "link2"}
        
        fetched_articles_data = [
            {'title': 'Article 1', 'link': 'link1', 'summary': 'Summary 1'},
            {'title': 'Article 2', 'link': 'link2', 'summary': 'Summary 2'}
        ]
        mock_fetch_rss.return_value = fetched_articles_data

        main()

        mock_fetch_rss.assert_called_once_with(awwwwards_bot.RSS_URL)
        mock_load_sent.assert_called_once_with(TEST_SENT_ARTICLES_FILE)
        mock_send_digest.assert_not_called()
        mock_save_sent.assert_not_called() # save should not be called if no new articles were sent


    @patch('awwwwards_bot.SENT_ARTICLES_FILE', TEST_SENT_ARTICLES_FILE)
    @patch('awwwwards_bot.save_sent_articles')
    @patch('awwwwards_bot.load_sent_articles')
    @patch('awwwwards_bot.send_digest')
    @patch('awwwwards_bot.fetch_rss_feed')
    def test_main_flow_fetch_error(self, mock_fetch_rss, mock_send_digest, 
                                   mock_load_sent, mock_save_sent):
        """
        Test the main flow when fetch_rss_feed returns an empty list (simulating an error).
        """
        mock_load_sent.return_value = {"link1"} # Some articles might have been sent previously
        mock_fetch_rss.return_value = [] # Simulate fetch error

        main()

        mock_fetch_rss.assert_called_once_with(awwwwards_bot.RSS_URL)
        mock_load_sent.assert_called_once_with(TEST_SENT_ARTICLES_FILE) # load is still called
        mock_send_digest.assert_not_called()
        mock_save_sent.assert_not_called()


    @patch('awwwwards_bot.SENT_ARTICLES_FILE', TEST_SENT_ARTICLES_FILE)
    @patch('awwwwards_bot.save_sent_articles')
    @patch('awwwwards_bot.load_sent_articles')
    @patch('awwwwards_bot.send_digest')
    @patch('awwwwards_bot.fetch_rss_feed')
    def test_main_flow_send_digest_fails(self, mock_fetch_rss, mock_send_digest, 
                                         mock_load_sent, mock_save_sent):
        """
        Test the main flow when send_digest fails (returns False).
        """
        mock_load_sent.return_value = {"link1"}
        
        fetched_articles_data = [
            {'title': 'Article 1', 'link': 'link1', 'summary': 'Summary 1'},
            {'title': 'Article 2', 'link': 'link2', 'summary': 'Summary 2'} # New
        ]
        mock_fetch_rss.return_value = fetched_articles_data
        
        mock_send_digest.return_value = False # Simulate send failure

        main()

        mock_fetch_rss.assert_called_once_with(awwwwards_bot.RSS_URL)
        mock_load_sent.assert_called_once_with(TEST_SENT_ARTICLES_FILE)
        
        expected_articles_to_send = [
            {'title': 'Article 2', 'link': 'link2', 'summary': 'Summary 2'}
        ]
        mock_send_digest.assert_called_once_with(expected_articles_to_send)
        
        # Crucially, save should not be called if sending the digest failed
        mock_save_sent.assert_not_called()

if __name__ == '__main__':
    unittest.main()
