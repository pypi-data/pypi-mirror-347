# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="tigris_cea",
    version="0.6",
    packages=find_packages(),
    install_requires=[
        'matplotlib>=3.8.4',
        'netCDF4>=1.7.2',
        'numpy>=2.2.5',
        'openpyxl>=3.1.5',
        'PyQt5>=5.15.11',
        'requests>=2.32.3',
        'shapely>=2.1.0',
        'vtk>=9.4.2'
    ],
    author="Julien TRINCAL",
    author_email="julien.trincal@cea.fr",
    description="Post-treatment of Porflow, Hytec, Min3P and Crunch simulations",
    license="none",
    keywords="Porflow, Hytec, Min3P, Crunch",
    url="https://github.com/julientrincal/Tigris",
)
