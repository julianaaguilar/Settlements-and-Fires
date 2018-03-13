# Project: FIRE TRACKING
# Task: PROCESSES APPLICATION
# Team: JULIANA AGUILAR, LUCIA DELGADO AND JORGE QUINTERO

from .maps_maker import draw_map
from .raster_ghsl import ghsl_country
from .maps_maker_settle import fire_settle

def makemap(country,from_date, to_date, intensity):
	route = draw_map(country, from_date, to_date, intensity)
	return route

def makemap_settlement(country):
	route = ghsl_country(country)
	return route

def makemap_settlement_fire(country):
	route = fire_settle(country)
	return route
	
	