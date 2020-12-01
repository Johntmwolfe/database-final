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




def select(conn, str):
	cur = conn.cursor()
	cur.execute(str)

	rows = cur.fetchall()

	for row in rows:
		print(row)
"""how to select by a certain priority == ("select * from tasks where priority=?", (priority,))"""






def parse(conn, str):
	select(conn, "Select name from sales where Publisher = \"Nintendo\" order by Year ASC limit 10")

def main():
	conn = create_connection("proj.db")
	with conn: 
		val = raw_input("What do you want from the database?\n")
		parse(conn, val)
		#webbrowser.open("https://twitch.tv")

main()