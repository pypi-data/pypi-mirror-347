# http.py
# v0.4.0

"""HTTP Utility Functions"""

#region Imports

import httpx
import requests

from typing import List, Optional

from ..decorators import retry_http

#endregion

#region Exports

__all__: List[str] = [
    'get_with_retry',
    'get_with_retry_httpx',
]

#endregion

#region Functions

@retry_http
def get_with_retry(
            url: str,
            *,
            session: Optional[requests.Session],
        ) -> requests.Response:

    """Helper function to perform a simple GET web request with retries.

    :param url: The URL to fetch.
    :type url: str

    :param session: An optional `requests.Session` object
        to use for the request.
    
    :return: A `requests.Response`.
    :rtype: requests.Response
    """
    if session:
        return session.get(url)
    
    else:
        return requests.get(url)


@retry_http
def get_with_retry_httpx(
            url: str,
            *,
            client: Optional[httpx.Client],
        ) -> httpx.Response:

    """Helper function to perform a simple GET web request with retries.
    This variant uses httpx instead of requests.

    :param url: The URL to fetch.
    :type url: str

    :param client: An optional `httpx.Client` object
        to use for the request.
    
    :return: An `httpx.Response`.
    :rtype: httpx.Response
    """
    if client:
        return client.get(url)
    
    else:
        return httpx.get(url)

#endregion
