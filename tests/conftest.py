import geopandas
import pandas as pd
import pytest
from geopandas import GeoDataFrame, GeoSeries
from shapely.geometry import Point, Polygon


@pytest.fixture(scope="session")
def sample_geoseries():
    polygon = [Polygon([(0, 0), (1, 0), (1, 1)])]
    return GeoSeries(polygon)


@pytest.fixture()
def sample_geodataframe():
    N = 10
    crs = "epsg:4326"
    df = GeoDataFrame(
        [
            {"geometry": Point(x, y), "value1": x, "value2": y}
            for x, y in zip(range(N), range(N))
        ],
        crs=crs,
    )

    return df


@pytest.fixture(scope="session")
def sample_dataframe():
    N = 10
    return pd.DataFrame([{"col": x, "value": y} for x, y in zip(range(10), range(10))])
