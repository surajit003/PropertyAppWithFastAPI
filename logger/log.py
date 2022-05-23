import logging
from logging.handlers import RotatingFileHandler

from functools import wraps

from settings import LOG_FILE_NAME

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
fh = RotatingFileHandler(LOG_FILE_NAME)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)


def save_log(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            request = kwargs.get("request")
            url = request.url
            method = request.method
            message = dict(
                url=str(url),
                method=method,
            )
            if hasattr(request, "data"):
                data = await request.data()
                message["data"] = [data]
            if hasattr(request, 'json'):
                json_data = await request.json()
                message["data"] = [json_data]
            logger.debug(message)
        except Exception as exc:
            logger.exception(f'Exception occurred {exc}')
            pass
        return await func(*args, **kwargs)
    return wrapper
