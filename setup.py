"""Setup script for tormetron"""

import os.path
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="tormetron",
    version="0.0.dev1",
    description="Download, save and process rainfall radar images from AEMET",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jlbmdm/tormetron",
    author="Bengoa",
    author_email="tratratron@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["tormetron"],
    include_package_data=True,
    install_requires=[
        "requests", "numpy", "gdal", "click"
    ],
    entry_points={"console_scripts": ["tormetron=tormetron.__main__:main"]},
)

#Aviso: para incluir la carpeta radardata y otros ficheros uso el MANIFEST.in en lugar de la linea:
#    package_data={'': ['README.md', 'LICENSE', 'tormetron/radardata']},
#Aunque mantengo la linea:
#    include_package_data=True,
#Ver:
# https://stackoverflow.com/questions/1612733/including-non-python-files-with-setup-py
# https://stackoverflow.com/questions/1471994/what-is-setup-py