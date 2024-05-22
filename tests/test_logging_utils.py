import unittest
import os
import logging
import tempfile

from utils.logging_utils import configure_logging, logger, VERBOSE

class TestLoggingConfiguration(unittest.TestCase):
    def setUp(self):
        # Create a temporary log file
        self.log_file = tempfile.NamedTemporaryFile(delete=False).name
        self.logger = configure_logging(self.log_file) # Store the configured logger

    def tearDown(self):
        # Properly close and remove handlers
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

        # Remove the temporary log file
        os.remove(self.log_file)


    """Tests configuration of logging using configure_logging().
    
    Verifies that configure_logging():
    - Creates a logger with two handlers (file and console) 
    - The file handler writes to the provided log file at DEBUG level
    - The console handler writes to stdout at VERBOSE level 
    - The logger itself is set to DEBUG level
    """
    def test_configure_logging(self):
        configure_logging(self.log_file)

        # Check if the logger has two handlers (file and console)
        self.assertEqual(len(logger.handlers), 2)

        # Check if the first handler is a FileHandler and its level is DEBUG
        self.assertIsInstance(logger.handlers[0], logging.FileHandler)
        self.assertEqual(logger.handlers[0].level, logging.DEBUG)

        # Check if the second handler is a StreamHandler and its level is VERBOSE
        self.assertIsInstance(logger.handlers[1], logging.StreamHandler)
        self.assertEqual(logger.handlers[1].level, VERBOSE)

        # Check if the logger's level is DEBUG
        self.assertEqual(logger.level, logging.DEBUG)

        # Check if a log file is created
        self.assertTrue(os.path.exists(self.log_file))

    def test_logging_levels(self):
        configure_logging(self.log_file)

        # Test if the logger correctly logs messages at different levels
        logger.debug('Debug message')
        logger.info('Info message')
        logger.warning('Warning message')
        logger.error('Error message')
        logger.critical('Critical message')
        logger.verbose('Verbose message')

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

        # Test what happens if the function is called multiple times with different log_file parameters
        configure_logging('test1.log')
        configure_logging('test2.log')
        self.assertEqual(len(logger.handlers), 2)  # There should still be only two handlers

if __name__ == '__main__':
    unittest.main()
