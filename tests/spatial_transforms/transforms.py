import pandas as pd
from geopandas import GeoDataFrame
from geopandas.testing import assert_geodataframe_equal
from geospatial.spatial_transforms.transforms import merge_df
from shapely.geometry import Point


def test_merge_pd_gpd(sample_geodataframe, sample_dataframe):
    kwargs = {"on": "col"}
    gdf = sample_geodataframe.rename(columns={"value1": "col"})
    result = merge_df(gdf, sample_dataframe, strategy="attribute", **kwargs)
    expected_df = GeoDataFrame(
        [
            {"geometry": Point(x, y), "col": x, "value2": x, "value": x}
            for x, y in zip(range(10), range(10))
        ]
    )
    expected = expected_df.set_crs("epsg:4326")
    assert_geodataframe_equal(result, expected)


def test_sjoin(sample_geodataframe, sample_geoseries):

    gdf1 = sample_geodataframe.rename(columns={"value1": "col"})
    gdf2 = GeoDataFrame({"geometry": sample_geoseries})
    kwargs = {"how": "inner", "op": "intersects"}
    result = merge_df(gdf1, gdf2, strategy="spatial", **kwargs)
    expected_df = GeoDataFrame(
        {
            "geometry": [Point(0, 0), Point(1, 1)],
            "col": [0, 1],
            "value2": [0, 1],
            "index_right": [0, 0],
        }
    )
    expected = expected_df.set_crs("epsg:4326")
    assert_geodataframe_equal(result, expected)
