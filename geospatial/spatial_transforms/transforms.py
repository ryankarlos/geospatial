import json
from typing import Any, Dict, Optional, Sequence, Union

import geopandas as gpd
import pandas as pd
import pyproj
from geopandas.tools import geocode
from geospatial.logging_config import logging_config

logger = logging_config("transformer")


def check_epsg_code(str):
    """
    Returns epsg code for the proj string passed in
    Returns
    -------
    EPSG code

    """
    crs = pyproj.CRS(str)
    return crs.to_epsg()


def geocode_locations(df: gpd.GeoDataFrame, loc_col: str):
    """
    Geocode location names into polygon coordinates
    Parameters
    ----------
    df: Geopandas DataFrame
    loc_col:str
    name of column in df which contains locations
    Returns
    -------

    """
    locations = geocode(df.loc[:, loc_col])
    df["geometry"] = locations.loc[:, "geometry"]
    df["address"] = locations.loc[:, "address"]
    return df


def merge_df(
    df1: gpd.GeoDataFrame,
    df2: Union[gpd.GeoDataFrame, pd.DataFrame],
    strategy: str,
    **kwargs,
):
    """
    Merges two dataframes together based on 'attribute join' or
    'spatial join'. For former, merges geopandas and pandas df based
    on common atrribute. For latter, merged two geopnads df based on
    observations spatial relationship to each other
    Parameters
    ----------
    df1: Geopandas DataFrame
    df2: (Geopandas df, Pandas df)
    strategy: 'attribute' or 'spatial'
    kwargs

    Returns
    -------

    """
    if strategy == "attribute":
        try:
            assert isinstance(df1, gpd.GeoDataFrame)
            assert isinstance(df2, pd.DataFrame)
            logger.info(f"Merging geodataframe and pd dataframe on attribute")
            return df1.merge(df2, **kwargs)
        except AssertionError:
            raise TypeError(
                f"Dataframes passed in need to geopandas and pandas for {strategy} join"
            )
    elif strategy == "spatial":
        if not isinstance(df1, gpd.GeoDataFrame) and isinstance(df2, gpd.GeoDataFrame):
            raise TypeError(f"Both df need to be Geopandas df for {strategy} join")
        logger.info(f"carrying out spatial join with following settings: {kwargs}")
        return gpd.sjoin(df1, df2, **kwargs).loc[
            :, ["latitude", "longitude", "geometry"]
        ]


def response_to_gdf(
    response: Sequence[Dict[str, Any]],
    base_df: Optional[Union[pd.DataFrame, None]] = None,
) -> gpd.GeoDataFrame:
    """
    Converse the response json

    Parameters
    ----------
    response: json
    Response in json format, received after sending
    request to police url
    base_df: (Pd.DataFrame, None): Default:None
     If base_df specified - sets the crs of the gdf layer
     to match that of base_df

    Returns
    -------

    """
    df = pd.DataFrame(response)
    logger.info(f"generating lat/lon columns from location tuple")
    df["latitude"] = df["location"].map(lambda x: float(x["latitude"]))
    df["longitude"] = df["location"].map(lambda x: float(x["longitude"]))
    ds = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df["longitude"], df["latitude"])
    )
    if base_df is not None:
        logger.info(f"Setting projection of layer same as basemap: {base_df.crs}")
        ds = ds.set_crs(base_df.crs)
    return ds
