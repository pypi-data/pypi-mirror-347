import requests

__all__ = ['get_with_retry']

def get_with_retry(url: str, *, session: requests.Session | None) -> requests.Response: ...
