# Project: FIRE TRACKING
# Task: ESTIMATE SHARE OF SETTLED ARES AROUND FIRE
# Team: JULIANA AGUILAR, LUCIA DELGADO AND JORGE QUINTERO

'''
MAIN OUTPUTS:
- Shapefile with fires at the country level
- HTML Map
'''

import rasterio
from rasterio.plot import show
from rasterio.mask import mask

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

import os

from . import maps_maker
from . import raster_ghsl
#import maps_maker
#import raster_ghsl
from pathlib import Path

ROOT = str(Path(__file__).parents[1])
FILEPATH_O = os.path.join(ROOT,"data/GHSL")
FILEPATH_S = os.path.join(ROOT, "data/outfiles")
FILEPATH_W = os.path.join(ROOT, "maps")

def share_settled(country, buff_size=1, threshold=1):
	'''
	Creates buffers around the fires,  estimates the share of built-up area, 
	classifies the fire beign near settlements according to 
	the threshold: if share built-up >= threshold the fire has 1, 0 otherwise.

	Inputs:
		settle: raster opened in rasterio with settlements
		fire: shapefile with fires
		buff: size of the buffer in unit ?
		threshold: shatyre of settled territory considered as settled

	Return:
		(number of fires with settlements, number of fires, ratio)
	'''
	
	# Create paths
	file_ras  = country + "_ghsl.tif"
	file_geoj = country + ".geojson"
	path_ras = os.path.join(FILEPATH_S, file_ras)
	out_ras = os.path.join(FILEPATH_S, 'temp.tif')
	out_fires = os.path.join(FILEPATH_S, "firesplus.shp")
	out_geojson = os.path.join(FILEPATH_S, file_geoj)

	# Generate country ghsl raster
	#if os.path.isfile(path_ras) == False:
	#	raster_ghsl.ghsl_country(country)

	# Open files
	fire = maps_maker.get_points(country, start_date="2018-02-01", end_date="2018-03-13", confidence="normal", save = False, file_name = out_geojson)
	#settle = rasterio.open(path_ras)

	settle = raster_ghsl.ghsl_country(country, ras_reader=True)

	# Create buffers
	buffers = fire.copy(deep=True)
	buffers["geometry"] = buffers.geometry.buffer(buff_size)


	# Reproject geopandas dataframe to match raster's projection
	dst_crs = settle.crs.data
	buffers = buffers.to_crs(dst_crs)

	# Loop to take mean settlements by buffer
	# We have to loop because the getFeatures function doesn't work with the array
	fire['mean_settle'] = np.nan
	fire['settled'] = np.nan

	buffers.reset_index(drop=True, inplace=True)
	buffers.drop('geo', axis=1, inplace=True)
	buffers.columns

	for i in range(len(buffers.index)):
		# defint temporal .tif file path
		
		b1 = buffers.loc[i:i]
		print(b1)

		# Clip buffer to raster
		b1 = raster_ghsl.clipping(settle, b1, out_ras)

		# Take mean of settlement values
		mean =  raster_mean(b1) 

		# Write mean into geopandas dataframe
		ind = buffers.loc[i, "index_right"]
		fire.loc[fire["index_right"] == ind, 'mean_settle'] = mean
		
		if mean >= threshold:
			fire.loc[fire["index_right"] == ind, 'settled'] = 1
		else:
			fire.loc[fire["index_right"] == ind, 'settled'] = 0


	fire.drop('geo', axis=1, inplace=True)
	fire.set_index('geometry', drop=True, inplace=True)
	
	fire.to_file(filename = out_geojson, driver='GeoJSON')

	


def raster_mean(ras):
	'''
	Returns raster mean as a percentage.
	Inputs:
		ras: raster

	Return (float)	
	'''

	with rasterio.open(ras) as src:
	    array = src.read()

	# Values less than zero are missing
	array[array < 0] = 0

	mean = array.mean() * 100

	return mean

def thresh_settled(share_settle, threshold):
	if share_settle >= threshold:
		return 1
	else:
		return 0






