import argparse

import geopandas as gpd
from geospatial.io.api.call_api import get_request
from geospatial.io.api.crime import get_police_id, get_stop_search_by_force
from geospatial.plotting.geopandas_maps import (
    add_layer_to_plot,
    plot_basemap_from_shapefile,
)
from geospatial.spatial_transforms.transforms import response_to_gdf


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
    crime_ds = response_to_gdf(base_df, crime_london_json)
    crime_ds = gpd.sjoin(base_df, crime_ds, how="inner", op="intersects")
    ax = add_layer_to_plot(crime_ds, base_ax, base_df)
    return crime_london_json, base_df, ax


if __name__ == "__main__":
    _, _, ax = main()
