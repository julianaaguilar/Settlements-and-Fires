# Tracking fires and nearby settlements

Team: Juliana Aguilar, Lucía Delgado & Jorge Quintero

## The project

The objectives of this project is to provide an interactive platform to show the location of fires and the share of settled area they could impact in a selected country and time range. 

For this purpose we built a webpage using Flask. The webpage produces three types of **output** for the chosen country:

1.  **Dynamic map with fires** according to specified parameters –country, fires confidence level and time frame of occurrence. When placing the mouse at each fire, the map shows time and date of registration.

2. **Static map showing settled area** for a specified country.

3. **Dynamic map with fires and share of settled area around the fire.** As output one, the map can be customized for the country, the fires confidence level and time frame of occurrence. The main difference is that when placing the mouse at each fire, the map shows shows the percent of settled area around the fire in addition to time and date of registration.

 We use the following **datasets**:

1. **Fires worldwide:**

Fire points identified by NASA using images from two satellites: Modis and VIIRS. The program can be set to update the this data as new information is uploaded frequently. The data is downloaded from [NASA's website.](https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms/active-fire-data).

2. **Settlements**

Raster data from the European Commission's Global Human Settlement Layers (GHSL). This data contains information on built-up presence as derived by the ad-hoc Landsat 8 collection 2013/2014. The resolution is of 250m. The data was obtained from [this site.](http://cidportal.jrc.ec.europa.eu/ftp/jrcopendata/GHSL/GHS_BUILT_LDSMT_GLOBE_R2015B/GHS_BUILT_LDS2014_GLOBE_R2016A_54009_250/)

## The code 
(Responsible team member in parenthesis)

* *data_downloader.py* (Jorge Quintero):
	Downloads data from Nasa's website and stores it as regional archives.

* *maps_maker.py* (Lucía Delgado): 
	Prints a dynamic map of a specified country, fires confidence level and time frame of occurence the fires. 
	Stores it as html object.

* *raster_ghsl.py* (Juliana Aguilar):
	Prints a static map of settlements for a specified country.
	Stores it as a .png file.

* *join_raster_shp.py* (Juliana Aguilar):
	Estimates share of settled area around the each fire.
	Produces a shapefile with this information.

* *maps_maker_settle.py* (Map generation: Lucía Delgado; Sync with other codes: Juliana Aguilar): 
	Generates an interactive map for one country including information about settled area at 1km buffer to each fire.

* *webpage* (Juliana Aguilar): 
	Creates the interface to call and see the output of previous functions.	

**Auxiliary code**

* *install_packages.py*:
	Gives options to install the packages necessary to run the codes.
	
* *util.py*: 
	Supporting functions.

* *aux_country_to_coordinates.py*:
	Generates a dictionary that maps countries to central coordinates.

* *aux_dictionar_regions.py*:
	Generates a dictionary that maps countries to regions.

	
## Other details

* **The files** are heavy, and can't be uploaded to github. The complete set of files can be downloaded from [here.](https://www.dropbox.com/sh/825bo6b7atkl067/AACQwhnEzO5_DmeQAismH_wya?dl=0) The folder contains:

  * *Fires* (optional): We uploaded a small sample to github (South America), and the complete 
set of files can be downloaded from the link above. When using the full set extract the file "Fires.zip" to "Fire-database/FireTracker/app/data/fires_regions", and then modify "Fire-database/FireTracker/app/__init__.py" to include the complete list of countries. Exact insructions are given in the code.

  * *Settlements* (Required): to be able to execute the program extract the file "Settlements.zip" to "Fire-database/FireTracker/app/data/GHSL".

* **Install packages**: some of the packages are tricky to install, we collected various ways in which we were able to install these in our computers. All versions are in the install_packages.py file.
	

	
 

		





