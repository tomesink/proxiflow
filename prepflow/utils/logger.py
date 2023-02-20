import logging


def get_logger(name, level=logging.INFO):
    """
    Create a logger instance with the specified name and log level.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create console handler and set level to INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create formatter and add to console handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    # Add console handler to logger
    logger.addHandler(console_handler)

    return logger
