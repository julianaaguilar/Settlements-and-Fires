from flask import Flask, render_template, request, send_file
#from .model import runmakemap 

app = Flask(__name__, static_url_path='')

@app.route("/")
def index():
	countries = ["Colombia", "Ecuador", "Brazil"]
	ghsl_countries = ["Colombia", "Ecuador", "Brazil", "South Africa"]
	intensities = ["Low", "Normal", "High", "All"]
	return render_template('index.html', countries=countries, intensities=intensities, ghsl_countries=ghsl_countries)

@app.route("/map")
def map():
	country = request.args.get("country", "")
	intensity = request.args.get("intensity", "All")
	from_date = request.args.get("from_date", "2018-02-01")
	to_date = request.args.get("to_date", "2018-04-01")
	#d = makemap(country,from_date, to_date, intensity)

	return send_file('maps/colombia_outmap.html')

@app.route("/ghsl_map")
def ghsl_map():
	country = request.args.get("country", "")
	intensity = request.args.get("intensity", "All")
	from_date = request.args.get("from_date", "2018-02-01")
	to_date = request.args.get("to_date", "2018-04-01")
	
	src = "ghsl_map_img?country=" + country + \
			"&intensity=" + intensity + \
			"&from_date=" + from_date + \
			"&to_date=" + to_date 

	return render_template("ghsl_map.html", country=country, src=src)

@app.route("/ghsl_map_img")
def ghsl_map_img():
	country = request.args["country"]
	intensity = request.args["intensity"]
	from_date = request.args["from_date"]
	to_date = request.args["to_date"]
	#d = raster_ghsl ## completar con mi funcion y cambiar ruta abajo

	return send_file('maps/Ecuador_ghsl.png')