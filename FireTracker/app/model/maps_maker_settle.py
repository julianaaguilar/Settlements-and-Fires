# Project: FIRE TRACKING
# Task: COMPILE INFORMATION OF SETTLEMENTS AND FIRES
# Team: JULIANA AGUILAR, LUCIA DELGADO AND JORGE QUINTERO

'''
MAIN OUTPUTS
- Clips GHSL raster at the country level
- Saves clip
- Saves image
'''
'''
This code generates an interactive map for one country including information 
about settled area at 1km buffer to each fire.

We generate a map for only one country, since GHSL data (raster data)
is only avaliable for some countries. This code is easily generalizable to
other countries.
'''

import folium
import geopandas as gpd
from pathlib import Path
from . import join_ras_shp
from . import maps_maker
import os

ROOT = str(Path(__file__).parents[1])
FILEPATH_O = os.path.join(ROOT,"data/GHSL")
FILEPATH_S = os.path.join(ROOT, "data/outfiles")
FILEPATH_W = os.path.join(ROOT, "maps")

def fire_settle(country):
	'''
	Assign share of settled area 0.7 km around the fire to each fire in a dynamic map.

	Input:
		country (str)
	'''

	# File paths
	file_geoj = country + ".geojson"
	out_geojson = os.path.join(FILEPATH_S, file_geoj)
	name_1 = country + "_buff_share.html"
	out_share = os.path.join(FILEPATH_W, name_1)
	name_2 = country + "_buff_settle.html"
	out_settle = os.path.join(FILEPATH_W, name_2)

	# Generate geojson
	if os.path.isfile(out_geojson) == False:
		join_ras_shp.share_settled(country)

	# Open data in GeoJson Format

	df = gpd.read_file(out_geojson) 
	geojson = out_geojson

	#Location
	location = maps_maker.get_coordinates(country)

	'''
	Map for all fires
	'''
	#Add fires and information
	map1 = folium.Map(location = location, zoom_start = 7)
	for i in range(len(df)):                                              
		lat = df.iat[i,11]  
		lon = df.iat[i,12] 
		info = "Date: " + str(df.iat[i,2]) + " Time: "  + str(df.iat[i,3]) + " Mean Settled: "  + str(df.iat[i,17])
		print(info)
		folium.CircleMarker(radius=5, location=[lat, lon], popup = info,
			fill_color='salmon', color='red',
			fill_opacity=0.8, line_opacity=0.8).add_to(map1)

	#Save map
	map1.save(outfile=out_share) 

	'''
	Map for fires close to settlements
	'''
	#Add fires and information
	map2 = folium.Map(location = location, zoom_start = 7)
	for i in range(len(df)):                                              
		if df.iat[i,17] > 0:
			lat = df.iat[i,11]  
			lon = df.iat[i,12] 
			info = "Date: " + str(df.iat[i,2]) + " Time: "  + str(df.iat[i,3]) + " Mean Settled: "  + str(df.iat[i,17])
			folium.CircleMarker(radius=5, location=[lat, lon], popup = info,
				fill_color='salmon', color='red',
				fill_opacity=0.8, line_opacity=0.8).add_to(map2)

	#Save map
	map2.save(outfile=out_settle)

	return out_share



