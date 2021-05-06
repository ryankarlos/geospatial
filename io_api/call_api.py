import requests
from requests.exceptions import HTTPError
import logging

logger = logging.getLogger(__name__)


def get_request(url):
    response = requests.get(url, timeout=30)
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
