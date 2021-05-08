import os

from geospatial.io.constants import ESRI, GEOJSON
from geospatial.logging_config import logging_config
from geospatial.utils import set_working_dir_repo_root

logger = logging_config("io")


@set_working_dir_repo_root
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
    if driver == GEOJSON:
        assert filename.split(".")[1] == "geojson"
    elif driver == ESRI:
        assert filename.split(".")[1] == "shp"
    else:
        raise ValueError(
            f"driver must be either {GEOJSON} or {ESRI}." f"You passed {driver}"
        )

    df.to_file(path, driver=driver)
    logger.debug(f"{filename} saved in {path}")
