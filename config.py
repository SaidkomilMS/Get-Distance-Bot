RADIUS = 6371008
TOKEN = "1014744242:AAFNv1rs6xHsStfcrDSSOsEZQ8hBOO6ZR6g"
KOEF = 1.35
from math import acos, cos, sin, pi

def get_suffix(distance):
	if str(int(distance))[-1] in ['0', '5', '6', '7', '8', '9']:
		return 'ов'
	elif str(int(distance))[-1] in ['2', '3', '4']:
		return 'a'
	else: return ''

def distance_handler(distance):
	'''NOT FOR MESSAGE HANDLING'''
	if distance / 1000 > 0:
		distance = distance/1000
		unit = 'километр'
	elif distance > 0:
		unit = 'метр'
	else:
		distance = distance*100
		unit = 'сантиметр'
	race = distance*KOEF
	if unit == 'метр':
		n = 1
	else: n = 2
	return distance, race, n, unit, get_suffix(distance)

def get_distance(location, chat_id, last_location):
	angle = get_angle(location, chat_id, last_location)
	return RADIUS * angle

def get_angle(location, chat_id, last_location):
	longitude = location.longitude
	latitude = location.latitude
	llocation = last_location[chat_id]
	llongitude = llocation.longitude
	llatitude = llocation.latitude
	alpha = acos(sin(llatitude*pi/180)*sin(latitude*pi/180) + cos(llatitude*pi/180)*cos(latitude*pi/180)*cos(abs(longitude - llongitude)*pi/180))
	last_location[chat_id] = location
	return alpha
