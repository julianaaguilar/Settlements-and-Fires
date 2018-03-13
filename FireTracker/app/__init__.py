from flask import Flask, render_template, request, send_file
from . import model 


app = Flask(__name__, static_url_path='')

@app.route("/")
def index():
	countries = COUNTRIES_SA
	# countries = COUNTRIES_ALL
		# If all files are downloaded from the link in README, the values of countries 
		# can be changed to COUNTRIES_ALL to access all countries. 
		# Please, comment line X, and uncomment line X.

	ghsl_countries = COUNTRIES_GHSL
	ghsl_fire_countries = ["Colombia"]
	intensities = ["low", "normal", "high"]

	return render_template('index.html', countries=countries, intensities=intensities, \
		ghsl_countries=ghsl_countries, ghsl_fire_countries=ghsl_fire_countries)

@app.route("/map")
def map():
	# Note: the get does not return the alternative when value is empty.
	country = request.args.get("country", "")

	intensity = request.args.get("intensity", "normal")
	if intensity == None:
		intensity = "normal"

	from_date = request.args.get("from_date", "2018-02-01")
	if from_date == None:
		from_date = "2018-02-01"

	to_date = request.args.get("to_date", "2018-04-01")
	if to_date == None:
		to_date = "2018-04-01"

	from_tot = float(from_date[0:4]) * 10000 + \
				float(from_date[5:7]) * 100 + \
				float(from_date[8:10])

	to_tot = float(to_date[0:4]) * 10000 + \
			float(to_date[5:7]) * 100 + \
			float(to_date[8:10])

	if from_tot >= to_tot:
		map_out = model.makemap(country,from_date, to_date, intensity)
	else:
		map_out = model.makemap(country,to_date, from_date, intensity)

	return send_file(map_out)


@app.route("/ghsl_map")
def ghsl_map():
	country = request.args.get("country", "")
	
	src = "ghsl_map_img?country=" + country

	return render_template("ghsl_map.html", country=country, src=src)

@app.route("/ghsl_map_img")
def ghsl_map_img():
	country = request.args["country"]
	map_out = model.makemap_settlement(country)

	return send_file(map_out)

@app.route("/ghsl_fire")
def ghsl_fire():

	return render_template('index.html')

@app.route("/ghsl_fire_map")
def ghsl_fire_map():
	country = request.args.get("country", "")
	#map_out = model.makemap_settlement_fire(country)

	map_out = "maps/buffer_map_settled.html"

	return send_file(map_out)

# Definition of list inputs
COUNTRIES_ALL = ['Afghanistan', \
'Algeria', \
'Angola', \
'Argentina', \
'Armenia', \
'Australia', \
'Austria', \
'Azerbaijan', \
'Bangladesh', \
'Belgium', \
'Belize', \
'Benin', \
'Bhutan', \
'Bolivia', \
'Bosnia and Herzegovina', \
'Botswana', \
'Brazil', \
'Brunei', \
'Bulgaria', \
'Burkina Faso', \
'Burundi', \
'Cambodia', \
'Cameroon', \
'Canada', \
'Central African Republic', \
'Chad', \
'Chile', \
'China', \
'Colombia', \
'Costa Rica', \
'Croatia', \
'Cuba', \
'Cyprus', \
'Czechia', \
'Democratic Republic of the Congo', \
'Denmark', \
'Dominican Republic', \
'Ecuador', \
'Egypt', \
'El Salvador', \
'Equatorial Guinea', \
'Eritrea', \
'Ethiopia', \
'France', \
'Gabon', \
'Gambia', \
'Georgia', \
'Germany', \
'Ghana', \
'Greece', \
'Guatemala', \
'Guinea', \
'Guinea-Bissau', \
'Guyana', \
'Haiti', \
'Honduras', \
'Hungary', \
'India', \
'Indonesia', \
'Iran', \
'Iraq', \
'Ireland', \
'Israel', \
'Italy', \
'Ivory Coast', \
'Jamaica', \
'Japan', \
'Jordan', \
'Kazakhstan', \
'Kenya', \
'Kuwait', \
'Kyrgyzstan', \
'Laos', \
'Liberia', \
'Libya', \
'Luxembourg', \
'Macedonia', \
'Madagascar', \
'Malawi', \
'Malaysia', \
'Mali', \
'Mauritania', \
'Mexico', \
'Moldova', \
'Morocco', \
'Mozambique', \
'Myanmar', \
'Namibia', \
'Nepal', \
'Netherlands', \
'New Caledonia', \
'New Zealand', \
'Nicaragua', \
'Niger', \
'Nigeria', \
'North Korea', \
'Northern Cyprus', \
'Norway', \
'Oman', \
'Pakistan', \
'Palestine', \
'Panama', \
'Papua New Guinea', \
'Paraguay', \
'Peru', \
'Philippines', \
'Poland', \
'Portugal', \
'Puerto Rico', \
'Qatar', \
'Republic of Serbia', \
'Republic of the Congo', \
'Romania', \
'Russia', \
'Saudi Arabia', \
'Senegal', \
'Sierra Leone', \
'Slovakia', \
'Solomon Islands', \
'Somalia', \
'Somaliland', \
'South Africa', \
'South Korea', \
'South Sudan', \
'Spain', \
'Sri Lanka', \
'Sudan', \
'Suriname', \
'Swaziland', \
'Sweden', \
'Syria', \
'Taiwan', \
'Tajikistan', \
'Thailand', \
'The Bahamas', \
'Togo', \
'Trinidad and Tobago', \
'Tunisia', \
'Turkey', \
'Turkmenistan', \
'Uganda', \
'Ukraine', \
'United Arab Emirates', \
'United Kingdom', \
'United Republic of Tanzania', \
'United States of America', \
'Uruguay', \
'Uzbekistan', \
'Venezuela', \
'Vietnam', \
'Yemen', \
'Zambia', \
'Zimbabwe']

COUNTRIES_SA = ['Argentina', \
'Bolivia', \
'Brazil', \
'Chile', \
'Colombia', \
'Ecuador', \
'Paraguay', \
'Peru', \
'Suriname', \
'Uruguay']

COUNTRIES_GHSL = ['Ecuador',
 'El Salvador',
 'Gambia',
 'Guatemala',
 'Honduras',
 'Israel',
 'Lebanon',
 'Panama',
 'Qatar']
