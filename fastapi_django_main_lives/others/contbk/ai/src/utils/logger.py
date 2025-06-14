import logging

def get_logger():
    """Returns a logger instance"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    return logger