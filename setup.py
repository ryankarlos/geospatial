from setuptools import setup, find_packages


# Get the long description from the README file
with open('README.md') as f:
    long_description = f.read()

if __name__ == "__main__":
    setup(
        name="Geospatial Analysis in Python",
        version="0.1",
        description="``geospatial librairy tutorials",
        long_description=long_description,
        author="Ryan Nazareth",
        packages=find_packages(exclude=["tests", "data/ESRI"]),
        project_urls={'Source': 'https://github.com/ryankarlos/Geospatial'},
        python_requires='>=3.9',
    )
