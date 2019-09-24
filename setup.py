"""Setup script for tormetron"""

import os.path
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="tormetron",
    version="0.0.dev2",
    description="Download, save and process rainfall radar images from AEMET",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jlbmdm/tormetron",
    author="Bengoa",
    author_email="tratratron@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Spanish",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    packages=["tormetron"],
    include_package_data=True,
    install_requires=[
        "requests", "numpy", "gdal", "click"
    ],
    entry_points={"console_scripts": ["tormetron=tormetron.__main__:main"]},
)
#Para classifiers, ver https://pypi.org/pypi?%3Aaction=list_classifiers

#Aviso: para incluir la carpeta radardata y otros ficheros uso el MANIFEST.in en lugar de la linea:
#    package_data={'': ['README.md', 'LICENSE', 'tormetron/radardata']},
#Aunque mantengo la linea:
#    include_package_data=True,
#Ver:
# https://stackoverflow.com/questions/1612733/including-non-python-files-with-setup-py
# https://stackoverflow.com/questions/1471994/what-is-setup-py