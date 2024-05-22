import unittest
import os
import logging
import tempfile

from utils.logging_utils import configure_logging, logger, VERBOSE

class TestLoggingConfiguration(unittest.TestCase):
    def setUp(self):
        # Create a temporary log file
        self.log_file = tempfile.NamedTemporaryFile(delete=False).name
        self.logger = configure_logging(self.log_file)  # Store the configured logger

    def tearDown(self):
        # Close and remove ALL handlers
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

        # Remove the temporary log file
        os.remove(self.log_file)

    def test_configure_logging(self):
        # No need to call configure_logging() again here
        # Use the logger configured in setUp()

        # Check if the logger has two handlers (file and console)
        self.assertEqual(len(self.logger.handlers), 2)

        # Check if the first handler is a FileHandler and its level is DEBUG
        self.assertIsInstance(self.logger.handlers[0], logging.FileHandler)
        self.assertEqual(self.logger.handlers[0].level, logging.DEBUG)

        # Check if the second handler is a StreamHandler and its level is VERBOSE
        self.assertIsInstance(self.logger.handlers[1], logging.StreamHandler)
        self.assertEqual(self.logger.handlers[1].level, VERBOSE)

        # Check if the logger's level is DEBUG
        self.assertEqual(self.logger.level, logging.DEBUG)

        # Check if a log file is created
        self.assertTrue(os.path.exists(self.log_file))

    def test_logging_levels(self):
        # No need to call configure_logging() again here

        # Test if the logger correctly logs messages at different levels
        self.logger.debug('Debug message')
        self.logger.info('Info message')
        self.logger.warning('Warning message')
        self.logger.error('Error message')
        self.logger.critical('Critical message')
        self.logger.verbose('Verbose message')

        # Check if the messages are correctly written to the log file
        with open(self.log_file, 'r') as file:
            log_content = file.read()
        self.assertIn('Debug message', log_content)
        self.assertIn('Info message', log_content)
        self.assertIn('Warning message', log_content)
        self.assertIn('Error message', log_content)
        self.assertIn('Critical message', log_content)
        self.assertIn('Verbose message', log_content)

    def test_edge_cases(self):
        # Test what happens if the log_file parameter is None
        with self.assertRaises(ValueError):
            configure_logging(None)

        # Test what happens if the log_file parameter is an empty string
        with self.assertRaises(ValueError):
            configure_logging('')

        # Call configure_logging with different temp files
        with tempfile.NamedTemporaryFile(delete=False) as temp_log1:
            configure_logging(temp_log1.name)

        with tempfile.NamedTemporaryFile(delete=False) as temp_log2:
            configure_logging(temp_log2.name)

        # Assert that there are still 2 handlers (file and console)
        self.assertEqual(len(self.logger.handlers), 2)