# Project: FIRE TRACKING
# Task: AUTOMATIZED DOWNLOAD OF FIRE DATASETS
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
Projection: WGS84
'''
'''
INSTRUCTIONS:
To run this function on a schedule, load scraping.py into ipython and
paste the following code:

schedule.every().day.at("4:30").do(scraping.go)
while True:
    schedule.run_pending()
    time.sleep(1)
'''

import re
import bs4
#import piqueue
import json
import sys
import csv
import urllib
#
from . import util
#import util
import os.path
import datetime
from os.path import join as pjoin
#import schedule
import time
#from crontab import CronTab
import zipfile
from os import listdir
from os.path import isfile, join
import geopandas as gpd
import pandas as pd
import urllib.parse
#sudo -H pip3 install schedule
from pathlib import Path


website = "https://earthdata.nasa.gov/earth-observation-data/\
near-real-time/firms/active-fire-data"

formats = ["MODIS24h", "MODIS48h", "MODIS7d","VIIRS24h", "VIIRS48h", "VIIRS7d"]

#final_directory = '/home/student/capp30122-win-18-jorgequintero/fire_project/downloads'

ROOT = Path(__file__).parents[1]
final_directory = os.path.join(str(ROOT), "data/fires_regions/")


def build_soup(website):
    '''
    Takes a website and creates a soup.

    Inputs:
        website: a url

    Outputs:
        Soup object.
    '''

    #the util.py file was given to us in PA2. 
    #We didnt change anything in it
    sitio = util.get_request(website)
    siitio = util.read_request(sitio)
    soup = bs4.BeautifulSoup(siitio, "html5lib")

    return soup


def soup_to_links(soup):
    '''
    Takes a soup and looks for the relevant url in a table. 
    Inputs:
        soup: obect to look for urls.
        

    Outputs:
        Dictionary with all the links to the files to download.
    '''

    data = []
    links = []
    dict_all = {}
    

    #looking in the soup for the table with the links
    table = soup.find('table')
    table_body = table.find('tbody')
      
    #representing the table into data
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values

        #creating a nested dictionary that organizes the links\
        #by regions and formats
        name = cols[0]
        if name not in dict_all:
            dict_all[name]={}
        
        #list of links per row
        list_link = []
        for link in row.find_all('a'):
            url_only = link.get('href')
            list_link.append(url_only)

        #populates the dictionary, by row with linksss
        for f in range(0,len(formats)):
            i_name = formats[f]
            dict_all[name][i_name] = list_link[f]


    return(dict_all)


def zipper(directory):
    '''
    This function takes all the zipped files in a directory
    and unzippes them.

    Input: directory
    '''
    for file_ in listdir(directory):
        path_to_file = pjoin(directory, "{t}".format(t = file_))      
        if path_to_file.endswith(".zip"):
            zip_ref = zipfile.ZipFile(path_to_file, 'r')
            zip_ref.extractall(directory)
            zip_ref.close()
            os.remove(path_to_file)
    return("Files unzipped")


def appender():
    '''
    Appends last daily fire observations onto the archive.

    Outputs:
        Files (list). MODIS and VIIRS files for the specified region.
    
    '''

    timeframe = ["archive.shp" , "24h.shp"]
    formats = ["MODIS_C6_", "VNP14IMGTDL_NRT_"]

    country_set = set()
    for file_ in listdir(final_directory):
        for t in timeframe:
            if file_.startswith("MODIS_C6_") and file_.endswith(t):
                c = file_[9:]
                country = c.replace(t,"")
                country_set.add(country)
    
                
    dic = {}
    for c in country_set:
        for f in formats:   
            archive_name = pjoin(final_directory, "{t}{u}{v}".format(t = f , u = c, v = "archive.shp"))
            fire_name = pjoin(final_directory, "{t}{u}{v}".format(t = f , u = c, v = "24h.shp"))
            dic[f + c] = [archive_name, fire_name]             

    count = 0
    #Lucia Delgado provided to the gpd. functionts
    for key in dic:
        file_a =  gpd.read_file(dic[key][0])         
        file_b =  gpd.read_file(dic[key][1])         
        apendeado = gpd.GeoDataFrame( pd.concat( [file_a, file_b] , ignore_index=True) )
        file_name = "{t}/{u}{v}.shp".format(t = final_directory, u = key, v = "archive")
        print(file_name)
        apendeado.to_file(filename = file_name, driver = "ESRI Shapefile")
        count +=1
        print('{u} {v}'.format(u = count, v = "files written"))

    for file_ in listdir(final_directory):
        if not (file_.endswith("_archive.shp") or \
        file_.endswith("_archive.shx") or file_.endswith("_archive.dbf")\
        or file_.endswith("_archive.cpg")):
            file_delete = pjoin(final_directory, file_)
            os.remove(file_delete)
    return(dic)

    
def go():
    '''
    Function that runs the whole thing and saves files to folder
    
    Output: bunch of files in appropriate foler
    '''

    #we ultimately decided we dont want ALL the formats in the following list, bur rather
    #only the files corresponding to the last 24h.
    #formats = ["MODIS24h", "MODIS48h", "MODIS7d","VIIRS24h",\
    # "VIIRS48h", "VIIRS7d"]

    formats_ = ["MODIS24h", "VIIRS24h"]


    soup = build_soup(website)
    dict_links = soup_to_links(soup)

    #File download. 
    for key in dict_links:
        #Most of the times there are simply no fires in alaska. 
        #when that happens, the zip is empty and creates a mess
        if key != "Alaska":
            for i in formats_:
                target_file = dict_links[key][i]

                #opening the links
                f = urllib.request.urlopen(target_file)
                data = f.read()
                path_to_file = pjoin(final_directory, "{t}{u}{v}".format(t = key , u = i, v=".zip"))
                with open(path_to_file, "wb") as code:
                    code.write(data)

        print(key)

    unzipping = zipper(final_directory)
    appending = appender()
    return("finished downloading and unzipping and appending")


def selector(region, format):
    '''
    Takes a region (string) and returns a to file names.

    Inputs:
        Region (string).
        format

    Outputs:
        Files (string). MODIS or VIIRS files for the specified region.
    '''



    soup = build_soup(website)
    dict_all = soup_to_links(soup)
   
    dictionary = {}
    dictionary_VIIRS = {}
    regions = []

    for key in dict_all:
        regions.append(key)



    for key in listdir(final_directory):
        path_to_file = pjoin(final_directory, "{t}".format(t = key))
        if key.startswith("MODIS_C6_Australia"):
            dictionary["Australia and New Zealand"] = path_to_file
        elif key.startswith("MODIS_C6_Canada"):
            dictionary["Canada"] = path_to_file
        elif key.startswith("MODIS_C6_Central_America"):
            dictionary["Central America"] = path_to_file
        elif key.startswith("MODIS_C6_Europe"):
            dictionary["Europe"] = path_to_file
        elif key.startswith("MODIS_C6_Global"):
            dictionary["World"] = path_to_file
        elif key.startswith("MODIS_C6_Northern_and_Central_Africa"):
            dictionary["North and Central Africa"] = path_to_file
        elif key.startswith("MODIS_C6_Russia"):
            dictionary["Russia and Asia"] = path_to_file
        elif key.startswith("MODIS_C6_SouthEast_Asia"):
            dictionary["South East Asia"] = path_to_file
        elif key.startswith("MODIS_C6_South_America"):
            dictionary["South America"] = path_to_file
        elif key.startswith("MODIS_C6_South_Asia"):
            dictionary["South Asia"] = path_to_file
        elif key.startswith("MODIS_C6_Southern_Africa"):
            dictionary["Southern Africa"] = path_to_file
        elif key.startswith("MODIS_C6_USA"):
            dictionary["USA (Conterminous) and Hawaii"] = path_to_file
        elif key.startswith("MODIS_C6_Alaska"):
            dictionary["Alaska"] = path_to_file


    for key in listdir(final_directory):
        path_to_file = pjoin(final_directory, "{t}".format(t = key))
        if key.startswith("VNP14IMGTDL_NRT_Australia"):
            dictionary_VIIRS["Australia and New Zealand"] = path_to_file
        elif key.startswith("VNP14IMGTDL_NRT_Canada"):
            dictionary_VIIRS["Canada"] = path_to_file
        elif key.startswith("VNP14IMGTDL_NRT_Central_America"):
            dictionary_VIIRS["Central America"] = path_to_file
        elif key.startswith("VNP14IMGTDL_NRT_Europe"):
            dictionary_VIIRS["Europe"] = path_to_file
        elif key.startswith("VNP14IMGTDL_NRT_Global"):
            dictionary_VIIRS["World"] = path_to_file
        elif key.startswith("VNP14IMGTDL_NRT_Northern_and_Central_Africa"):
            dictionary_VIIRS["North and Central Africa"] = path_to_file
        elif key.startswith("VNP14IMGTDL_NRT_Russia"):
            dictionary_VIIRS["Russia and Asia"] = path_to_file
        elif key.startswith("VNP14IMGTDL_NRT_SouthEast_Asia"):
            dictionary_VIIRS["South East Asia"] = path_to_file
        elif key.startswith("VNP14IMGTDL_NRT_South_America"):
            dictionary_VIIRS["South America"] = path_to_file
        elif key.startswith("VNP14IMGTDL_NRT_South_Asia"):
            dictionary_VIIRS["South Asia"] = path_to_file
        elif key.startswith("VNP14IMGTDL_NRT_Southern_Africa"):
            dictionary_VIIRS["Southern Africa"] = path_to_file
        elif key.startswith("VNP14IMGTDL_NRT_USA"):
            dictionary_VIIRS["USA (Conterminous) and Hawaii"] = path_to_file
        elif key.startswith("VNP14IMGTDL_NRT_Alaska"):
            dictionary_VIIRS["Alaska"] = path_to_file
        



    if region in regions and format == "VIIRS":
        file_ = dictionary_VIIRS[region]

    elif region in regions and format == "MODIS":
        file_ = dictionary[region]

    else:
        file_ = "Wrong format or region"


    return(file_)



