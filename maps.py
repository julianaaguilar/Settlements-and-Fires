# TASK: Fire Data to Output
# Fire Tracker Team
# Lucia Delgado
# Last modified: March 7, 2018 

'''
GOAL OF THIS CODE

Provided:
	country
	date_frame
	confidence

Generate:
	shapefile
	map
'''


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
import data_downloader


'''
NOTE ON FIRE DATA:

*We use fire points identified by NASA using satelite images
from two satelites: Modis and Viirs.

*Geographic WGS84 projection

*Data obtained from 
https://earthdata.nasa.gov/earth-observation-data
/near-real-time/firms/active-fire-data

*A data base for each region is being updated dayly. 
'''

'''
STEPS:
1. Find region of country
2. Merge info from two satelites
3. Select info for country
4. Select dates
5. Select quality
6. Generate file
7. Generate Map
'''


def draw_map (country, start_date, end_date, confidence):

	#Generate file with the plots that we want to draw
	get_points(country, start_date, end_date, confidence, 
	save = True, file_name = "output.geojson")

	# Call data
	df = gpd.read_file('output.geojson') 
	geojson = r'output.geojson'

	# Get location
	#NOTE: we need a dictionaty to map country to location
	#Location for Colombia
	location = [4.60971, -74.08175]

	#Features added
	outmap = folium.Map(location = location, zoom_start = 7)
	for i in range(len(df)):                                              
		lat = df.iat[i,9]  
		lon = df.iat[i,10] 
		folium.CircleMarker(radius=5, location=[lat, lon],
			fill_color='salmon', color='red',
			fill_opacity=0.8, line_opacity=0.8).add_to(outmap)

	outmap.save(outfile='outmap.html') 
	return outmap

	'''
	#Add features practice
	map3 = folium.Map(location = location, zoom_start = 7)

	folium.CircleMarker(radius=3, location=[4.50642, -69.53278], 
	fill_color='salmon', color='red',
	fill_opacity=0.8, line_opacity=0.8).add_to(map3)
	map3.save(outfile='map3.html') 
	''' 



def get_points (country, start_date, end_date, confidence, 
	save = False, file_name = "output.geojson"):
	'''
	This function gets a country and a time frame, 
	and returs a GeoDataFrame with the fire data
	for the desired country and data frame.
	
	Inputs:
		country: string
		start_date: (string with format 2018-02-26) 
		end_date: (string with format 2018-02-26)
		confidence: "normal", "low", "high"
		save: boolean, saves to json and shp
		file_name: string
	Returns geopandas data frame
	'''

	# 1. Identigy region of the country:
	region = country_to_region(country)

	#2. Get files
	'''
	For this part we need to match each region to file
	Check with Jorge

	There will be two shapefiles per region
	A dictionary matchin region to modis and viirs file
	'''
	#modis = "nasa_data/region/MODIS_C6_Central_America_7d.shp"
	#viirs = "nasa_data/region/VNP14IMGTDL_NRT_Central_America_7d.shp"


	modis = data_downloader.selector(region, "MODIS")
	#modis = "nasa_data/southamerica/MODIS_C6_South_America_7d.shp"
	
	viirs =  data_downloader.selector(region, "VIIRS")
	#viirs = "nasa_data/southamerica/VNP14IMGTDL_NRT_South_America_7d.shp"

	#3. Combine shapefiles
	mv =  combine_shapefiles(modis, viirs)

	#4. Filter by country
	country_points = clip_fire_country(country, mv)

	#5. Filter by time
	country_time = time_filter(country_points, start_date, end_date)
	#country_time.plot()
	#plt.show()

	#6. Filter by confidence
	country_time.CONFIDENCE = country_time.CONFIDENCE.apply(lambda val: 
		str(val))
	filter_confidence = country_time.CONFIDENCE == confidence 
	country_filtered = country_time[filter_confidence]

	if len(country_filtered) == 0:
		return "No data matching this request"

	#7. Save
	if save == True:
		country_filtered.drop("geo", axis = 1, inplace = True )
		#country_filtered.to_file(filename = filename + "_shp, 
		#	driver='ESRI Shapefile')
		if os.path.isfile(file_name) == True:
			os.remove(file_name)
		country_filtered.to_file(filename = file_name, 
			driver='GeoJSON')

	return country_filtered


def combine_shapefiles(modis, viirs):
	'''
	This function takes as an argument the location of two
	shape files and returns a shapefile compining both
	Inputs
		modis: string
		viirs: string
	Returs: geopandas dataframe
	'''
	# READ FILES
	#modis = "nasa_data/MODIS_C6_Global_7d.shp"
	#viirs = "nasa_data/VNP14IMGTDL_NRT_Global_7d.shp"

	#modis = "nasa_data/region/MODIS_C6_Central_America_7d.shp"
	#viirs = "nasa_data/region/VNP14IMGTDL_NRT_Central_America_7d.shp"
				
	m = gpd.read_file(modis)
	v = gpd.read_file(viirs)

	# DATA REVIEW
	type(m)
	type(v)
	m.head()
	v.head()

	#reference system
	m.crs #empty
	v.crs

	#Since projection is empty, we set 
	#set projection to WGS84:
	m.crs = {'init': 'epsg:4326'}
	v.crs = {'init': 'epsg:4326'}

	#Combine both shapefiles
	mv = gpd.GeoDataFrame( pd.concat( [m,v] , ignore_index=True) )

	#Plot
	#mv.plot()
	#plt.show()

	return mv

def country_to_region(country):
	'''
	This function gets a country and returs the region 
	that the country belongs to.
	Input: 
		country (string)
	Output: 
		region (string)
	'''
	country_to_reg = {'Afghanistan': 'South Asia',
	 'Algeria': 'North and Central Africa',
	 'Angola': 'North and Central Africa',
	 'Argentina': 'South America',
	 'Armenia': 'Russia and Asia',
	 'Australia': 'Australia and New Zealand',
	 'Austria': 'Europe',
	 'Azerbaijan': 'Russia and Asia',
	 'Bangladesh': 'South Asia',
	 'Belgium': 'Europe',
	 'Belize': 'Central America',
	 'Benin': 'North and Central Africa',
	 'Bhutan': 'South Asia',
	 'Bolivia': 'South America',
	 'Bosnia and Herzegovina': 'Europe',
	 'Botswana': 'Southern Africa',
	 'Brazil': 'South America',
	 'Brunei': 'South East Asia',
	 'Bulgaria': 'Europe',
	 'Burkina Faso': 'North and Central Africa',
	 'Burundi': 'North and Central Africa',
	 'Cambodia': 'South East Asia',
	 'Cameroon': 'North and Central Africa',
	 'Canada': 'Canada',
	 'Central African Republic': 'North and Central Africa',
	 'Chad': 'North and Central Africa',
	 'Chile': 'South America',
	 'China': 'South Asia',
	 'Colombia': 'Central America',
	 'Costa Rica': 'Central America',
	 'Croatia': 'Europe',
	 'Cuba': 'Central America',
	 'Cyprus': 'North and Central Africa',
	 'Czechia': 'Europe',
	 'Democratic Republic of the Congo': 'North and Central Africa',
	 'Denmark': 'Europe',
	 'Dominican Republic': 'Central America',
	 'Ecuador': 'South America',
	 'Egypt': 'North and Central Africa',
	 'El Salvador': 'Central America',
	 'Equatorial Guinea': 'North and Central Africa',
	 'Eritrea': 'North and Central Africa',
	 'Ethiopia': 'North and Central Africa',
	 'France': 'Europe',
	 'Gabon': 'North and Central Africa',
	 'Gambia': 'North and Central Africa',
	 'Georgia': 'Russia and Asia',
	 'Germany': 'Europe',
	 'Ghana': 'North and Central Africa',
	 'Greece': 'Europe',
	 'Guatemala': 'Central America',
	 'Guinea': 'North and Central Africa',
	 'Guinea-Bissau': 'North and Central Africa',
	 'Guyana': 'Central America',
	 'Haiti': 'Central America',
	 'Honduras': 'Central America',
	 'Hungary': 'Europe',
	 'India': 'South Asia',
	 'Indonesia': 'South East Asia',
	 'Iran': 'North and Central Africa',
	 'Iraq': 'North and Central Africa',
	 'Ireland': 'Europe',
	 'Israel': 'North and Central Africa',
	 'Italy': 'North and Central Africa',
	 'Ivory Coast': 'North and Central Africa',
	 'Jamaica': 'Central America',
	 'Japan': 'Russia and Asia',
	 'Jordan': 'North and Central Africa',
	 'Kazakhstan': 'Russia and Asia',
	 'Kenya': 'North and Central Africa',
	 'Kuwait': 'North and Central Africa',
	 'Kyrgyzstan': 'Russia and Asia',
	 'Laos': 'South Asia',
	 'Liberia': 'North and Central Africa',
	 'Libya': 'North and Central Africa',
	 'Luxembourg': 'Europe',
	 'Macedonia': 'Europe',
	 'Madagascar': 'Southern Africa',
	 'Malawi': 'Southern Africa',
	 'Malaysia': 'South Asia',
	 'Mali': 'North and Central Africa',
	 'Mauritania': 'North and Central Africa',
	 'Mexico': 'Central America',
	 'Moldova': 'Europe',
	 'Morocco': 'North and Central Africa',
	 'Mozambique': 'Southern Africa',
	 'Myanmar': 'South Asia',
	 'Namibia': 'Southern Africa',
	 'Nepal': 'South Asia',
	 'Netherlands': 'Europe',
	 'New Caledonia': 'Australia and New Zealand',
	 'New Zealand': 'Australia and New Zealand',
	 'Nicaragua': 'Central America',
	 'Niger': 'North and Central Africa',
	 'Nigeria': 'North and Central Africa',
	 'North Korea': 'Russia and Asia',
	 'Northern Cyprus': 'North and Central Africa',
	 'Norway': 'Europe',
	 'Oman': 'South Asia',
	 'Pakistan': 'South Asia',
	 'Palestine': 'North and Central Africa',
	 'Panama': 'Central America',
	 'Papua New Guinea': 'Australia and New Zealand',
	 'Paraguay': 'South America',
	 'Peru': 'South America',
	 'Philippines': 'South East Asia',
	 'Poland': 'Europe',
	 'Portugal': 'Europe',
	 'Puerto Rico': 'Central America',
	 'Qatar': 'North and Central Africa',
	 'Republic of Serbia': 'Europe',
	 'Republic of the Congo': 'North and Central Africa',
	 'Romania': 'Europe',
	 'Russia': 'Europe',
	 'Saudi Arabia': 'North and Central Africa',
	 'Senegal': 'North and Central Africa',
	 'Sierra Leone': 'North and Central Africa',
	 'Slovakia': 'Europe',
	 'Solomon Islands': 'South East Asia',
	 'Somalia': 'North and Central Africa',
	 'Somaliland': 'North and Central Africa',
	 'South Africa': 'Southern Africa',
	 'South Korea': 'Russia and Asia',
	 'South Sudan': 'North and Central Africa',
	 'Spain': 'North and Central Africa',
	 'Sri Lanka': 'South Asia',
	 'Sudan': 'North and Central Africa',
	 'Suriname': 'South America',
	 'Swaziland': 'Southern Africa',
	 'Sweden': 'Europe',
	 'Syria': 'North and Central Africa',
	 'Taiwan': 'South East Asia',
	 'Tajikistan': 'South Asia',
	 'Thailand': 'South Asia',
	 'The Bahamas': 'Central America',
	 'Togo': 'North and Central Africa',
	 'Trinidad and Tobago': 'Central America',
	 'Tunisia': 'North and Central Africa',
	 'Turkey': 'North and Central Africa',
	 'Turkmenistan': 'South Asia',
	 'Uganda': 'North and Central Africa',
	 'Ukraine': 'Europe',
	 'United Arab Emirates': 'South Asia',
	 'United Kingdom': 'Europe',
	 'United Republic of Tanzania': 'North and Central Africa',
	 'United States of America': 'Central America',
	 'Uruguay': 'South America',
	 'Uzbekistan': 'South Asia',
	 'Venezuela': 'Central America',
	 'Vietnam': 'South East Asia',
	 'Yemen': 'North and Central Africa',
	 'Zambia': 'North and Central Africa',
	 'Zimbabwe': 'Southern Africa'}
		
	return country_to_reg[country]


def clip_fire_country(country, fire_data):
	'''
	This function takes a country and a fire_data set and returs a 
	geopandas data frame containning the fire_data for the country
	Inputs:
		country: string
		fire_data: geopandas dataframe
	Returns: Data frame
	'''
	mv = fire_data

	#Get world polygon:

	resolution = '110m'
	category = 'cultural'
	name = 'admin_0_countries'
	world_shp = shpreader.natural_earth(resolution, category, name)

	# Read the world shapefile using geopandas
	world_gpd = gpd.read_file(world_shp)

	#Prepare world data (clean)
	world_gpd.columns
	world_clean = world_gpd[["ADMIN","geometry"]]

	#Prepare fire data (Save points geometry in a variable)
	mv1 = mv
	mv1[["geo"]] = mv1[["geometry"]]

	#CRS must match
	world_clean.crs == mv1.crs
	mv1.crs = {'init': 'epsg:4326'}
	world_clean.crs = {'init': 'epsg:4326'}

	#Join fire data to world
	points_world = gpd.sjoin(world_clean, mv1, how="inner", op='intersects')
	#Load geometry from fire data
	points_world[["geometry"]] = points_world[["geo"]]

	#Country selection
	#colo
	#country = "Mexico"
	selection = points_world.loc[world_gpd['ADMIN'] == country]

	#Plot>
	country_border = world_gpd.loc[world_gpd['ADMIN'] == country]
	base = country_border.plot(color='white', edgecolor='black')
	selection.plot(ax = base,color='red' ) 
	#plt.show()

	return selection


def time_filter(country_points, start_date, end_date):
	'''
	This function takes a geopandas data frame and a 
	start and end date. Returns a filtered data frame for the desired 
	time frame.
	Inputs:
		country_points (geopandas data frame)
		start_date (string)
		end_date (string)
	Returns> geopandas data frame
	'''

	filter_lower = country_points.ACQ_DATE >= start_date 
	on_date = country_points[filter_lower]

	filter_upper = on_date.ACQ_DATE <= end_date
	on_date = on_date[filter_upper]

	return on_date

#http://scitools.org.uk/cartopy/docs/v0.15/matplotlib/intro.html
#https://automating-gis-processes.github.io/2016/Lesson3-spatial-join.html