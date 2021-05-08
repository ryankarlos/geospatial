import argparse
from argparse import Namespace

import matplotlib.pyplot as plt
from geospatial.io.api.crime import get_police_id, get_stop_search_by_force
from geospatial.logging_config import logging_config
from geospatial.plotting.geopandas_maps import (
    add_layer_to_plot,
    plot_basemap_from_shapefile,
)
from geospatial.spatial_transforms.transforms import merge_df, response_to_gdf
from geospatial.utils import set_working_dir_repo_root
from gevent import monkey as curious_george

# need to patch before importing function using grequests
# https://stackoverflow.com/questions/56309763/grequests-monkey-patch-warning
curious_george.patch_all(thread=False, select=False)

# fmt: off
from geospatial.io.api.call_api import get_request  # isort:skip # noqa E402

logger = logging_config("main")


def set_argparse_type(args: Namespace) -> Namespace:
    """
    Check if the str is digit - in case where crs
    number is passed either than string in which case
    convert it to int

    Parameters
    ----------
    args:Namespace

    Returns
    -------

    """

    if args.projection.isdigit():
        args.projection = int(args.projection)
    return args


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
        default="WGS84",
        help="the crs to be used when creating the basemap",
    )
    parser.add_argument(
        "-pol",
        "--police_force",
        type=str,
        default="City of London Police",
        help="The Police Force to get crime data from",
    )

    return set_argparse_type(parser.parse_args())


@set_working_dir_repo_root
def main():
    args = argparse_args()
    police_id = get_police_id(get_request, args.police_force)
    crime_london_json = get_stop_search_by_force(get_request, police_id, calls=30)
    base_df, base_ax = plot_basemap_from_shapefile(args.shapefile, args.projection)
    crime_ds = response_to_gdf(crime_london_json, base_df)
    kwargs = {"how": "right", "op": "intersects"}

    crime_ds = merge_df(base_df, crime_ds, strategy="spatial", **kwargs)
    # slice this as stray point in the corner of the plot outside map
    layer_df = crime_ds.cx[:, :51.8]
    ax = add_layer_to_plot(layer_df, base_ax, base_df)
    return crime_london_json, base_df, ax


if __name__ == "__main__":
    _, _, ax = main()
    plt.figure()
    plt.show()
