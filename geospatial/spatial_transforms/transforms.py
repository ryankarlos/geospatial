from typing import Union

import geopandas
import pandas as pd
import pyproj
from geopandas.tools import geocode


def check_epsg_code(str):
    """
    Returns epsg code for the proj string passed in
    Returns
    -------
    EPSG code

    """
    crs = pyproj.CRS(str)
    return crs.to_epsg()


def geocode_locations(df: geopandas.GeoDataFrame, loc_col: str):
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
    df1: geopandas.GeoDataFrame,
    df2: Union[geopandas.GeoDataFrame, pd.DataFrame],
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
            assert isinstance(df1, geopandas.GeoDataFrame)
            assert isinstance(df2, pd.DataFrame)
            return df1.merge(df2, **kwargs)
        except AssertionError:
            raise TypeError(
                f"Dataframes passed in need to geopandas and pandas for {strategy} join"
            )
    elif strategy == "spatial":
        if not isinstance(df1, geopandas.GeoDataFrame) and isinstance(
            df2, geopandas.GeoDataFrame
        ):
            raise TypeError(f"Both df need to be Geopandas df for {strategy} join")
        return geopandas.sjoin(df1, df2, **kwargs)
