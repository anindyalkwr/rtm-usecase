import logging

from config.utils import get_env

LOG_LEVEL = get_env("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=getattr(logging, LOG_LEVEL, logging.INFO)
)

logger = logging.getLogger(__name__)
