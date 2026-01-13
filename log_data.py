import logging
import os

def setup_logging(log_file='app.log'):
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file)
            #logging.StreamHandler()
        ]
    )

setup_logging()
logger = logging.getLogger(__name__)
#logger.info("Logging is set up.")
#logger.debug("This is a debug message.")