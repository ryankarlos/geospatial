import os

from geospatial.utils import logging_config

logger = logging_config("io")


def write_gdf_to_file(df, filename, driver="GeoJSON"):
    """
    write geodataframe to file. Depending on the driver
    choice could write to
    shapefile or geojson
    Parameters
    ----------
    df: GeoDataFrame
    filename: string
    file path to write to
    driver: string, default: ‘ESRI Shapefile’
    Can either be 'GeoJSON' or ‘ESRI Shapefile’.
    Returns
    -------
    """
    path = os.path.join("data", filename)
    if driver == "GeoJSON":
        assert filename.split(".")[1] == "geojson"
    elif driver == "ESRI Shapefile":
        assert filename.split(".")[1] == "shp"
    else:
        raise ValueError(
            f"driver must be either 'GeoJSON' or ''ESRI Shapefile'."
            f"You passed {driver}"
        )

    df.to_file(path, driver=driver)
    logger.debug(f"{filename} saved in {path}")
