import sys
from unittest import mock

import pytest
from geopandas import GeoDataFrame
from geospatial.runners.crime_london import main
from matplotlib.pyplot import Axes


def test_crimes_london_runner_e2e():

    with mock.patch(
        "sys.argv", ["runner.py", "-shp=../data/ESRI/London_Borough_Excluding_MHW.shp"]
    ):
        result = main()
    assert isinstance(result[0], list)
    assert len(result[0]) == 62
    assert isinstance(result[1], GeoDataFrame)
    assert isinstance(result[2], Axes)
