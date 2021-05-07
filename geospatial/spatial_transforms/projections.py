import pyproj


def check_epsg_code(str):
    """
    Returns epsg code for the proj string passed in
    Returns
    -------
    EPSG code

    """
    crs = pyproj.CRS(str)
    return crs.to_epsg()
