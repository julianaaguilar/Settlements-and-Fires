# FIRE TRACKING
# Juliana Aguilar, Lucía Delgado, Jorge Quintero

import raster_ghsl as ghsl


import rasterio
from rasterio.plot import show
from rasterio.mask import mask

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

import os

FILEPATH = "/home/student/FireTracking/data/"
FILEPATH_S = "/home/student/FireTracking/data/outfiles"

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


def share_settled(country, buff_size=0.7, threshold=1):
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

	file_ras  = country + "_ghsl.tif"
	file_shp = "Fires_countries/colombia_shp.shp"

	# Create paths
	path_shp = os.path.join(FILEPATH, file_shp)
	path_ras = os.path.join(FILEPATH_S, file_ras)
	out_ras = os.path.join(FILEPATH_S, 'temp.tif')
	out_fires = os.path.join(FILEPATH_S, "firesplus.shp")

	# Open files
	fire = gpd.read_file(path_shp)
	settle = rasterio.open(path_ras)

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

	for i in range(len(buffers.index)):
		# defint temporal .tif file path
		
		b1 = buffers.loc[i:i]

		# Clip buffer to raster
		b1 = ghsl.clipping(settle, b1, out_ras)

		# Take mean of settlement values
		mean =  raster_mean(b1) 

		# Write mean into geopandas dataframe
		ind = buffers.loc[i, "index_righ"]
		fire.loc[fire["index_righ"] == ind, 'mean_settle'] = mean
		
		if mean >= threshold:
			fire.loc[fire["index_righ"] == ind, 'settled'] = 1
		else:
			fire.loc[fire["index_righ"] == ind, 'settled'] = 0

	fire.to_file(out_fires)

	return fire




