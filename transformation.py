import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import pyproj

pd.set_option("display.max_columns", 15)


def check_epsg_code(str):
    """
    Returns epsg code for the proj string passed in
    Returns
    -------
    EPSG code

    """
    crs = pyproj.CRS(str)
    return crs.to_epsg()


def plot_basemap_from_shapefile(filepath, projection="mercrator"):
    """
    Plots basemap from shapefile
    Parameters
    ----------
    projection(Optional, Default:'mercractor': str, int
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
        data = data.set_crs("EPSG:3395")
    elif projection == "WGS84":
        data = data.set_crs("EPSG:4326")
    elif isinstance(projection, int):
        data = data.set_crs(f"EPSG:{projection}")
    ax = data.plot(figsize=(10, 10), alpha=0.5, color="wheat", edgecolor="black")
    ax.set_title(f"Basemap with {projection} projection")
    return data, ax


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


if __name__ == "__main__":
    london, ax = plot_basemap_from_shapefile(
        "data/ESRI/London_Borough_Excluding_MHW.shp"
    )
    print(london.head())
    plt.show()