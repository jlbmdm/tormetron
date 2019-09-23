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
    version="0.0.1",
    description="Descarga, almacena y procesa info de radar de lluvias de AEMET",
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
#Ver:
# https://stackoverflow.com/questions/1612733/including-non-python-files-with-setup-py
# https://stackoverflow.com/questions/1471994/what-is-setup-py