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



