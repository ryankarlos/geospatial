from requests.exceptions import HTTPError

import grequests
from geospatial.logging_config import logging_config

logger = logging_config("io")


def get_request(url, calls=None):
    """
    Make requests asynchronously and collec list of responses
    Parameters
    ----------
    url: str
    url of the request
    calls: Optional (int, None)
    Number of calls to make to the url - defaults to None for
    single request
    Returns
    -------
    """
    # response = requests.get(url, timeout=timeout)
    if calls is not None:
        # call multiple times asynchronously
        number_calls = [url] * calls
        rs = (grequests.get(u) for u in number_calls)
    else:
        # single call
        rs = (grequests.get(u) for u in [url])
    responses = grequests.map(rs)
    result = []
    for r in responses:
        if r.status_code == 200:
            result = r.json()
            break
    if len(result) == 0:
        raise HTTPError("server not responding")

    else:
        logger.info(f"HTTP request for {url} was successful!")

    return result
