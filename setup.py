from setuptools import setup, find_packages

setup(
    name="Geospatial Analysis in Python",
    version="0.1",
    description="``geospatial librairy tutorials",
    author="Ryan Nazareth",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
)
