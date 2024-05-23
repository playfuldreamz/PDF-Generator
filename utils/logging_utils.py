import logging

# Create a logger
logger = logging.getLogger('pdf_generator')

# Define a custom logging level
VERBOSE = 55 # Choose a unique level number
logging.addLevelName(VERBOSE, "VERBOSE")

# Set the method for the custom level
def verbose(self, message, *args, **kws):
    if self.isEnabledFor(VERBOSE):
        self._log(VERBOSE, message, args, **kws)

logging.Logger.verbose = verbose

def configure_logging(log_file):
    if log_file is None or log_file == '':
        raise ValueError('log_file cannot be None or an empty string')

    # Remove all existing handlers
    for handler in logger.handlers:
        logger.removeHandler(handler)

    logger.setLevel(logging.DEBUG) # Set the logger's level to DEBUG to capture all messages

    # Create a file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG) # Set the file handler's level to DEBUG to log all messages

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(VERBOSE) # Set the console handler's level to VERBOSE

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Remove all handlers associated with the logger to avoid duplicate logging
    for handler in logger.handlers:
        logger.removeHandler(handler)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
