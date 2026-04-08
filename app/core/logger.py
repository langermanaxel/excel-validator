import logging
from app.core.config import get_settings

settings = get_settings()

def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        filename="app.log",
        level=settings.log_level,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(name)