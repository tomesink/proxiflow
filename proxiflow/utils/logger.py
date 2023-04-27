import logging


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Create a logger instance with the specified name and log level.

    :param name: The name of the logger instance.
    :type name: str
    :param level: The logging level for the logger instance. Defaults to logging.INFO.
    :type level: int

    :returns: The logger instance.
    :rtype: logging.Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create console handler and set level to INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Create formatter and add to console handler
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    # Add console handler to logger
    logger.addHandler(console_handler)

    return logger
