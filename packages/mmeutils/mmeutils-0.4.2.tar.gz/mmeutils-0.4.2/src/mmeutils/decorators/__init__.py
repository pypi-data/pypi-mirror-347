# decorators.py
# v6.0.0

"""A collection of general-use Python function decorators."""

#region Imports

import functools
import httpx
import json
import requests.exceptions as reqexc
import time

#from requests.exceptions import HTTPError, ChunkedEncodingError, ConnectionError, Timeout
from typing import Callable, List

#endregion

#region Exports

__all__: List[str] = [
    'retry_http',
    'retry_empty_dict',
    'retry_json_error',
    'retry_on_exception',
]

#endregion

#region Decorators

def retry_http(func: Callable, *, retries: int=3, sleep: float=0.4) -> Callable:
    """Retries a function call when an HTTP error occurs."""

    @functools.wraps(func)
    def retry_wrapper(*args, retries=retries, **kwargs):

        while retries > 0:

            try:

                result = func(*args, **kwargs)

                return result
            
            except (
                        reqexc.HTTPError,
                        reqexc.ConnectionError,
                        reqexc.Timeout,
                        reqexc.ChunkedEncodingError,
                        httpx.HTTPError,
                        httpx.ConnectError,
                        httpx.TimeoutException,
                    ):

                retries -= 1

                time.sleep(sleep)

                if retries == 0:
                    raise

    return retry_wrapper


def retry_empty_dict(func: Callable, *, retries: int=3) -> Callable:
    """Retries a function call when an empty dictionary is returned."""

    @functools.wraps(func)
    def retry_wrapper(*args, retries=retries, **kwargs):

        result = {}

        while len(result.keys()) == 0 and retries > 0:
            result = func(*args, **kwargs)
            retries -= 1
        
        return result

    return retry_wrapper


def retry_json_error(func: Callable, *, retries: int=3) -> Callable:
    """Retries a function call when a JSON decode error occurs."""

    @functools.wraps(func)
    def retry_wrapper(*args, retries=retries, **kwargs):
        while retries > 0:
            try:
                result = func(*args, **kwargs)
                return result
            
            except json.JSONDecodeError:
                retries -= 1

                if retries == 0:
                    raise

    return retry_wrapper


def retry_on_exception(func: Callable, *, retries: int=3) -> Callable:
    """Retries a function call when any exception (Exception) is raised."""

    @functools.wraps(func)
    def retry_wrapper(*args, retries=retries, **kwargs):
        while retries > 0:
            try:
                result = func(*args, **kwargs)
                return result
            
            except Exception:
                retries -= 1

                if retries == 0:
                    raise

    return retry_wrapper

#endregion
