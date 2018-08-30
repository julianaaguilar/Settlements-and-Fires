# Tracking fires and nearby settlements

*Team: Juliana Aguilar, Lucía Delgado & Jorge Quintero*

## The project

The objectives of this project is to provide an interactive platform to show the location of fires and the share of settled area they could impact in a selected country and time range. 

For this purpose we built a webpage using Flask. The webpage produces three types of **outputs** for the chosen country:

1. **Fires:** dynamic map with specified parameters (country, fires confidence level and time frame of occurrence). 
Placing the mouse at each fire shows time and date of registration.

2. **Settlements:** static map showing GHLS data for the specified country.

3. **Fires and settlements:** dynamic map with specified parameters (country, fires confidence level and time frame 
of occurence). Placing the mouse at each fire shows time, date of registration and percent of settled area around 
the fire. This data is only available for Colombia.

 We use the following **datasets**:

**1. Fires worldwide:**

Fire points identified by NASA using images from two satellites: Modis and VIIRS. The program can be set to update the this data. The data was downloaded from [NASA's website.](https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms/active-fire-data).

**2. Settlements**

Raster data from the European Commission's Global Human Settlement Layers (GHSL). This data contains information on built-up presence as derived by the ad-hoc Landsat 8 collection 2013/2014. The resolution is of 250m. The data was obtained from [this site.](http://cidportal.jrc.ec.europa.eu/ftp/jrcopendata/GHSL/GHS_BUILT_LDSMT_GLOBE_R2015B/GHS_BUILT_LDS2014_GLOBE_R2016A_54009_250/)

# The code 
(Responsible team member in parenthesis)

data_downloader.py (Jorge Quintero):
	Downloads data from Nasa's website and stores it as regional archives.

maps_maker.py (Lucía Delgado): 
	Prints a dynamic map of a specified country, fires confidence level and time frame of occurence the fires. 
	Stores it as html object.

raster_ghsl.py (Juliana Aguilar):
	Prints a static map of settlements for a specified country.
	Stores it as a .png file.

join_raster_shp.py (Juliana Aguilar):
	Estimates share of settled area around the each fire.
	Produces a shapefile with this information.

maps_maker_settle.py (Map generation: Lucía Delgado; Sync with other codes: Juliana Aguilar): 
	Generates an interactive map for one country including information about settled area at 1km buffer to each fire.

webpage (Juliana Aguilar): 
	Creates the interface to call and see the output of previous functions.	

**Auxiliary code**



util.py: 
	File form PS2 we used to build soups. We didnt change it.

aux_country_to_coordinates.py:
	Generates a dictionary that maps countries to central coordinates

aux_dictionar_regions.py:
	Generates a dictionary that maps countries to regions

	
# About the files
The files we use in this project are heavy, and can't be uploaded to github.

Additional files: https://www.dropbox.com/sh/825bo6b7atkl067/AACQwhnEzO5_DmeQAismH_wya?dl=0 

1. Fires (optional): We uploaded a small sample to github (South America), but the complete 
set of files can be downloaded from the link above. 
Instructions: i) Extract the file "Fires.zip" to "Fire-database/FireTracker/app/data/fires_regions"; 
ii) Modify "Fire-database/FireTracker/app/__init__.py" to include the complete list of countries. 
Exact insructions are given in the code.

2. Settlements (Required): The folder is empty. Instructions: i) Extract the file "Settlements.zip" to "Fire-database/FireTracker/app/data/GHSL".
	



Sample data: 
As mentioned, github only includes a demo version. If complete files are downloaded as previously specified you 
need to modify "/app/__init__.py" to reflect these changes.
	
# Instructions -Option 1
0. Extract "Settlements.zip" to "Fire-database/FireTracker/app/data/GHSL".
1. Change your directory to "/Fire-database/Firetracker/" 
2. Install pipenv. Follow these instructions:https://www.dropbox.com/sh/825bo6b7atkl067/AACQwhnEzO5_DmeQAismH_wya?dl=0 
2. Run $ pipenv install
3. Run $ pipenv shell
4. Run $ FLASK_APP=run.py pipenv run flask run
5. Open your favourite browser and go to the path indicated by the python console. Usually: 127.0.0.1000
6. Place your request (it takes several minutes, between 5 and 15, depending on the request).
7. If dates don't display automatically, type a starting and ending date between 2018-02-01 and 2018-03-13. 
Please keep the format, it corresponds to year/month/day.
8. If you get your previous search, instead of the new one, refres your browser.


Specific features:By placing the mouse on top of the fire you can see its main characteristics.

# Instructions -Option 2
	The virtual environment should handle all downloads. These packages will be automatically installed after 
	step 2 in the previous intructions. 
	However, if you find problems intalling the packages these are some of the steps we followed. 
	
	0. Install packages
	
	use pip install <package> --user 
for the following packages:
	flask = "*"
	rtree = "*"
	fiona = "*"
	geopandas =	 "*"
	matplotlib = "*"
	pyshp = "*"
	pandas = "*"
	folium = "*"
	pathlib = "*"
	rasterio = "==1.0a12"
	numpy = "*"
	requests = "*"
	regex = "*"
	"beautifulsoup4" = "*"

	'''
Install Anaconda (REQUIRED TO INSTALL CARTOPY)
	wget https://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh
	wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
	bash Miniconda3-latest-Linux-x86_64.sh
	bash Anaconda-latest-Linux-x86_64.sh
	conda install ipython
To make the changes take effect, close and then re-open your Terminal window.
	'''
	'''
Install cartopy
	conda install -c conda-forge cartopy
	sudo pip install cartopy
	'''
	'''
Install rasterio, if pip install doesn't work
	sudo add-apt-repository ppa:ubuntugis/ppa
	sudo apt-get update
	sudo apt-get install python-numpy gdal-bin libgdal-dev
	pip install rasterio===1.0a12
	'''
	
1. Change your directory to "/Fire-database/Firetracker/"
2. Run $ FLASK_APP=run.py flask run
3. Follow steps 5-8 of Instructions-Option 1
	
 

		





