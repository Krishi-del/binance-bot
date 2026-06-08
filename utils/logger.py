import logging
import os

from config import LOG_DIR, LOG_FILE, LOG_FORMAT, LOG_DATE_FORMAT

# optional: allow environment control
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def get_logger(name: str) -> logging.Logger:
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)

    #  Prevent propagation (avoids duplicate logs)
    logger.propagate = False

    #  Prevent duplicate handler setup (safer check)
    if logger.hasHandlers():
        return logger

    #  Set dynamic log level (IMPORTANT IMPROVEMENT)
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    # =========================
    # FILE HANDLER
    # =========================
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # =========================
    # CONSOLE HANDLER
    # =========================
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger