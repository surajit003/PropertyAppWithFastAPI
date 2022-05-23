import json
import logging
from functools import wraps
from settings import BASE_DIR

logger = logging.getLogger(__name__)

LOG_FILE = BASE_DIR.joinpath('data/app.json')


async def append_log(data):
    with open(LOG_FILE, 'a') as file:
        json.dump(data, file)
        file.write('\n')


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
            await append_log(message)
        except Exception as exc:
            logger.exception(f'Exception occurred {exc}')
            pass
        return await func(*args, **kwargs)

    return wrapper
