import sqlite3
import webbrowser
from sqlite3 import Error
"""
information below is summarized on sqlitetutorial.net

<> = optional inclusion
[] = a list of possible elements
() = a stand in for the element at hand
distinct - removes repeat tuples
limit - number of rows to return
select <distinct> [* or list of columns] from (db) limit (# of rows) where (condition) order by [column ASC, column DESC] group by (column) having (search condition)
**having MUST be used in conjunction with group by

Union - R U S
Except - R - S
Intersect - R n S

condition types:
between (values) and (value)
(column) in [values]
(column) like (pattern)  -  (pattern) is a str that the original must match to
(column) glob (a type of regex expression) 		//more on sqlitetutorial.net/sqlite-glob/
(column) = NULL

order of operations:
	select from where group having order limit
"""

def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		print(sqlite3.version)
	except Error as e:
		print(e)
	return conn




def search(conn):
	str = "select Name from sales limit 10"
	cur = conn.cursor()
	cur.execute(str)

	rows = cur.fetchall()

	for row in rows:
		print(row)
"""how to select by a certain priority == ("select * from tasks where priority=?", (priority,))"""




def watch(conn):
	webbrowser.open("https://twitch.tv")




def data(conn):
	print("I dunno how matplotlib works!!")




def menu(int):
	switcher = {
		0: "\n\nWelcome to the video game sales database!\nWhat would you like?\nSearch for games (search/s)\nWatch a particular game (watch/w)\nLook through data about games (data/d)\nQuit application (quit/q)\n"
	}
	print switcher.get(int, "ERROR")




def main():
	conn = create_connection("proj.db")
	with conn: 
		menu(0)
		val = raw_input()
		while val != "q" and val != "quit":
			if val == "s" or val == "search":
				search(conn)
			elif val == "w" or val == "watch":
				watch(conn)
			elif val == "d" or val == "data":
				data(conn)
			menu(0)
			val = raw_input()
		print("Have a great day!")
		#webbrowser.open("https://twitch.tv")




main()