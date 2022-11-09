import traceback
import uuid
from functools import wraps
from time import time

from flask import request

import utils.log_utils as log


def safe_request(method):
    """ Decorator to make the HTTP request safe (logging + error catching) """

    @wraps(method)
    def wrapper(*args, **kwargs):
        request_uid = str(uuid.uuid4())[:8]

        log.request(request_uid, f"Incoming {request.method} request at endpoint \"{request.url}\"!")
        if request.data:
            log.request(request_uid, f"Request body: {request.data}!")

        try:
            start_time = time()
            response = method(*args, **kwargs, uid=request_uid)
            log.request(request_uid, f"Responding with code {response.status_code} in {int((time() - start_time) * 1000)} ms")
            if response.data:
                log.request(request_uid, f"Responding with payload: {response.data}")
        except Exception as e:
            log.error(f"[{request_uid}] An internal exception has been caught by safe request:")
            log.error(f"[{request_uid}] {e}")
            log.error(f"[{request_uid}] {traceback.format_exc()}")
            return {"message": "Internal server error, see console for details"}, 500

        return response

    return wrapper


average_response_times = {}


def log_response_time(endpoint_name: str):
    """
    Decorator to log & calculate the average response time of an endpoint
    - uses the running average algorithm approximate that is equivalent to exponential moving average
    - for more information: https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average
    """

    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            start_time = time()
            response = method(*args, **kwargs)
            response_time = int((time() - start_time) * 1000)

            if endpoint_name not in average_response_times:
                average_response_times[endpoint_name] = response_time
            else:
                average_response_times[endpoint_name] = _running_average(average_response_times[endpoint_name], response_time)

            return response

        return wrapper

    return decorator


def _running_average(average, new_data, sample_count=1000):
    average -= average / sample_count
    average += new_data / sample_count
    return average
