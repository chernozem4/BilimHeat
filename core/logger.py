import logging
import sys


def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Создаёт и настраивает логгер с выводом в консоль.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    return logger


logger = setup_logger()
