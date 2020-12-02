import time
import random
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



def process(parser, line):
	while len(parser) > 0:
		letter = parser[:1]
		parser = parser[1:]
		if letter == "1":
			line += "standing, "
		elif letter == "2":
			line += "name, "
		elif letter == "3":
			line += "platform, "
		elif letter == "4":
			line += "year, "
		elif letter == "5":
			line += "genre, "
		elif letter == "6":
			line += "publisher, "
		elif letter == "7":
			line += "NA_Sales, "
		elif letter == "8":
			line += "EU_Sales, "
		elif letter == "9":
			line += "JP_Sales, "
		elif letter == "a":
			line += "Other_Sales, "
		elif letter == "b":
			line += "Global_Sales, "
		else:
			print("Not a valid string.")
			return "ERR"
	line = line[:-2] + " "
	return line



def att_grab():
	print("Which attributes do you want to apply?\n1. Standing (row in the DB)\n2. Name\n3. Platform\n4. Year\n5. Genre\n6. Publisher\n7. North American Sales\n8. European Sales\n9. Japan Sales\na. Other sales\nb.Global sales\nType which you want: ")
	val = raw_input()
	if val == "1":
		return "standing"
	elif val == "2":
		return "name"
	elif val == "3":
		return "platform"
	elif val == "4":
		return "year"
	elif val == "5":
		return "genre"
	elif val == "6":
		return "publisher"
	elif val == "7":
		return "NA_Sales"
	elif val == "8":
		return "EU_Sales"
	elif val == "9":
		return "JP_Sales"
	elif val == "a":
		return "Other_Sales"
	elif val == "b":
		return "Global_Sales"
	else:
		print("Not an attribute. Pick better next time.")
		return "ERR"


def conditions(select):
	looped = false
	clone = select + " where ";
	menu(3)
	val = raw_input()
	while val != "5":
		looped = true
		if val == "1":
			val = att_grab()
			while val=="ERR":
				val = att_grab()
			clone += val + " between "
			val = raw_input("Enter the between values, seperated by a space: ")
			split = val.find(" ")
			first = val[:split]
			last = val[split+1:]
			clone += first + " and " + last
			print(clone)
		elif val == "2":
			val = att_grab()
			while val=="ERR":
				val = att_grab()
			clone += val + " in "
			val = raw_input("Enter the matching values, seperate by commas (you don't have to include a comma if there's just the one:\n")
			liz = []
			i = val.find(",");
			while i != -1:
				liz.append(val[:i])
				val = val[i+1:]
				i = val.find(",")
			liz.append(val)
			clone += "("
			for item in liz:
				clone += item + ", "
			clone = clone[:-2] + ")"
			print(clone)
		elif val == "3":
			val = att_grab()
			while val=="ERR":
				val = att_grab()
			clone += val + " like "
			val = raw_input("Enter the matcher value (it is case sensitive, so be specific): ")
			clone += "\'%" + val + "%\'"
			print(clone)
		elif val == "4":
			val = att_grab()
			while val=="ERR":
				val = att_grab()
		#elif val == "5":
		#else:
		#	print("Invalid response. Try again.")
		#	return "ERR"
		time.sleep(.2)
		menu(4)
		val = raw_input()
		if val != 5:	
			clone += " and "
	if looped:
		return clone
	else:
		return select




def search(conn):
	str = "select "
	menu(2)
	val = raw_input()
	str = process(val,str)
	print(str)
	if str != "ERR":
		str += "from sales"
		str = conditions(str)
	#cur = conn.cursor()
	#cur.execute(str)

	#rows = cur.fetchall()

	#for row in rows:
	#	print(row)
"""how to select by a certain priority == ("select * from tasks where priority=?", (priority,))"""



def reduce(lizt):
	#[0] == name, [1] == platform, [2] == year, [3] == genre
	clone = []
	for row in lizt:
		clone.append(row)
	menu(1)
	val = raw_input()
	if val == "y":
		val = raw_input("Type in a year: ")
		i = 0
		while i < len(clone):
			if clone[i][2] == val:
				i += 1
			else:
				clone.pop(i)
	elif val == "g":
		val = raw_input("Type in the genre: ")
		i = 0
		while i < len(clone):
			if clone[i][3] == val:
				i += 1
			else:
				clone.pop(i)
	elif val == "c":
		val = raw_input("Type in a console: ")
		i = 0
		while i < len(clone):
			if clone[i][1] == val:
				i+= 1
			else:
				clone.pop(i)
	elif val == "p":
		x = 1;
		for row in lizt:
			print(str(x) + ": ")
			print(row)
			x += 1
	elif val == "n":
		val = raw_input("Type in a title: ")
		i = 0
		while i < len(clone):
			if clone[i][0].find(val) != -1:
				i += 1
			else:
				clone.pop(i)
	else:
		print("Not valid, asshole.")


	if len(clone) == 0:
		print("No games matched that search. Try again?\n")
		return lizt
	else:
		return clone;




def watch(conn):
	line = "https://twitch.tv/directory/game/"
	val = raw_input("Looking for a specific game, or something new? (specific/new)\n")
	curr = conn.cursor()
	if val == "specific" or val == "s":
		val = raw_input("Type of the name of the game in: ")
		search = "select name, platform, year, genre from sales where name like '%" + val + "%'"
		curr.execute(search)

		rows = curr.fetchall()
		while len(rows) > 1:
			rows = reduce(rows)
			time.sleep(.2)

		for row in rows:
			line += row[0]
	elif val == "new" or val == "n":
		curr.execute("select name from sales where year > '2015'")

		rows = curr.fetchall()
		x = random.randrange(0,len(rows))
		line += rows[x][0]

	webbrowser.open(line)




def data(conn):
	print("I dunno how matplotlib works!!")




def menu(int):
	switcher = {
		0: "\n\nWelcome to the video game sales database!\nWhat would you like?\nSearch for games (search/s)\nWatch a particular game (watch/w)\nLook through data about games (data/d)\nQuit application (quit/q)\n",
		1: "\nMultiple games match that search. Can you be more specific?\nChoose a more specific name(n)\nChoose a year(y)\nChoose a genre(g)\nChoose a console of platform(c)\nPrint the games you have so far(p)\n",
		2: "\nWhich attributes do you want to see?\n1. Standing (row in the DB)\n2. Name\n3. Platform\n4. Year\n5. Genre\n6. Publisher\n7. North American Sales\n8. European Sales\n9. Japan Sales\na. Other sales\nb.Global sales\nType the letters and numbers you want, in the order you want them: ",
		3: "\nDo you want a certain condition on the data?\n\n1. An attribute value within a certain range\n2. Check if value matches a list of values (genre == \"Platform, Action, or Misc\")\n3. Answer includes a portion of the answer (Name includes \"Bear\")\n4. Include if this column's empty\n5. None of the above\n",
		4: "\nAny other conditions?\n\n1. An attribute value within a certain range\n2. Check if value matches a list of values (genre == \"Platform, Action, or Misc\")\n3. Answer includes a portion of the answer (Name includes \"Bear\")\n4. Include if this column's empty\n5. None of the above\n"}
	print switcher.get(int, "ERROR")




def main():
	random.seed()
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
			time.sleep(.5)
			menu(0)
			val = raw_input()
		print("Have a great day!")
		#webbrowser.open("https://twitch.tv")




main()