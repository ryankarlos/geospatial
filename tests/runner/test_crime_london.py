import sys
from argparse import Namespace
from unittest import mock

import pytest
from geopandas import GeoDataFrame
from geospatial.runners.crime_london import argparse_args, main
from matplotlib.pyplot import Axes


@pytest.mark.parametrize(
    "input,expected",
    [
        (
            ["runner.py", "-shp=data/ESRI/London_Borough_Excluding_MHW.shp"],
            Namespace(
                police_force="City of London Police",
                projection="mercrator",
                shapefile="data/ESRI/London_Borough_Excluding_MHW.shp",
            ),
        ),
        (
            [
                "runner.py",
                "-shp=data/ESRI/London_Borough_Excluding_MHW.shp",
                "--proj=WGS84",
                "--pol=Somerset and Avon",
            ],
            Namespace(
                police_force="Somerset and Avon",
                projection="WGS84",
                shapefile="data/ESRI/London_Borough_Excluding_MHW.shp",
            ),
        ),
    ],
)
def test_argparse(input, expected):
    # set command line args with required arg
    sys.argv = input
    args = argparse_args()
    assert args == expected


def test_crimes_london_runner_e2e():

    with mock.patch(
        "sys.argv",
        [
            "runner.py",
            "-shp=data/ESRI/London_Borough_Excluding_MHW.shp",
            "--police_force=City of London Police",
        ],
    ):
        result = main()
    assert isinstance(result[0], list)
    assert len(result[0]) == 62
    assert isinstance(result[1], GeoDataFrame)
    assert isinstance(result[2], Axes)
