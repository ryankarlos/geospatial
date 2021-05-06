from plotting.geopandas_maps import plot_basemap_from_shapefile
import matplotlib.pyplot as plt
import argparse


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
    args = parser.parse_args()
    return args


def main():
    args = argparse_args()
    london, ax = plot_basemap_from_shapefile(args.shapefile, args.projection)
    plt.show()


if __name__ == "__main__":
    main()
