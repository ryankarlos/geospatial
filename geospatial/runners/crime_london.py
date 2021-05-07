import argparse

import geopandas as gpd
import pandas as pd
from geospatial.io.api.call_api import get_request
from geospatial.io.api.crime import get_police_id, get_stop_search_by_force
from geospatial.plotting.geopandas_maps import (
    add_layer_to_plot,
    plot_basemap_from_shapefile,
)


def argparse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-shp",
        "--shapefile",
        type=str,
        required=True,
        help="path to the shapefile for generating the basemap",
    )
    parser.add_argument(
        "-proj",
        "--projection",
        type=str,
        default="mercrator",
        help="the crs to be used when creating the basemap",
    )
    parser.add_argument(
        "-pol",
        "--police_force",
        type=str,
        default="City of London Police",
        help="The Police Force to get crime data from",
    )
    args = parser.parse_args()
    return args


def main():
    args = argparse_args()
    police_id = get_police_id(get_request, args.police_force)
    crime_london_json = get_stop_search_by_force(get_request, police_id)
    base_df, base_ax = plot_basemap_from_shapefile(args.shapefile, args.projection)
    crime = pd.DataFrame(crime_london_json)
    crime["latitude"] = crime["location"].map(lambda x: float(x["latitude"]))
    crime["longitude"] = crime["location"].map(lambda x: float(x["longitude"]))
    crime_ds = gpd.GeoDataFrame(
        crime, geometry=gpd.points_from_xy(crime["longitude"], crime["latitude"])
    )
    crime_ds = crime_ds.set_crs(base_df.crs)
    crime_ds = gpd.sjoin(base_df, crime_ds, how="inner", op="intersects")
    ax = add_layer_to_plot(crime_ds, base_ax, base_df)
    return crime_london_json, base_df, ax


if __name__ == "__main__":
    _, _, ax = main()
