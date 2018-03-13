# Project
FIRE TRACKING

Team: JULIANA AGUILAR, LUCIA DELGADO AND JORGE QUINTERO

Objectives and description: 
● Provide an interactive platform that allows fire tracking around
the globe with updated information.
● Identify fires that are within a certain radius of human
settlements.

For further understanding open "Tracking fires worldwide.pdf", it contains the main information about the project.  


# Data
1. Fires worldwide
We use fire points identified by NASA using satelite images
from two satelites: Modis and Viirs.

Data obtained from 
https://earthdata.nasa.gov/earth-observation-data
/near-real-time/firms/active-fire-data

2. Settlements
We use Global Human Settlement Layers (GHSL). These data contain an information layer on built-up 
presence as derived by the ad-hoc Landsat 8 collection 2013/2014. 

Downloaded from: 
   http://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_LDSMT_GLOBE_R2015B/GHS_BUILT_LDS2014_GLOBE_R2016A_54009_250/

Resolution: 250m of resolution
Year: 2014


# What you should know about the files
The files we use in this project are heavy, and can't be uploaded to github.

We put a small sample in github, but the complete set of files can be downloaded from this link:


# Running the web-pag: Instructions
1. Change your directory to "/Fire-database/Firetracker/" 
2. Install pipenv using
2. Run $ pipenv install
3. Run $ FLASK_APP=run.py pipenv run flask run
4. Open your favourite browser and go to the path indicated by the python console



# Fires_database

The Following Libraries are Needed:

	To run data_downloader.py
		import re
		import bs4
		import json
		import sys
		import csv
		import urllib
		import util
		import os.path
		import datetime
		from os.path import join as pjoin
		import time
		import zipfile
		from os import listdir
		from os.path import isfile, join
		import geopandas as gpd
		import pandas as pd
		import urllib.parse

	To run map_maker:
		import rtree
		import fiona
		import geopandas as gpd
		import matplotlib.pyplot as plt
		import shapefile
		import pandas as pd
		import cartopy
		import cartopy.io.shapereader as shpreader
		import folium
		import os
		from pathlib import Path


# Data sources:

	Main data source 1 - NASA | Satellite imaginery of fires: https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms/active-fire-data

	Main data source 2 - XXX | Human settlements data: 


# Main Code Descriptions:

	data_downloader.py:
		Downloads data from Nasa's website and stores it as regional archives.

	maps_maker.py: 
		Draws a map of a specified region, confidence level and time frame. Stores it as html object

# Auxiliary code:

	util.py: 
		File form PS2 we used to build soups. We didnt change it.

	aux_country_to_coordinates.py:
		Generates a dictionary that maps countries to central coordinates
	
	aux_dictionar_regions.py:
		Generates a dictionary that maps countries to regions



