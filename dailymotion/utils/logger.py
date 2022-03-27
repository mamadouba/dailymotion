import logging
from dailymotion.settings import settings


def getLogger():
    level = logging.INFO
    if settings.debug:
        level = logging.DEBUG
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger(__name__)


logger = getLogger()
