# FIRE TRACKER

	Team: Juliana Aguilar, Lucía Delgado & Jorge Quintero

	Objectives: 
	- Provide an interactive platform that allows fire tracking around
	the globe with updated information.
	- Identify fires that are within a certain radius of human
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
	We use Global Human Settlement Layers (GHSL) from the European Commission. These data contain an information layer on built-up 
	presence as derived by the ad-hoc Landsat 8 collection 2013/2014. 

	Downloaded from: 
	   http://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_LDSMT_GLOBE_R2015B/GHS_BUILT_LDS2014_GLOBE_R2016A_54009_250/

	Resolution: 250m

	Year: 2014


# About the files
	The files we use in this project are heavy, and can't be uploaded to github.
	Additional files can be downloaded from here: https://www.dropbox.com/sh/825bo6b7atkl067/AACQwhnEzO5_DmeQAismH_wya?dl=0

	1. Fires worldwide: We put a small sample in github (South America), and the complete set of files can be downloaded from this link:
	 
	2. Settlements: we couldn't upload these files. Please unzip the file "GHS_BUILT_LDS2014_GLOBE_R2016A_54009_250_v1_0.zip" into "/FireTracker/app/data/GHSL".

# The webpage
	The webpage was built using flask. It produces three types of outputs:
	1. Fires: dynamic map with specified parameters (country, fires confidence level and time frame of occurence). Placing the mouse at each fire shows time and date of registration.
	2. Fires and settlements: dynamic map with specified parameters (country, fires confidence level and time frame of occurence). Placing the mouse at each fire shows time, date of registration and percent of settled area around the fire. This data is only available for Colombia.
	3. Settlements: static map showing GHLS data for the specified country. Available only for few countries.
	
	
	Instructions
	1. Change your directory to "/Fire-database/Firetracker/" 
	2. Install pipenv. Follow these instructions:https://www.dropbox.com/sh/825bo6b7atkl067/AACQwhnEzO5_DmeQAismH_wya?dl=0 
	2. Run $ pipenv install
	3. Run $ pipenv shell
	4. Run $ FLASK_APP=run.py pipenv run flask run
	5. Open your favourite browser and go to the path indicated by the python console. Usually: 127.0.0.1000
	6. Place your request (it takes several minutes, between 5 and 15, depending on the request.

	Note: Pipfile contains information on all the packages used. These packages will be automatically installed after step 2. 
	
	Sample: 
	As mentioned, github only includes a demo version. If complete files are downloaded as previously specified you need to modify "/app/__init__.py" to reflect these changes.

# The code

	data_downloader.py:
		Downloads data from Nasa's website and stores it as regional archives.

	maps_maker.py: 
		Prints a dynamic map of a specified country, fires confidence level and time frame of occurence the fires. 
		Stores it as html object.
	
	raster_ghsl.py:
		Prints a static map of settlements for a specified country.
		Stores it as a .png file.
	
	join_raster_shp.py:
		Estimate share of settled area around the each fire.
		Produces a shapefile with this information.
	buffers.py:
		
		

# Auxiliary code

	util.py: 
		File form PS2 we used to build soups. We didnt change it.

	aux_country_to_coordinates.py:
		Generates a dictionary that maps countries to central coordinates
	
	aux_dictionar_regions.py:
		Generates a dictionary that maps countries to regions



