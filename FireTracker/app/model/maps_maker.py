# Project: FIRE TRACKING
# Task: PROCESS FIRE DATA AND PRODUCE DYNAMIC MAP
# Team: JULIANA AGUILAR, LUCIA DELGADO AND JORGE QUINTERO

'''
MAIN OUTPUTS:
- Shapefile with fires at the country level
- HTML Map
'''
'''
THE DATA:

We use fire points identified by NASA using satelite images
from two satelites: Modis and Viirs.

Data obtained from 
https://earthdata.nasa.gov/earth-observation-data
/near-real-time/firms/active-fire-data

A data base for each region can be updated dayly using data_downloader.py 

Format: ESRI Shapefile
Projection: WGS84, (EPSG:4326)
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
from . import data_downloader
#import data_downloader
from pathlib import Path

ROOT = Path(__file__).parents[1]
OUT_GEOJSON = os.path.join(str(ROOT), "data/outfiles/output.geojson")


def draw_map (country, start_date, end_date, confidence):
	'''
	This function gets a country and a time frame, 
	and confidence and returs a MAP
	
	Inputs:
		country: string
		start_date: (string with format 2018-02-26) 
		end_date: (string with format 2018-02-26)
		confidence: "normal", "low", "high"
		
	Returns: HTML Map
	'''
	name_ = "maps/" + country + ".html"
	name = os.path.join(str(ROOT), name_)
	
	print(OUT_GEOJSON)

	#Generate file with the plots that we want to draw
	get_points(country, start_date, end_date, confidence, 
	save = True, file_name = OUT_GEOJSON)

	# Call data
	df = gpd.read_file(OUT_GEOJSON) 
	geojson = OUT_GEOJSON

	# Get location
	location = get_coordinates(country)

	#Features added
	outmap = folium.Map(location = location, zoom_start = 4)
	for i in range(len(df)):                                              
		lat = df.iat[i,9]  
		lon = df.iat[i,10] 
		info = "Date: " + str(df.iat[i,2]) + " Time: "  + str(df.iat[i,2])
		folium.CircleMarker(radius=5, location=[lat, lon], popup = info,
			fill_color='salmon', color='red',
			fill_opacity=0.8, line_opacity=0.8).add_to(outmap)
	
	outmap.save(outfile=name) 
	return name


def get_points (country, start_date, end_date, confidence, 
	save = True, file_name = OUT_GEOJSON):
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
	There will be two shapefiles per region
	A dictionary matchin region to modis and viirs file
	'''

	#modis = data_downloader.selector(region, "MODIS")	
	#viirs =  data_downloader.selector(region, "VIIRS")

	modis = os.path.join(str(ROOT), "data/fires_regions/MODIS_C6_South_America_archive.shp")
	viirs = os.path.join(str(ROOT),"data/fires_regions/VNP14IMGTDL_NRT_South_America_archive.shp")


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
	 'Colombia': 'South America',
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

def get_coordinates(country):
	'''
	This function takes a country and returns central coordinates
	in the form [latitute, longitude]

	Inputs: country(string)
	Returns: list
	'''

	'''
	NOTE:
	This dictionary maps all countries to center coordinates. 
	Latitude and Longiture

	Source: 
	https://developers.google.com/public-data/docs/canonical/countries_csv
	'''

	coordinates = {
	"Andorra"	:	[	42.546245	,	1.601554	],
	"United Arab Emirates"	:	[	23.424076	,	53.847818	],
	"Afghanistan"	:	[	33.93911	,	67.709953	],
	"Antigua and Barbuda"	:	[	17.060816	,	-61.796428	],
	"Anguilla"	:	[	18.220554	,	-63.068615	],
	"Albania"	:	[	41.153332	,	20.168331	],
	"Armenia"	:	[	40.069099	,	45.038189	],
	"Netherlands Antilles"	:	[	12.226079	,	-69.060087	],
	"Angola"	:	[	-11.202692	,	17.873887	],
	"Antarctica"	:	[	-75.250973	,	-0.071389	],
	"Argentina"	:	[	-38.416097	,	-63.616672	],
	"American Samoa"	:	[	-14.270972	,	-170.132217	],
	"Austria"	:	[	47.516231	,	14.550072	],
	"Australia"	:	[	-25.274398	,	133.775136	],
	"Aruba"	:	[	12.52111	,	-69.968338	],
	"Azerbaijan"	:	[	40.143105	,	47.576927	],
	"Bosnia and Herzegovina"	:	[	43.915886	,	17.679076	],
	"Barbados"	:	[	13.193887	,	-59.543198	],
	"Bangladesh"	:	[	23.684994	,	90.356331	],
	"Belgium"	:	[	50.503887	,	4.469936	],
	"Burkina Faso"	:	[	12.238333	,	-1.561593	],
	"Bulgaria"	:	[	42.733883	,	25.48583	],
	"Bahrain"	:	[	25.930414	,	50.637772	],
	"Burundi"	:	[	-3.373056	,	29.918886	],
	"Benin"	:	[	9.30769	,	2.315834	],
	"Bermuda"	:	[	32.321384	,	-64.75737	],
	"Brunei"	:	[	4.535277	,	114.727669	],
	"Bolivia"	:	[	-16.290154	,	-63.588653	],
	"Brazil"	:	[	-14.235004	,	-51.92528	],
	"Bahamas"	:	[	25.03428	,	-77.39628	],
	"Bhutan"	:	[	27.514162	,	90.433601	],
	"Bouvet Island"	:	[	-54.423199	,	3.413194	],
	"Botswana"	:	[	-22.328474	,	24.684866	],
	"Belarus"	:	[	53.709807	,	27.953389	],
	"Belize"	:	[	17.189877	,	-88.49765	],
	"Canada"	:	[	56.130366	,	-106.346771	],
	"Cocos [Keeling] Islands"	:	[	-12.164165	,	96.870956	],
	"Congo [DRC]"	:	[	-4.038333	,	21.758664	],
	"Central African Republic"	:	[	6.611111	,	20.939444	],
	"Congo [Republic]"	:	[	-0.228021	,	15.827659	],
	"Switzerland"	:	[	46.818188	,	8.227512	],
	"Côte d'Ivoire"	:	[	7.539989	,	-5.54708	],
	"Cook Islands"	:	[	-21.236736	,	-159.777671	],
	"Chile"	:	[	-35.675147	,	-71.542969	],
	"Cameroon"	:	[	7.369722	,	12.354722	],
	"China"	:	[	35.86166	,	104.195397	],
	"Colombia"	:	[	4.570868	,	-74.297333	],
	"Costa Rica"	:	[	9.748917	,	-83.753428	],
	"Cuba"	:	[	21.521757	,	-77.781167	],
	"Cape Verde"	:	[	16.002082	,	-24.013197	],
	"Christmas Island"	:	[	-10.447525	,	105.690449	],
	"Cyprus"	:	[	35.126413	,	33.429859	],
	"Czech Republic"	:	[	49.817492	,	15.472962	],
	"Germany"	:	[	51.165691	,	10.451526	],
	"Djibouti"	:	[	11.825138	,	42.590275	],
	"Denmark"	:	[	56.26392	,	9.501785	],
	"Dominica"	:	[	15.414999	,	-61.370976	],
	"Dominican Republic"	:	[	18.735693	,	-70.162651	],
	"Algeria"	:	[	28.033886	,	1.659626	],
	"Ecuador"	:	[	-1.831239	,	-78.183406	],
	"Estonia"	:	[	58.595272	,	25.013607	],
	"Egypt"	:	[	26.820553	,	30.802498	],
	"Western Sahara"	:	[	24.215527	,	-12.885834	],
	"Eritrea"	:	[	15.179384	,	39.782334	],
	"Spain"	:	[	40.463667	,	-3.74922	],
	"Ethiopia"	:	[	9.145	,	40.489673	],
	"Finland"	:	[	61.92411	,	25.748151	],
	"Fiji"	:	[	-16.578193	,	179.414413	],
	"Falkland Islands [Islas Malvinas]"	:	[	-51.796253	,	-59.523613	],
	"Micronesia"	:	[	7.425554	,	150.550812	],
	"Faroe Islands"	:	[	61.892635	,	-6.911806	],
	"France"	:	[	46.227638	,	2.213749	],
	"Gabon"	:	[	-0.803689	,	11.609444	],
	"United Kingdom"	:	[	55.378051	,	-3.435973	],
	"Grenada"	:	[	12.262776	,	-61.604171	],
	"Georgia"	:	[	42.315407	,	43.356892	],
	"French Guiana"	:	[	3.933889	,	-53.125782	],
	"Guernsey"	:	[	49.465691	,	-2.585278	],
	"Ghana"	:	[	7.946527	,	-1.023194	],
	"Gibraltar"	:	[	36.137741	,	-5.345374	],
	"Greenland"	:	[	71.706936	,	-42.604303	],
	"Gambia"	:	[	13.443182	,	-15.310139	],
	"Guinea"	:	[	9.945587	,	-9.696645	],
	"Guadeloupe"	:	[	16.995971	,	-62.067641	],
	"Equatorial Guinea"	:	[	1.650801	,	10.267895	],
	"Greece"	:	[	39.074208	,	21.824312	],
	"South Georgia and the South Sandwich Islands"	:	[	-54.429579	,	-36.587909	],
	"Guatemala"	:	[	15.783471	,	-90.230759	],
	"Guam"	:	[	13.444304	,	144.793731	],
	"Guinea-Bissau"	:	[	11.803749	,	-15.180413	],
	"Guyana"	:	[	4.860416	,	-58.93018	],
	"Gaza Strip"	:	[	31.354676	,	34.308825	],
	"Hong Kong"	:	[	22.396428	,	114.109497	],
	"Heard Island and McDonald Islands"	:	[	-53.08181	,	73.504158	],
	"Honduras"	:	[	15.199999	,	-86.241905	],
	"Croatia"	:	[	45.1	,	15.2	],
	"Haiti"	:	[	18.971187	,	-72.285215	],
	"Hungary"	:	[	47.162494	,	19.503304	],
	"Indonesia"	:	[	-0.789275	,	113.921327	],
	"Ireland"	:	[	53.41291	,	-8.24389	],
	"Israel"	:	[	31.046051	,	34.851612	],
	"Isle of Man"	:	[	54.236107	,	-4.548056	],
	"India"	:	[	20.593684	,	78.96288	],
	"British Indian Ocean Territory"	:	[	-6.343194	,	71.876519	],
	"Iraq"	:	[	33.223191	,	43.679291	],
	"Iran"	:	[	32.427908	,	53.688046	],
	"Iceland"	:	[	64.963051	,	-19.020835	],
	"Italy"	:	[	41.87194	,	12.56738	],
	"Jersey"	:	[	49.214439	,	-2.13125	],
	"Jamaica"	:	[	18.109581	,	-77.297508	],
	"Jordan"	:	[	30.585164	,	36.238414	],
	"Japan"	:	[	36.204824	,	138.252924	],
	"Kenya"	:	[	-0.023559	,	37.906193	],
	"Kyrgyzstan"	:	[	41.20438	,	74.766098	],
	"Cambodia"	:	[	12.565679	,	104.990963	],
	"Kiribati"	:	[	-3.370417	,	-168.734039	],
	"Comoros"	:	[	-11.875001	,	43.872219	],
	"Saint Kitts and Nevis"	:	[	17.357822	,	-62.782998	],
	"North Korea"	:	[	40.339852	,	127.510093	],
	"South Korea"	:	[	35.907757	,	127.766922	],
	"Kuwait"	:	[	29.31166	,	47.481766	],
	"Cayman Islands"	:	[	19.513469	,	-80.566956	],
	"Kazakhstan"	:	[	48.019573	,	66.923684	],
	"Laos"	:	[	19.85627	,	102.495496	],
	"Lebanon"	:	[	33.854721	,	35.862285	],
	"Saint Lucia"	:	[	13.909444	,	-60.978893	],
	"Liechtenstein"	:	[	47.166	,	9.555373	],
	"Sri Lanka"	:	[	7.873054	,	80.771797	],
	"Liberia"	:	[	6.428055	,	-9.429499	],
	"Lesotho"	:	[	-29.609988	,	28.233608	],
	"Lithuania"	:	[	55.169438	,	23.881275	],
	"Luxembourg"	:	[	49.815273	,	6.129583	],
	"Latvia"	:	[	56.879635	,	24.603189	],
	"Libya"	:	[	26.3351	,	17.228331	],
	"Morocco"	:	[	31.791702	,	-7.09262	],
	"Monaco"	:	[	43.750298	,	7.412841	],
	"Moldova"	:	[	47.411631	,	28.369885	],
	"Montenegro"	:	[	42.708678	,	19.37439	],
	"Madagascar"	:	[	-18.766947	,	46.869107	],
	"Marshall Islands"	:	[	7.131474	,	171.184478	],
	"Macedonia [FYROM]"	:	[	41.608635	,	21.745275	],
	"Mali"	:	[	17.570692	,	-3.996166	],
	"Myanmar [Burma]"	:	[	21.913965	,	95.956223	],
	"Mongolia"	:	[	46.862496	,	103.846656	],
	"Macau"	:	[	22.198745	,	113.543873	],
	"Northern Mariana Islands"	:	[	17.33083	,	145.38469	],
	"Martinique"	:	[	14.641528	,	-61.024174	],
	"Mauritania"	:	[	21.00789	,	-10.940835	],
	"Montserrat"	:	[	16.742498	,	-62.187366	],
	"Malta"	:	[	35.937496	,	14.375416	],
	"Mauritius"	:	[	-20.348404	,	57.552152	],
	"Maldives"	:	[	3.202778	,	73.22068	],
	"Malawi"	:	[	-13.254308	,	34.301525	],
	"Mexico"	:	[	23.634501	,	-102.552784	],
	"Malaysia"	:	[	4.210484	,	101.975766	],
	"Mozambique"	:	[	-18.665695	,	35.529562	],
	"Namibia"	:	[	-22.95764	,	18.49041	],
	"New Caledonia"	:	[	-20.904305	,	165.618042	],
	"Niger"	:	[	17.607789	,	8.081666	],
	"Norfolk Island"	:	[	-29.040835	,	167.954712	],
	"Nigeria"	:	[	9.081999	,	8.675277	],
	"Nicaragua"	:	[	12.865416	,	-85.207229	],
	"Netherlands"	:	[	52.132633	,	5.291266	],
	"Norway"	:	[	60.472024	,	8.468946	],
	"Nepal"	:	[	28.394857	,	84.124008	],
	"Nauru"	:	[	-0.522778	,	166.931503	],
	"Niue"	:	[	-19.054445	,	-169.867233	],
	"New Zealand"	:	[	-40.900557	,	174.885971	],
	"Oman"	:	[	21.512583	,	55.923255	],
	"Panama"	:	[	8.537981	,	-80.782127	],
	"Peru"	:	[	-9.189967	,	-75.015152	],
	"French Polynesia"	:	[	-17.679742	,	-149.406843	],
	"Papua New Guinea"	:	[	-6.314993	,	143.95555	],
	"Philippines"	:	[	12.879721	,	121.774017	],
	"Pakistan"	:	[	30.375321	,	69.345116	],
	"Poland"	:	[	51.919438	,	19.145136	],
	"Saint Pierre and Miquelon"	:	[	46.941936	,	-56.27111	],
	"Pitcairn Islands"	:	[	-24.703615	,	-127.439308	],
	"Puerto Rico"	:	[	18.220833	,	-66.590149	],
	"Palestinian Territories"	:	[	31.952162	,	35.233154	],
	"Portugal"	:	[	39.399872	,	-8.224454	],
	"Palau"	:	[	7.51498	,	134.58252	],
	"Paraguay"	:	[	-23.442503	,	-58.443832	],
	"Qatar"	:	[	25.354826	,	51.183884	],
	"Réunion"	:	[	-21.115141	,	55.536384	],
	"Romania"	:	[	45.943161	,	24.96676	],
	"Serbia"	:	[	44.016521	,	21.005859	],
	"Russia"	:	[	61.52401	,	105.318756	],
	"Rwanda"	:	[	-1.940278	,	29.873888	],
	"Saudi Arabia"	:	[	23.885942	,	45.079162	],
	"Solomon Islands"	:	[	-9.64571	,	160.156194	],
	"Seychelles"	:	[	-4.679574	,	55.491977	],
	"Sudan"	:	[	12.862807	,	30.217636	],
	"Sweden"	:	[	60.128161	,	18.643501	],
	"Singapore"	:	[	1.352083	,	103.819836	],
	"Saint Helena"	:	[	-24.143474	,	-10.030696	],
	"Slovenia"	:	[	46.151241	,	14.995463	],
	"Svalbard and Jan Mayen"	:	[	77.553604	,	23.670272	],
	"Slovakia"	:	[	48.669026	,	19.699024	],
	"Sierra Leone"	:	[	8.460555	,	-11.779889	],
	"San Marino"	:	[	43.94236	,	12.457777	],
	"Senegal"	:	[	14.497401	,	-14.452362	],
	"Somalia"	:	[	5.152149	,	46.199616	],
	"Suriname"	:	[	3.919305	,	-56.027783	],
	"São Tomé and Príncipe"	:	[	0.18636	,	6.613081	],
	"El Salvador"	:	[	13.794185	,	-88.89653	],
	"Syria"	:	[	34.802075	,	38.996815	],
	"Swaziland"	:	[	-26.522503	,	31.465866	],
	"Turks and Caicos Islands"	:	[	21.694025	,	-71.797928	],
	"Chad"	:	[	15.454166	,	18.732207	],
	"French Southern Territories"	:	[	-49.280366	,	69.348557	],
	"Togo"	:	[	8.619543	,	0.824782	],
	"Thailand"	:	[	15.870032	,	100.992541	],
	"Tajikistan"	:	[	38.861034	,	71.276093	],
	"Tokelau"	:	[	-8.967363	,	-171.855881	],
	"Timor-Leste"	:	[	-8.874217	,	125.727539	],
	"Turkmenistan"	:	[	38.969719	,	59.556278	],
	"Tunisia"	:	[	33.886917	,	9.537499	],
	"Tonga"	:	[	-21.178986	,	-175.198242	],
	"Turkey"	:	[	38.963745	,	35.243322	],
	"Trinidad and Tobago"	:	[	10.691803	,	-61.222503	],
	"Tuvalu"	:	[	-7.109535	,	177.64933	],
	"Taiwan"	:	[	23.69781	,	120.960515	],
	"Tanzania"	:	[	-6.369028	,	34.888822	],
	"Ukraine"	:	[	48.379433	,	31.16558	],
	"Uganda"	:	[	1.373333	,	32.290275	],
	"U.S. Minor Outlying Islands"	:	[	0	,	0	],
	"United States"	:	[	37.09024	,	-95.712891	],
	"Uruguay"	:	[	-32.522779	,	-55.765835	],
	"Uzbekistan"	:	[	41.377491	,	64.585262	],
	"Vatican City"	:	[	41.902916	,	12.453389	],
	"Saint Vincent and the Grenadines"	:	[	12.984305	,	-61.287228	],
	"Venezuela"	:	[	6.42375	,	-66.58973	],
	"British Virgin Islands"	:	[	18.420695	,	-64.639968	],
	"U.S. Virgin Islands"	:	[	18.335765	,	-64.896335	],
	"Vietnam"	:	[	14.058324	,	108.277199	],
	"Vanuatu"	:	[	-15.376706	,	166.959158	],
	"Wallis and Futuna"	:	[	-13.768752	,	-177.156097	],
	"Samoa"	:	[	-13.759029	,	-172.104629	],
	"Kosovo"	:	[	42.602636	,	20.902977	],
	"Yemen"	:	[	15.552727	,	48.516388	],
	"Mayotte"	:	[	-12.8275	,	45.166244	],
	"South Africa"	:	[	-30.559482	,	22.937506	],
	"Zambia"	:	[	-13.133897	,	27.849332	],
	"Zimbabwe"	:	[	-19.015438	,	29.154857	]
	}

	return coordinates[country]
