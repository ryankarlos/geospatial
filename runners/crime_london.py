from plotting.geopandas_maps import plot_basemap_from_shapefile
import matplotlib.pyplot as plt


def main():
    london, ax = plot_basemap_from_shapefile(
        "../data/ESRI/London_Borough_Excluding_MHW.shp"
    )
    print(london.head())
    plt.show()


if __name__ == "__main__":
    main()
