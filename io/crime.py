import os
import logging
from constants import URL_CRIME, IGNORED_OUTCOMES

logger = logging.getLogger(__name__)


def get_neighbourhoods(get_request, police_id):
    url = os.path.join(URL_CRIME, f"{police_id}/neighbourhoods")

    return get_request(url)


def get_stop_search_by_force(get_request, police_id, date=None):
    """
    Retrieve stop and search data for a given police force. if date is not provided,
    returns all stop and search data which have lead to outcomes like arrest, court summons
    for latest month(s).Also removes any data with no location info
    """

    new_list = []
    if date is None:
        url = os.path.join(URL_CRIME, f"stops-force?force={police_id}")
    else:
        url = os.path.join(URL_CRIME, f"stops-force?force={police_id}&date={date}")
    response = get_request(url)
    for json in response:
        if (json.get("outcome") not in IGNORED_OUTCOMES) and (
            json.get("location") is not None
        ):
            new_list.append(json)

    logger.info(f"Successfully fetched data from month: {date}")
    return new_list


def get_police_id(get_request, force_name):
    """
    Get police id and police force names in json
    """
    url = os.path.join(URL_CRIME, "forces")
    response = get_request(url)
    for json in response:
        if json.get("name") == force_name:
            police_id = json.get("id")
            break

    logger.info(f"Police id for {force_name}:- '{police_id}'")

    return police_id
