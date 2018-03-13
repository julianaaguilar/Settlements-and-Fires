# Project: FIRE TRACKING
# Task: PROCESS GHSL RASTERS
# Team: JULIANA AGUILAR, LUCIA DELGADO AND JORGE QUINTERO

'''
MAIN OUTPUTS
- Clips GHSL raster at the country level
- Saves clip
- Saves image
'''

'''
THE DATA 

GHSL - Global Human Settlement Layers 

Downloaded from: 
   http://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_LDSMT_GLOBE_R2015B/GHS_BUILT_LDS2014_GLOBE_R2016A_54009_250/

These data contain an information layer on built-up 
presence as derived by the ad-hoc Landsat 8 collection 2013/2014.

Due to space constraints, continents where cut using ArcGIS.

Resolution: 250m of resolution
Year: 2014
Values: Values are expressed as decimals (Float) from 0 to 1
Projection: World Mollweide (EPSG:54009)
'''

'''
MAIN SOURCES OF CODE
https://mapbox.github.io/rasterio/intro.html
served as main source for this code 
'''


import rasterio
from rasterio.plot import show
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.transform import array_bounds
from rasterio import crs
from rasterio.crs import CRS

import cartopy.io.shapereader as shpreader
import geopandas as gpd
import fiona 

from matplotlib import pyplot

import numpy as np

import os
import math
from pathlib import Path

ROOT = str(Path(__file__).parents[1])
FILEPATH_O = os.path.join(ROOT,"data/GHSL")
FILEPATH_S = os.path.join(ROOT, "data/outfiles")
FILEPATH_W = os.path.join(ROOT, "maps")

def ghsl_country(country):
	'''
	Clips GHSL raster to country shape and prints.
	Inputs:
		country (str): country name

	Return: WSG84 bounds of image	
	'''
	# Shp with country boundaries and reproject to raster's projection
	country_shp = country_boundariesWSG84(country)

	# Get filename
	filen = country_shp.iloc[0]["CONTINENT"]

	# Changessss depending on country/ras
	#file_in = filen + "_GHSL.tif"
	file_in = "GHS_BUILT_LDS2014_GLOBE_R2016A_54009_250_v1_0.tif"
	file_out = country + "_ghsl.tif"
	file_out_png = country + "_ghsl.png"

	# Read raster
	file_ras = os.path.join(FILEPATH_O, file_in)
	out_ras = os.path.join(FILEPATH_S, file_out)
	out_png = os.path.join(FILEPATH_W, file_out_png)
	
	# Clip raster to country
	mosaic = rasterio.open(file_ras)
	out_ras = clipping(mosaic, country_shp, out_ras)

	# Print and export bounds
	map_c = rasterio.open(out_ras)

	profile = map_c.profile

	with rasterio.open(out_ras, 'w', **profile) as dst:
		dst.write(map_c)
	# bounds = boundsWSG84(map_c)

	print_ras(map_c, out_png)

	return out_png
 
def country_boundariesWSG84(country):
	'''
	Clips country boundaries from worldmap
	Input:
		country (str): country name
	Return: Geopandas dataframe with WSG84 projection
	'''
	resolution = '110m'
	category = 'cultural'
	name = 'admin_0_countries'

	world_shp = shpreader.natural_earth(resolution='110m', category='cultural', name='admin_0_countries')

	world_gpd = gpd.read_file(world_shp)

	world_clean = world_gpd[["ADMIN","geometry", "CONTINENT"]]

	country_shp = world_clean.loc[world_gpd['ADMIN'] == country]

	country_shp.crs = {'init': 'epsg:4326'}

	return country_shp

def getFeatures(gdf):
    '''
    Function to parse features from GeoDataFrame in such a manner that rasterio wants them
    From: https://automating-gis-processes.github.io/CSC18/lessons/L6/clipping-raster.html
    '''
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

def boundsWSG84(map_c, dst_crs='EPSG:4326'):
	'''
	Calculate bounds of projected image.
	Not in use.

	Inputs: 
		map_c: (rasterio._io.RasterReader) origin raster opened with rasterio
		out_ras: path to save reprojected raster
		dst_crs: destination coordinates system
	'''
	dst_crs = 'EPSG:4326'

	transform, width, height = calculate_default_transform(
		map_c.crs, dst_crs, map_c.width, map_c.height, *map_c.bounds)

	bounds = rasterio.transform.array_bounds(height, width, transform)

	return bounds

def clipping(ras, shp, out_ras):
	'''
	Clip raster to shapefile.
	'''
	# Reproject  country boundaries to raster's projection	
	dst_crs = ras.crs.data
	shp = shp.to_crs(dst_crs)

	coords = getFeatures(shp)

	out_img, out_transform = mask(raster=ras, shapes=coords, crop=True)
	out_meta = ras.meta.copy()

	out_meta.update({"driver": "GTiff", 
		"height": out_img.shape[1], 
		"width": out_img.shape[2], 
		"transform": out_transform, 
		"crs":dst_crs})

	with rasterio.open(out_ras, "w", **out_meta) as dest: 
		dest.write(out_img)

	return out_ras

def print_ras(map_c, out_png):
	'''
	Prints pretty maps based on raster. 
	Saves as image.
	Inputs:
		map_c: rasterio._io.RasterReader
		out_png: path to save raster
	'''

	fig, ax = pyplot.subplots(1)

	show(map_c, with_bounds=False, cmap="Reds", ax=ax)
	#pyplot.colorbar()
	ax.set_xticks([])
	ax.set_yticks([])
	ax.set_title("")
	ax.set_ylabel("")
	ax.spines['right'].set_visible(False)
	ax.spines['top'].set_visible(False)
	ax.spines['left'].set_visible(False)
	ax.spines['bottom'].set_visible(False)

	pyplot.savefig(out_png, bbox_inches='tight', transparent=True, dpi=150)


