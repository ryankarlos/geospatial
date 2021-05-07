import logging

import requests
from requests.exceptions import HTTPError

logger = logging.getLogger("dev")


def get_request(url, timeout=None):
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
    response = requests.get(url, timeout=timeout)
    try:
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        logger.exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        pass
        logger.exception(f"Other error occurred: {err}")
    else:
        logger.info(f"HTTP request for {url} was successful!")

    response.encoding = "utf-8"

    return response.json()
