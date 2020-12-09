import time
import random
import sqlite3
import math
import webbrowser
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
from sqlite3 import Error
from tabulate import tabulate
import numpy as np 
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




'''	
Main function, drives the program
'''
def main():
	random.seed()								#seed used for the watch function
	conn = create_connection("vgsales.db")			#connect to the database
	with conn: 
		menu(0)								#output initial menu
		val = input()
		#print(val)
		while val != "q" and val != "quit":
			if val == "s" or val == "search":
				search(conn)					#search through the database, sql style
			elif val == "w" or val == "watch":
				watch(conn)						#pull up a twitch stream of the game
			elif val == "d" or val == "data":
				data_menu(conn)							#look at the data in a visualized format
			time.sleep(.5)
			menu(0)
			val = input()					#loop
		print("Have a great day!")





'''
creates the initial connection with the database
'''
def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		print(sqlite3.version)
	except Error as e:
		print(e)
	return conn




'''
search function. Let's the user create a sqlite 
search, querying the user so they can create a
query on their own.
'''
def search(conn):
	str = "select "
	print("\nWhich attributes to you want to use?\n")
	menu(2)						#Takes a string representing all the columns they want
	val = input()			#take that string in
	liz = process(val)			#process the string, turning it into a list of attributes
	while liz[0] == "ERR":
		menu(2)
		val = input()
		liz = process(val)

	if liz[0] == "*":	#If they included all of it...
		str += "* "
	else:								#NOT all of it
		for attrib in liz:				#for each item in the list...
			str += attrib + ", "		#...add it to the select operation
		str = str[:-2] + " "			#cut off the end that has the comma
	str += "from sales "				#add the database
		
	#condition operation
	str = conditions(str, False)	#compile the conditions the user wants

	#group operation
	val = input("Do you want the group the output to a certain attribute? \n(yes/no): ")
	if val == "yes" or val == "y":
		print("Which attribute?\n")
		val = att_grab()					#att_grab() grabs a single column
		str += "group by " + val + " "

		#having operation
		val = input("Do you want to have a condition for these groupings?\n(yes/no): ")
		if val == "yes" or val == "y":
			str = conditions(str,True)	#adds only one conditional (true prevents looping)

	#order by operation
	val = input("Do you want the output sorted?\n(y/n): ")
	if val == "yes" or val == "y":
		str += " order by"
		str = order(str)				#loops for how many orders the user wants

	#limit operation
	val = input("Do you want a limit to the return values? (y/n): ")
	if val == "yes" or val == "y":
		val = input("Limit by how many?: ")		#how many rows does the user want (at max)
		str += " limit " + val
		
	#try the string
	cur = conn.cursor()		#make a cursor object to step through the database
	print("SELECTION: " + str)
	cur.execute(str)		#perform the select operations

	rows = cur.fetchall()	#make a list of all the rows selecteed

	pages(rows, liz)		#print all the rows




'''
Print out many rows in a more standardized format.
User can tab back and forth through the rows as they choose
'''
def pages(rows, lizt):
	page = 0
	last = math.ceil(len(rows)/50)
	while True:
		table = []
		header = []
		print("****************************************************************************")
		print("Page " + str(page + 1) + " of " +  str(last))
		x = 0
		#print("#", end = "\t")
		while x < len(lizt):
			if lizt[x] == "*":
				header.append("Standing")
				header.append("Name")
				header.append("Platform")
				header.append("Year")
				header.append("Genre")
				header.append("Publisher")
				header.append("NA_Sales")
				header.append("EU_Sales")
				header.append("JP_Sales")
				header.append("Other_Sales")
				header.append("Global_Sales")
			else:
				header.append(lizt[x])
			x += 1
		x = 0
		while x < 50:
			place = 50 * page + x
			if place >= len(rows):
				break
			else:
				table.append(rows[place])
			x += 1
		print(tabulate(table, headers = header))
		print("****************************************************************************")
		print("(f)irst\t\t(p)revious\t\tPage " + str(page+1) + " of " + str(last) + "\t\t(n)ext\t\t(l)ast")
		val = input("Or (q)uit")
		if val == "f":
			page = 0
		elif val == "p":
			page -= 1
			if page < 0:
				page = 0
		elif val == "n":
			page += 1
			if page > last - 1:
				page = last - 1
		elif val == "l":
			page = last - 1
		elif val == "q":
			break
		else:
			print("Not a valid string")






'''
Process a line, which is a string of numbers and letters, 
that represents a list of attributes the user wants. The
list is created here, then returned.
'''
def process(parser):
	liz = []						#empty list
	while len(parser) > 0:			#while there's more of the string to parse
		letter = parser[:1]			#grab a single letter
		parser = parser[1:]			#cut it off the rest of the list
		if letter == "1":			
			liz.append("Standing")	#push the item onto the list per the encoding 
		elif letter == "2":
			liz.append("Name")
		elif letter == "3":
			liz.append("Platform")
		elif letter == "4":
			liz.append("Year")
		elif letter == "5":
			liz.append("Genre")
		elif letter == "6":
			liz.append("Publisher")
		elif letter == "7":
			liz.append("NA_Sales")
		elif letter == "8":
			liz.append("EU_Sales")
		elif letter == "9":
			liz.append("JP_Sales")
		elif letter == "a":
			liz.append("Other_Sales")
		elif letter == "b":
			liz.append("Global_Sales")
		elif letter == "*":				#if they asked for all of them...
			liz.append("*")				#...add an encoding for every item
		else:								#error value
			print("Not a valid string.")
			err = ["ERR"]					#push on error code
			return err						#quick return the error
	return liz




'''
Create a long list of conditionals. Or just one,
depending on the single bool
'''
def conditions(select, single):
	looped = False				#bool to see if we've entered the loop or not
	clone = select
	if not single:			#if we're not just going through once...	
		clone += " where "	#add the where

	print("\nDo you want a certain condition on the data?\n")
	menu(3)						#conditional menus
	val = input()
	while val != "6":			#while we haven't exited
		looped = True			#we looped!

		#range measure
		if val == "1":
			val = att_grab()				#grab the attribute they want
			clone += val + " between "		#select encoding
			val = input("Enter the between values, seperated by a space: ")
			split = val.find(" ")			#find space between the range
			first = val[:split]				#first one
			last = val[split+1:]			#second one
			clone += first + " and " + last	#add encoding

		#exact match measure
		elif val == "2":
			val = att_grab()							#grab attribute
			clone += val + " in "						#match encoding
			val = input("Enter the matching values, seperate by commas (you don't have to include a comma if there's just the one:\n")
			liz = []									#user gives a string of values to match, seperated by commas
			i = val.find(",")							#find item
			while i != -1:					#while there's more to find...
				liz.append(val[:i])			#add that item to the list
				val = val[i+1:]				#remove item from the string
				i = val.find(",")			#look for the next item
			liz.append(val)								#there's an item past the final comma, so it needs to be added
			clone += "("								#begin the list encoding
			for item in liz:
				clone +=  "\"" + item.strip() + "\", "	#add the list
			clone = clone[:-2] + ")"					#remove the ", from the end, close the parenthesis

		#search for a substring
		elif val == "3":
			val = att_grab()				#grab an attribute
			clone += val + " like "			#add substring encoding
			val = input("Enter the matcher value (it is case sensitive, so be specific): ")
			clone += "\'%" + val + "%\'"	#add the searcher value

		#NULL checker
		elif val == "4":
			print("\nWhich attributes do you want to check?")
			menu(2)						#take a list of attributes
			val = input()
			liz = process(val)			#make a list of those attributes
			while liz[0]=="ERR":
				menu(2)				#if they gave you a bad value, make them do it again
				val = input()
				liz = process(val)
			clone += "("				#beginning of NULL encoding
			for item in liz:
				clone += item + " | "	#adding multiple values
			clone = clone[:-3] + ")"	#remove " | " and close the list
			val = input("Are you wanting to check if this is NULL, or filled?\n1. NULL\n2. Not NULL\n")
			while val != "1" and val != "2":	#if they didnt give you a valid string, make them give you a valid one
				val = input("Are you wanting to check if this is NULL, or filled?\n1. NULL\n2. Not NULL\n")
			if val == "1":
				clone += " is NULL"
			else:
				clone += " is not NULL"

		#regular math comparisons
		elif val == "5":
			val = att_grab()								#grab attribute for comparisons
			clone += " " + val
			menu(4)											#query them on which math operator they're using (< | <= | > | >= | != | =)
			val = input()
			while int(val) > 6 or int(val) < 1:				#if they didn't give you a valid value, make them
				menu(4)
				val = input()
			comparator = input("Comparator value (the number or value you're comparing to): ")
			if val == "1":
				clone += " > " + comparator					#add the various math comparisons
			elif val == "2":
				clone += " >= " + comparator
			elif val == "3":
				clone += " < " + comparator
			elif val == "4":
				clone += " <= " + comparator
			elif val == "5":
				clone += " = " + comparator
			else:
				clone += " != " + comparator
		else:
			looped = False
		
		
		if (single):				#if we're not supposed to loop after this
			val = "6"				#force the user to quit
		else:					#if they can loop...
			print("\nAny other conditions?\n")
			menu(3)					
			val = input()	#ask them for more comparisons
			if val != "6" and looped == True:	
				clone += " and "
	if looped:					#if we actually added a conditional..
		return clone			#send it back
	else:
		return select			#otherwise, no work was done here. Send back the old.




'''
Asks the user to select an attribute, and sends it back
'''
def att_grab():
	print("Which attribute do you want to use?\n1. Standing (row in the DB)\n2. Name\n3. Platform\n4. Year\n5. Genre\n6. Publisher\n7. North American Sales\n8. European Sales\n9. Japan Sales\na. Other sales\nb.Global sales\nType which you want: ")
	val = input()			
	if val == "1":				#pretty basic stuff, honestly. The
		return "Standing"		#user inputs a value, and if its 
	elif val == "2":			#valid, the corresponding attribute
		return "Name"			#is returned
	elif val == "3":
		return "Platform"
	elif val == "4":
		return "Year"
	elif val == "5":
		return "Genre"
	elif val == "6":
		return "Publisher"
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
		return att_grab()	#recursively make them return a valid attribute


'''
Makes the encoding for the ordering operation
'''
def order(line):
	val = ""
	while val != "no" and val != "n":											#while the user isn't done...
		val = att_grab()														#grab an attribute
		up_down = input("Order by ascending or descending? (asc/desc): ")	#do the want the attribute in ascending or descending order?
		if up_down == "a" or up_down == "asc":
			line += " " + val + " asc,"											#ascending encoding
		elif up_down == "d" or up_down == "desc":
			line += " " + val + " desc,"										#descending encoding
		else:
			print("Try again, idiot.")
		val = input("Want to sort further? (yes/no): ")						#ask if they want more
	return line[:-1]															#return the line, without the final comma




'''
Watch function! Sends the user to twitch.tv when
they find a game they want to watch
'''
def watch(conn):
	line = "https://twitch.tv/directory/game/"											#base URL
	val = input("Looking for a specific game, or something new? (specific/new)\n")	#ask the user if they want new, or something specific
	curr = conn.cursor()															#cursor for searching

	#specific
	if val == "specific" or val == "s":
		val = input("Type of the name of the game in (case-sensitive): ")		#get the specific value
		search = "select *from sales where name like '%" + val + "%'"
		curr.execute(search)														#search for the specific value

		rows = curr.fetchall()			#grab every game that fits
		while len(rows) > 1:			#if there's more than one...			
			rows = reduce(rows)			#reduce the amount of rows
			time.sleep(.2)

			line += rows[0][0]

	#new
	elif val == "new" or val == "n":			
		curr.execute("select name from sales where year > '2015'")	#find all games from 2016-forward

		rows = curr.fetchall()						#grab all games
		x = random.randrange(0,len(rows))			#get a random one
		line += rows[x][0]

	webbrowser.open(line)							#go to that page on twitch!




'''
Reduces a larger list of games until only one remains, then returns that value
'''
def reduce(lizt):
	#[0] == name, [1] == platform, [2] == year, [3] == genre
	clone = []				
	for row in lizt:
		clone.append(row)		#copy the original list
	menu(1)
	val = input()			#see how the user wants to further remove rows
	
	#year
	if val == "y":
		val = input("Type in a year: ")
		i = 0
		while i < len(clone):		#step through the list
			if clone[i][2] == int(val):	#if the year value matches their year...
				i += 1				#it can stay
			else:
				clone.pop(i)		#lest, we DESTROY IT
	
	#genre
	elif val == "g":							#the other cases function much the same as the year case
		val = input("Type in the genre: ")
		i = 0
		while i < len(clone):
			if clone[i][3] == val:
				i += 1
			else:
				clone.pop(i)

	#platform
	elif val == "c":
		val = input("Type in a console: ")
		i = 0
		while i < len(clone):
			if clone[i][1] == val:
				i+= 1
			else:
				clone.pop(i)

	#name case
	elif val == "n":
		val = input("Type in a title: ")
		i = 0
		while i < len(clone):
			if clone[i][0].find(val) != -1:
				i += 1
			else:
				clone.pop(i)

	#This isn't a destroy case: this prints off all the games so far allowed by the search so far
	elif val == "p":
		if len(lizt) > 50:
			pages(lizt, ["Name","Platform","Year","Genre"])
		else:
			x = 1
			for row in lizt:			#for every row...
				print(str(x) + ": ")	#the number of this row
				print(row)				#the row itself
				x += 1
	
	else:
		print("Not valid, asshole.")

	#after they do the reduction, check if they accidentally got rid of everything. 
	if len(clone) == 0:
		print("No games matched that search. Try again?\n")	#let them know they goofed
		return lizt											#return original list
	else:				#if they DIDN'T reduce to nothing..
		return clone	#return their good work!

# Gets the sales information from the database
def get_Sales(game_name, conn):
	with conn:
		NA_Sales = "SELECT NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales FROM sales WHERE Name = ?;"
		return conn.execute(NA_Sales, (game_name,)).fetchone()

# Creates the bar diagram for the sales from each region
def bar_sales(game_name, all_sales):
	x = ["North America", "Europe", "Japan", "Others", "Global"]
	h = []
	for index in all_sales:
		h.append(index)
	c = ["darkred", "orangered", "darkgreen", "navy", "darkviolet"]
	plt.bar(x, h, color=c)
	plt.xlabel("Sales in regions")
	plt.ylabel("Sales in millions")
	plt.title("Sales for the video game: " + game_name)
	plt.show()

# Prints a matplotlib bar chart of sales from all parts of the world.
def data(conn):
	print("Which video game would you like to see for sales data?")
	game_name = input()
	all_sales = get_Sales(game_name, conn)
	bar_sales(game_name, all_sales)

def data_menu(conn):
    print("Welcome to the data section!")
    print("Would you like to see sales data about games? (yes: sales/ no: choose another option in list)")
    print("Would you like to see a pie chart showing the most common genres? (yes: pie/no: choose another option in list)")
    print("Quit? (Q/q) ")
    val = input()
    while val != "Q" and val != "q" and val != "quit" and val != "Quit":
        if val == "sales" or val == "Sales":
            data(conn)
        elif val == "pie" or val == "Pie":
            data2(conn)
        time.sleep(.5)
        menu(0)
        val = input()
    print("Have a great day!")
    
def func(pct, allvalues): 
    absolute = int(pct / 100.*np.sum(allvalues)) 
    return "{:.1f}%\n({:d} g)".format(pct, absolute)

# pir chart data
def data2(conn):
    genres = 'Action', 'Sports', 'Misc', 'Role-Playing', 'Shooter', 'Adventure', 'Racing', 'Platform', 'Simulation', 'Fighting', 'Strategy', 'Puzzel'
    sizes = [20, 14, 10, 9, 8, 8, 8, 5, 5, 5, 4, 4]
    fig = plt.figure(figsize =(10, 7)) 
    plt.pie(sizes, labels = genres, autopct = lambda pct: func(pct, data))
    plt.show()



'''
A place to store the large ass strings. These are 
all various menus used within the program
'''
def menu(int):
	switcher = {
		0: 
'''
Welcome to the video game sales database!
What would you like?
Search for games (search/s)
Watch a particular game (watch/w)
Look through data about games (data/d)
Quit application (quit/q)
		''',
		
		1: 
'''
Multiple games match that search. Can you be more specific?
Choose a more specific name(n)
Choose a year(y)
Choose a genre(g)
Choose a console of platform(c)
Print the games you have so far(p)
''',

		2: 
'''
1. Standing (row in the DB)
2. Name
3. Platform
4. Year
5. Genre
6. Publisher
7. North American Sales
8. European Sales
9. Japan Sales
a. Other sales
b.Global sales
Type the letters and numbers you want, in the order you want them.\nSearch(if you want them all, put a *): ",
''',

		3: 
'''
1. An attribute value within a certain range
2. Check if value matches a list of values (genre == \"Platform, Action, or Misc\")
3. Answer includes a portion of the answer (Name includes \"Bear\")
4. Include if this column's empty
5. A mathematical comparison(less than, greater than, equal to)
6. None of the above
''',

		4:
'''
Which conditional?
1. >
2. >=
3. <
4. <=
5. =
6. !=
'''
	}
	print(switcher.get(int, "ERROR"))

main()
