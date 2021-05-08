import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from geospatial.logging_config import logging_config
from mpl_toolkits.axes_grid1 import make_axes_locatable

pd.set_option("display.max_columns", 15)

logger = logging_config("plot")
logger.propagate = False


def plot_basemap_from_shapefile(filepath, projection):
    """
    Plots basemap from shapefile
    Parameters
    ----------
    projection: str, int
    Setting ccoordinate reference system to mercrator or WGS84: Lat/Lon if
    passed as string. Alternatively can pass in the EPSG code if different
    projection required.
    Returns
    -------
    Geopandas dataframe with set proj
    plot ax object

    """
    data = gpd.read_file(filepath)
    if projection == "mercator":
        data_new = data.to_crs("EPSG:3395")
    elif projection == "WGS84":
        data_new = data.to_crs("EPSG:4326")
    else:
        assert isinstance(projection, int)
        data_new = data.to_crs(f"EPSG:{projection}")
    logger.info(f"basemap has been converted from {data.crs} to {data_new.crs}")
    ax = data_new.plot(figsize=(10, 10), alpha=0.5, color="wheat", edgecolor="black")
    ax.set_title(f"Basemap with {projection} projection")
    return data_new, ax


def add_layer_to_plot(layer_df, ax, base_df):
    """
    Adds additional layer on top of base plot layer e.g. cities on top of basemap with borough polygon data
    or Linestring for rivers on top of map with cities and borough boundaries.
    Parameters
    ----------
    layer_df:Geopandas DataFrame
    Contains geometry coordinate for layer to be added onto base
    ax: axes object for basemap
    base_df: Geopandas DataFrame
    Contains geometry coordinate for base layer. Requires to check CRS of new layer with this.
    Returns
    -------
    plot ax object with all layers
    """
    if base_df.crs != layer_df.crs:
        logger.info("layer df is not same projection as basemap so converting")
        layer_df = layer_df.set_crs(base_df.crs)
    new_ax = layer_df.plot(ax=ax, marker="o", color="red", markersize=5)
    logger.info("Plotting layer with coordinate points on basemap")
    return new_ax


def choloropeth_map(df, col):
    fig, ax = plt.subplots(1, 1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    return df.plot(
        column=col,
        ax=ax,
        legend=True,
        legend_kwds={"label": "Population by Country"},
        cax=cax,
    )
