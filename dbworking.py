import sqlite3
from location import Location

db = 'db.db'

def is_not_in_db(user_id):
	with sqlite3.connect(db) as connection:
		cursor = connection.cursor()
		result = cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
		return not bool(len(result))

def add_user(user_id):
	with sqlite3.connect(db) as connection:
		cursor = connection.cursor()
		cursor.execute("INSERT INTO `users` (`user_id`,`loc_num`) VALUES (?, ?)", (user_id, 1))
		
def get_loc_nums():
	with sqlite3.connect(db) as connection:
		cursor = connection.cursor()
		result = cursor.execute("SELECT `user_id`, `loc_num` FROM `users`").fetchall()
		mydict = {}
		for r in result:
			mydict[int(r[0])] = r[1]
		return mydict

def save_loc(user_id, location):
	with sqlite3.connect(db) as connection:
		cursor = connection.cursor()
		cursor.execute("UPDATE `users` SET `latitude` = ?, `longitude` = ? WHERE `user_id` = ?", (location.latitude, location.longitude, user_id))
		
def get_last_locs():
	with sqlite3.connect(db)as connection:
		cursor = connection.cursor()
		result = cursor.execute("SELECT `user_id`, `latitude`,`longitude` FROM `users`"). fetchall()
		mydict = {}
		for r in result:
			mydict[r[0]] = Location(r[1], r[2])
		return mydict
		
def set_loc_num(user_id, val):
	with sqlite3.connect(db) as connection:
		cursor = connection.cursor()
		cursor.execute("UPDATE `users` SET `loc_num` = ? WHERE `user_id` = ?", (val, user_id))