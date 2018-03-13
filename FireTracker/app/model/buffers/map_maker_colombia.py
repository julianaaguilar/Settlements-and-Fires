'''
This code generates an interactive map for colombia including information 
about about population close to the fires.

We generate a map for Colombia, sincehuman settlement data (raster data)
is only avaliable for some countries. This code is easily generalizable to
other countries.
'''

import folium
import geopandas as gpd


#Generate GeoJson from shapefile:
#ogr2ogr -f GeoJSON buffers_Col.geojson buffers_Col.shx

# Open data in GeoJson Format

df = gpd.read_file('buffers_Col.geojson') 
geojson = r'buffers_Col.geojson'

#Location for Colombia
location = [4.60971, -74.08175]

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
map1.save(outfile='buffer_map.html') 

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
map2.save(outfile='buffer_map_settled.html')



