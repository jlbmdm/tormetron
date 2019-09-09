"""Setup script for tormetron"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="tormetron",
    version="1.0.0",
    description="Descarga, almacena y procesa info de radar de lluvias de AEMET",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jlbmdm/tormetron",
    author="Bengoa",
    author_email="tormetron@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["radarAEMET", "procesaRadar"],
    include_package_data=True,
    install_requires=[
        "requests", "numpy", "osgeo", "osgeo.gdal", "osgeo.gdalconst", "PIL" 
    ],
    entry_points={"console_scripts": ["tormetron=radarAEMET.__main__:main"]},
)
