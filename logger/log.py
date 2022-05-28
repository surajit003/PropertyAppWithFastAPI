import logging
import os
import uuid
from logging.handlers import RotatingFileHandler
from functools import wraps

from aws.services.dynamo_db.logs import create_log
from settings import LOG_FILE_DIR
from settings import LOG_FILE_NAME

LOG_FILE = LOG_FILE_DIR.joinpath(LOG_FILE_NAME)


def create_log_dir():
    if not os.path.exists("logs"):
        os.makedirs("logs")


def create_log_file():
    try:
        open(LOG_FILE, "x")
    except FileExistsError:
        pass


create_log_dir()
create_log_file()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
fh = RotatingFileHandler(LOG_FILE)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)


def save_log(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            request = kwargs.get("request")
            url = request.url
            client = request.client.host
            method = request.method
            message = dict(
                url=str(url),
                method=method,
            )
            if hasattr(request, "data"):
                data = await request.data()
                message["data"] = [data]
            if hasattr(request, "json"):
                json_data = await request.json()
                message["data"] = [json_data]
            logger.debug(message)
            data = dict(
                log_id=str(uuid.uuid4()),
                request_ip=client,
                message=message
            )
            res = await create_log(data)
            print('res',res)
        except Exception as exc:
            logger.exception(f"Exception occurred {exc}")
            pass
        return await func(*args, **kwargs)

    return wrapper
