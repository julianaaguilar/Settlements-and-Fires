from .maps_maker import draw_map

def makemap(country,from_date, to_date, intensity):
	route = draw_map(country, from_date, to_date, intensity)
	return route

def makemap_settlement(country,from_date, to_date, intensity):
	route = draw_map(country, from_date, to_date, intensity)
	return route
	
	