import logging

from requests.exceptions import HTTPError

import grequests
from gevent import monkey as curious_george

# need to patch before import func which uses grequests
# https://stackoverflow.com/questions/56309763/grequests-monkey-patch-warning
curious_george.patch_all(thread=False, select=False)


logger = logging.getLogger("dev")


def get_request(url, calls=None):
    """

    Parameters
    ----------
    url: str
    url of the request
    timeout: Default None
    A number, or a tuple, indicating how many seconds to wait
    for the client to make a connection and/or send a response.

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
