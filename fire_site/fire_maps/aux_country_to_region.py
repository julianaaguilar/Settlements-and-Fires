# This dofile generates a dictionary matching countries to regions


import rtree
import fiona
import geopandas as gpd
import matplotlib.pyplot as plt
import shapefile
import pandas as pd
import cartopy
import cartopy.io.shapereader as shpreader


regions = ["Russia and Asia", "South East Asia", "Australia and New Zealand",
"Southern Africa" , "Alaska", "South America", "World", "South Asia", 
"USA (Conterminous) and Hawaii", "Canada", "Central America", "Europe", 
"North and Central Africa"]


alaska = "nasa_data/dict/VNP14IMGTDL_NRT_Alaska_7d/VNP14IMGTDL_NRT_Alaska_7d.shp"
australia = "nasa_data/dict/VNP14IMGTDL_NRT_Australia_and_New_Zealand_7d/VNP14IMGTDL_NRT_Australia_and_New_Zealand_7d.shp"
canada = "nasa_data/dict/VNP14IMGTDL_NRT_Canada_7d/VNP14IMGTDL_NRT_Canada_7d.shp"
central_am = "nasa_data/dict/VNP14IMGTDL_NRT_Central_America_7d/VNP14IMGTDL_NRT_Central_America_7d.shp"
europe = "nasa_data/dict/VNP14IMGTDL_NRT_Europe_7d/VNP14IMGTDL_NRT_Europe_7d.shp"
northcentrafrica = "nasa_data/dict/VNP14IMGTDL_NRT_Northern_and_Central_Africa_7d/VNP14IMGTDL_NRT_Northern_and_Central_Africa_7d.shp"
russia_asia = "nasa_data/dict/VNP14IMGTDL_NRT_Russia_and_Asia_7d/VNP14IMGTDL_NRT_Russia_and_Asia_7d.shp"
south_am = "nasa_data/dict/VNP14IMGTDL_NRT_South_America_7d/VNP14IMGTDL_NRT_South_America_7d.shp"
south_asia = "nasa_data/dict/VNP14IMGTDL_NRT_South_Asia_7d/VNP14IMGTDL_NRT_South_Asia_7d.shp"
south_east_asia = "nasa_data/dict/VNP14IMGTDL_NRT_SouthEast_Asia_7d/VNP14IMGTDL_NRT_SouthEast_Asia_7d.shp"
south_africa = "nasa_data/dict/VNP14IMGTDL_NRT_Southern_Africa_7d/VNP14IMGTDL_NRT_Southern_Africa_7d.shp"
usa = "nasa_data/dict/VNP14IMGTDL_NRT_USA_contiguous_and_Hawaii_7d/VNP14IMGTDL_NRT_USA_contiguous_and_Hawaii_7d.shp"


regtofile = {}
regtofile["Russia and Asia"] = russia_asia
regtofile["South East Asia"] = south_east_asia
regtofile["Australia and New Zealand"] = australia
regtofile["Southern Africa"] =  south_africa
regtofile["Alaska"] = alaska
regtofile["South America"] = south_am
regtofile["South Asia"] = south_asia
regtofile["USA (Conterminous) and Hawaii"] = usa
regtofile["Canada"] = canada
regtofile["Central America"] = central_am
regtofile["Europe"] = europe
regtofile["North and Central Africa"] = northcentrafrica


main = {}

for reg in regtofile:
	main[reg] = dregs.generate_dictionary(regtofile[reg])

d_reg = {}
for region in main:
 	for country in main[region]:
 		d_reg[country] = region



def generate_dictionary(region_fire_shapefile):
	'''
	This function gets a shapelie and return a list of
	the countries in the shapefile.
	'''
	mv = gpd.read_file(region_fire_shapefile)
	resolution = '110m'
	category = 'cultural'
	name = 'admin_0_countries'

	world_shp = shpreader.natural_earth(resolution, category, name)
	# read the shapefile using geopandas
	world_gpd = gpd.read_file(world_shp)


	#Generate dictionaty
	regions = world_gpd[["SOVEREIGNT","ADMIN", "REGION_WB", "geometry"]]

	points_world = gpd.sjoin(regions, mv, how="inner", op='intersects')
	country_list = points_world.ADMIN.unique()
		#regions.to_csv("world.csv")

	return country_list.tolist()

# Resulting dictionay

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
