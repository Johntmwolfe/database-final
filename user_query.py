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
	conn = create_connection("proj.db")			#connect to the database
	with conn: 
		menu(0)								#output initial menu
		val = input()
		print(val)
		while val != "0":
			if val == "1":
				search(conn)					#search through the database, sql style
			elif val == "2":
				watch(conn)						#pull up a twitch stream of the game
			elif val == "3":
				data_menu(conn)							#look at the data in a visualized format
			time.sleep(.5)
			menu(0)
			val = input()					#loop
		print("\nThank you for using the JAR Database!\nHave a great day!\n")





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
	print("******************************************")
	print("*     Welcome to the Search section!     *")
	print("******************************************")
	print("\nWhich attributes do you want to use to search?\n")
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
	val = input("Do you want to group the output by a certain attribute? \nEnter 1 for yes and 0 for no:\n")
	print()
	if val == "1":
		print("Which attribute?\n")
		val = att_grab()					#att_grab() grabs a single column
		str += "group by " + val + " "

		#having operation
		val = input("Do you want to have a condition for these groupings?\n(1 for yes and 0 for no):\n")
		if val == "1":
			str = conditions(str,True)	#adds only one conditional (true prevents looping)

	#order by operation
	val = input("Do you want the output sorted?\n(1 for yes and 0 for no):\n")
	if val == "1":
		str += " order by"
		str = order(str)				#loops for how many orders the user wants

	#limit operation
	val = input("Do you want a limit to the return values? (1 for yes and 0 for no):\n")
	if val == "1":
		val = input("Limit by how many?: ")		#how many rows does the user want (at max)
		while not val.isnumeric():
			val = input("Not a valid number, or you included spaces. Try again:\n")
		str += " limit " + val
		
	#try the string
	cur = conn.cursor()		#make a cursor object to step through the database
	#print("SELECTION: " + str)
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
				break;
			else:
				table.append(rows[place])
			x += 1
		print(tabulate(table, headers = header))
		print("****************************************************************************")
		print("(f)irst\t\t(p)revious\t\tPage " + str(page+1) + " of " + str(last) + "\t\t(n)ext\t\t(l)ast")
		val = input("Or (q)uit ")
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
			break;
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
def conditions(line, single):
	looped = False				#bool to see if we've entered the loop or not
	clone = ""
	if single:
		clone = " having "
	else:
		clone = " where "

	print("\nDo you want a certain condition on the data?\n")
	menu(3)						#conditional menus
	val = input()
	while val != "6":			#while we haven't exited
		#range measure
		if val == "1":
			attrib = att_grab()				#grab the attribute they want
			clone += attrib + " between "		#select encoding
			val = input("Enter the between values, seperated by a space: ")
			split = val.find(" ")			#find space between the range
			first = val[:split]				#first one
			last = val[split+1:]			#second one
			if attrib.split() == "4":
				clone += first + " and " + last	#add encoding
			else:
				clone += "\'" + first + "\' and \'" + last + "\'"

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
		
		
		if (single):				#if we're not supposed to loop after this
			val = "6"				#force the user to quit
		else:					#if they can loop...
			print("\nAny other conditions?\n")
			menu(3)					
			val = input()	#ask them for more comparisons
			if val == "1" or val == "2" or val == "3" or val == "4" or val == "5":	
				clone += " and "
			#if we actually added a conditional..
	if len(clone) == 7 or len(clone) == 8:
		return line
	else:
		return line + clone		#send it back




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
		print("Not an attribute. Please try again.")
		return att_grab()	#recursively make them return a valid attribute


'''
Makes the encoding for the ordering operation
'''
def order(line):
	val = ""
	while val != "0":											#while the user isn't done...
		val = att_grab()														#grab an attribute
		up_down = input("Order by ascending or descending? (1 for asc, 0 for desc): ")	#do the want the attribute in ascending or descending order?
		if up_down == "1":
			line += " " + val + " asc,"											#ascending encoding
		elif up_down == "0":
			line += " " + val + " desc,"										#descending encoding
		else:
			print("Invalid input. Please try again.")
		val = input("Want to sort further? (1 for yes, 0 for no): ")					#ask if they want more
	return line[:-1]															#return the line, without the final comma




'''
Watch function! Sends the user to twitch.tv when
they find a game they want to watch
'''
def watch(conn):
	line = "https://twitch.tv/directory/game/"											#base URL
	print("**********************************")
	print("*  Welcome to the watch section! *")
	print()
	print("* Here you will be able to watch *")
	print("*   a stream via Twitch of any   *")
	print("*      game you would like!      *")
	print("**********************************")
	val = input("\nAre you looking for a specific game, or something new?\n(1 for specific, 0 for new)\n")	#ask the user if they want new, or something specific
	curr = conn.cursor()
	dummy = False															#cursor for searching

	#specific
	if val == "1":
		val = input("\nPlease enter the name of the game: ")		#get the specific value
		search = "select name, platform, year, genre from sales where name like '%" + val + "%'"
		curr.execute(search)														#search for the specific value

		rows = curr.fetchall()			#grab every game that fits
		while len(rows) > 1:			#if there's more than one...			
			rows = reduce(rows)			#reduce the amount of rows
			time.sleep(.2)

		line += rows[0][0]

	#new
	elif val == "0":			
		curr.execute("select name from sales where year > '2015'")	#find all games from 2016-forward

		rows = curr.fetchall()						#grab all games
		x = random.randrange(0,len(rows))			#get a random one
		line += rows[x][0]
	else:
		dummy = True

	if dummy:
		print("Error: invalid response. Try again next time!")
	else:
		#print("URL: " + line)
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
	if val == "2":
		val = input("Type in a year: ")
		i = 0
		while i < len(clone):		#step through the list
			if clone[i][2] == val:	#if the year value matches their year...
				i += 1				#it can stay
			else:
				clone.pop(i)		#lest, we DESTROY IT
	
	#genre
	elif val == "3":							#the other cases function much the same as the year case
		val = input("Type in the genre: ")
		i = 0
		while i < len(clone):
			if clone[i][3] == val:
				i += 1
			else:
				clone.pop(i)

	#platform
	elif val == "4":
		val = input("Type in a console: ")
		i = 0
		while i < len(clone):
			if clone[i][1] == val:
				i+= 1
			else:
				clone.pop(i)

	#name case
	elif val == "1":
		val = input("Type in a title: ")
		i = 0
		while i < len(clone):
			if clone[i][0].find(val) != -1:
				i += 1
			else:
				clone.pop(i)

	#This isn't a destroy case: this prints off all the games so far allowed by the search so far
	elif val == "5":
		pages(lizt, ["Name","Platform","Year","Genre"])

	
	else:
		print("Not valid.")

	#after they do the reduction, check if they accidentally got rid of everything. 
	if len(clone) == 0:
		print("No games matched that search. Try again?\n")	#let them know they goofed
		return lizt											#return original list
	else:				#if they DIDN'T reduce to nothing..
		return clone	#return their good work!


# Gets the sales information from the database
def get_Sales(game_name, conn):
	with conn:
		sales = "SELECT Standing, Name FROM sales WHERE Name LIKE ?;"
		stuff = conn.execute(sales, ("%{}%".format(game_name),)).fetchall()
		if len(stuff) == 0:
			print("No game matches that name. Try again.")
			return []
		print("")
		print("Standing | Name ")
		print("-------------------------------")
		for column in stuff:
			print(f"{column[0]}	 | {column[1]}")
		print("")
		print("This game has multiple other games with a smiliar name. Please enter standing number based on the name of the game you are looking for from the table above.")
		num = input()
		new_sales2 = "SELECT Name, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales FROM sales WHERE Standing = ?;"
		#correct_name2 = get_Name(num, conn)
		#correct_name = "SELECT Name FROM sales WHERE Standing = ?"
		#correct_name2 = conn.execute(correct_name, (num, )).fetchone()
		#print("This is the correct name2 --> ", correct_name2)
		return conn.execute(new_sales2, (num,)).fetchone()

# Creates the bar diagram for the sales from each region
def bar_sales(all_sales):
	x = ["North America", "Europe", "Japan", "Others", "Global"]
	c = ["red", "orange", "yellow", "green", "blue"]
	h = []
	for index in all_sales[1:]:
		h.append(float(index))
	print("This is the h array --> ", h)
	plt.style.use('dark_background')
	plt.bar(x, h, color=c, linewidth=1, edgecolor="white")
	plt.annotate(str(h[0]), xy=(0, h[0] + 1))
	plt.annotate(str(h[1]), xy=(1, h[1] + 1))
	plt.annotate(str(h[2]), xy=(2, h[2] + 1))
	plt.annotate(str(h[3]), xy=(3, h[3] + 1))
	plt.annotate(str(h[4]), xy=(4, h[4] + 1))
	plt.xlabel("Sales in regions")
	plt.ylabel("Sales in millions")
	plt.title("Video game sales for: " + all_sales[0])
	plt.show()

# Creates the bar diagram for the sales from each region for 2 games
def bar_sales2(game1, game2, game1_sales, game2_sales):
	x = ["North America", "Europe", "Japan", "Others", "Global"]
	h1 = []
	h2 = []
	bar_width = 0.35
	for index in game1_sales[1:]:
		h1.append(float(index))
	for index2 in game2_sales[1:]:
		h2.append(float(index2))
	bar1 = np.arange(len(x))
	bar2 = [i+bar_width for i in bar1]
	plt.style.use('dark_background')
	plt.bar(bar1, h1, bar_width, color="red", linewidth=1, edgecolor="white", label=game1_sales[0])
	plt.bar(bar2, h2, bar_width, color="orange", linewidth=1, edgecolor="white", label=game2_sales[0])
	plt.annotate(str(h1[0]), xy=(0, h1[0] + 1))
	plt.annotate(str(h1[1]), xy=(1, h1[1] + 1))
	plt.annotate(str(h1[2]), xy=(2, h1[2] + 1))
	plt.annotate(str(h1[3]), xy=(3, h1[3] + 1))
	plt.annotate(str(h1[4]), xy=(4, h1[4] + 1))
	plt.annotate(str(h2[0]), xy=(0.35, h2[0] + 1))
	plt.annotate(str(h2[1]), xy=(1.35, h2[1] + 1))
	plt.annotate(str(h2[2]), xy=(2.35, h2[2] + 1))
	plt.annotate(str(h2[3]), xy=(3.35, h2[3] + 1))
	plt.annotate(str(h2[4]), xy=(4.35, h2[4] + 1))
	plt.xlabel("Sales in regions")
	plt.ylabel("Sales in millions")
	plt.title("Video game sales")
	plt.xticks(bar1+bar_width/2, x)
	plt.legend()
	plt.show()

# Creates the bar diagram for the sales from each region for 3 games
def bar_sales3(game1, game2, game3, game1_sales, game2_sales, game3_sales):
	x = ["North America", "Europe", "Japan", "Others", "Global"]
	h1 = []
	h2 = []
	h3 = []
	bar_width = 0.2
	for index in game1_sales[1:]:
		h1.append(float(index))
	for index2 in game2_sales[1:]:
		h2.append(float(index2))
	for index3 in game3_sales[1:]:
		h3.append(float(index3))
	bar1 = np.arange(len(x))
	bar2 = [i+bar_width for i in bar1]
	bar3 = [i+bar_width for i in bar2]
	plt.style.use('dark_background')
	plt.bar(bar1, h1, bar_width, color="red", linewidth=1, edgecolor="white", label=game1_sales[0])
	plt.bar(bar2, h2, bar_width, color="orange", linewidth=1, edgecolor="white", label=game2_sales[0])
	plt.bar(bar3, h3, bar_width, color="gold", linewidth=1, edgecolor="white", label=game3_sales[0])
	plt.annotate(str(h1[0]), xy=(0, h1[0] + 1))
	plt.annotate(str(h1[1]), xy=(1, h1[1] + 1))
	plt.annotate(str(h1[2]), xy=(2, h1[2] + 1))
	plt.annotate(str(h1[3]), xy=(3, h1[3] + 1))
	plt.annotate(str(h1[4]), xy=(4, h1[4] + 1))

	plt.annotate(str(h2[0]), xy=(0.2, h2[0] + 1))
	plt.annotate(str(h2[1]), xy=(1.2, h2[1] + 1))
	plt.annotate(str(h2[2]), xy=(2.2, h2[2] + 1))
	plt.annotate(str(h2[3]), xy=(3.2, h2[3] + 1))
	plt.annotate(str(h2[4]), xy=(4.2, h2[4] + 1))

	plt.annotate(str(h3[0]), xy=(0.4, h3[0] + 1))
	plt.annotate(str(h3[1]), xy=(1.4, h3[1] + 1))
	plt.annotate(str(h3[2]), xy=(2.4, h3[2] + 1))
	plt.annotate(str(h3[3]), xy=(3.4, h3[3] + 1))
	plt.annotate(str(h3[4]), xy=(4.4, h3[4] + 1))
	plt.xlabel("Sales in regions")
	plt.ylabel("Sales in millions")
	plt.title("Video game sales")
	plt.xticks(bar1+bar_width, x)
	plt.legend()
	plt.show()

# Creates the bar diagram for the sales from each region for 4 games
def bar_sales4(game1, game2, game3, game4, game1_sales, game2_sales, game3_sales, game4_sales):
	x = ["North America", "Europe", "Japan", "Others", "Global"]
	h1 = []
	h2 = []
	h3 = []
	h4 = []
	bar_width = 0.2
	for index in game1_sales[1:]:
		h1.append(float(index))
	for index2 in game2_sales[1:]:
		h2.append(float(index2))
	for index3 in game3_sales[1:]:
		h3.append(float(index3))
	for index4 in game4_sales[1:]:
		h4.append(float(index4))
	bar1 = np.arange(len(x))
	bar2 = [i+bar_width for i in bar1]
	bar3 = [i+bar_width for i in bar2]
	bar4 = [i+bar_width for i in bar3]
	plt.style.use('dark_background')
	plt.bar(bar1, h1, bar_width, color="red", linewidth=1, edgecolor="white", label=game1_sales[0])
	plt.bar(bar2, h2, bar_width, color="orange", linewidth=1, edgecolor="white", label=game2_sales[0])
	plt.bar(bar3, h3, bar_width, color="gold", linewidth=1, edgecolor="white", label=game3_sales[0])
	plt.bar(bar4, h4, bar_width, color="green", linewidth=1, edgecolor="white", label=game4_sales[0])
	plt.annotate(str(h1[0]), xy=(0, h1[0] + 1))
	plt.annotate(str(h1[1]), xy=(1, h1[1] + 1))
	plt.annotate(str(h1[2]), xy=(2, h1[2] + 1))
	plt.annotate(str(h1[3]), xy=(3, h1[3] + 1))
	plt.annotate(str(h1[4]), xy=(4, h1[4] + 1))

	plt.annotate(str(h2[0]), xy=(0.2, h2[0] + 1))
	plt.annotate(str(h2[1]), xy=(1.2, h2[1] + 1))
	plt.annotate(str(h2[2]), xy=(2.2, h2[2] + 1))
	plt.annotate(str(h2[3]), xy=(3.2, h2[3] + 1))
	plt.annotate(str(h2[4]), xy=(4.2, h2[4] + 1))
	
	plt.annotate(str(h3[0]), xy=(0.4, h3[0] + 1))
	plt.annotate(str(h3[1]), xy=(1.4, h3[1] + 1))
	plt.annotate(str(h3[2]), xy=(2.4, h3[2] + 1))
	plt.annotate(str(h3[3]), xy=(3.4, h3[3] + 1))
	plt.annotate(str(h3[4]), xy=(4.4, h3[4] + 1))

	plt.annotate(str(h4[0]), xy=(0.6, h4[0] + 1))
	plt.annotate(str(h4[1]), xy=(1.6, h4[1] + 1))
	plt.annotate(str(h4[2]), xy=(2.6, h4[2] + 1))
	plt.annotate(str(h4[3]), xy=(3.6, h4[3] + 1))
	plt.annotate(str(h4[4]), xy=(4.6, h4[4] + 1))
	plt.xlabel("Sales in regions")
	plt.ylabel("Sales in millions")
	plt.title("Video game sales")
	plt.xticks(bar1+0.3, x)
	plt.legend()
	plt.show()

# Creates the bar diagram for the sales from each region for 5 games
def bar_sales5(game1, game2, game3, game4, game5, game1_sales, game2_sales, game3_sales, game4_sales, game5_sales):
	x = ["North America", "Europe", "Japan", "Others", "Global"]
	h1 = []
	h2 = []
	h3 = []
	h4 = []
	h5 = []
	bar_width = 0.15
	for index in game1_sales[1:]:
		h1.append(float(index))
	for index2 in game2_sales[1:]:
		h2.append(float(index2))
	for index3 in game3_sales[1:]:
		h3.append(float(index3))
	for index4 in game4_sales[1:]:
		h4.append(float(index4))
	for index5 in game5_sales[1:]:
		h5.append(float(index5))
	bar1 = np.arange(len(x))
	bar2 = [i+bar_width for i in bar1]
	bar3 = [i+bar_width for i in bar2]
	bar4 = [i+bar_width for i in bar3]
	bar5 = [i+bar_width for i in bar4]
	plt.style.use('dark_background')
	plt.bar(bar1, h1, bar_width, color="red", linewidth=1, edgecolor="white", label=game1_sales[0])
	plt.bar(bar2, h2, bar_width, color="orange", linewidth=1, edgecolor="white", label=game2_sales[0])
	plt.bar(bar3, h3, bar_width, color="gold", linewidth=1, edgecolor="white", label=game3_sales[0])
	plt.bar(bar4, h4, bar_width, color="green", linewidth=1, edgecolor="white", label=game4_sales[0])
	plt.bar(bar5, h5, bar_width, color="blue", linewidth=1, edgecolor="white", label=game5_sales[0])
	plt.annotate(str(h1[0]), xy=(0, h1[0] + 1))
	plt.annotate(str(h1[1]), xy=(1, h1[1] + 1))
	plt.annotate(str(h1[2]), xy=(2, h1[2] + 1))
	plt.annotate(str(h1[3]), xy=(3, h1[3] + 1))
	plt.annotate(str(h1[4]), xy=(4, h1[4] + 1))

	plt.annotate(str(h2[0]), xy=(0.15, h2[0] + 1))
	plt.annotate(str(h2[1]), xy=(1.15, h2[1] + 1))
	plt.annotate(str(h2[2]), xy=(2.15, h2[2] + 1))
	plt.annotate(str(h2[3]), xy=(3.15, h2[3] + 1))
	plt.annotate(str(h2[4]), xy=(4.15, h2[4] + 1))
	
	plt.annotate(str(h3[0]), xy=(0.3, h3[0] + 1))
	plt.annotate(str(h3[1]), xy=(1.3, h3[1] + 1))
	plt.annotate(str(h3[2]), xy=(2.3, h3[2] + 1))
	plt.annotate(str(h3[3]), xy=(3.3, h3[3] + 1))
	plt.annotate(str(h3[4]), xy=(4.3, h3[4] + 1))

	plt.annotate(str(h4[0]), xy=(0.45, h4[0] + 1))
	plt.annotate(str(h4[1]), xy=(1.45, h4[1] + 1))
	plt.annotate(str(h4[2]), xy=(2.45, h4[2] + 1))
	plt.annotate(str(h4[3]), xy=(3.45, h4[3] + 1))
	plt.annotate(str(h4[4]), xy=(4.45, h4[4] + 1))

	plt.annotate(str(h5[0]), xy=(0.6, h5[0] + 1))
	plt.annotate(str(h5[1]), xy=(1.6, h5[1] + 1))
	plt.annotate(str(h5[2]), xy=(2.6, h5[2] + 1))
	plt.annotate(str(h5[3]), xy=(3.6, h5[3] + 1))
	plt.annotate(str(h5[4]), xy=(4.6, h5[4] + 1))
	plt.xlabel("Sales in regions")
	plt.ylabel("Sales in millions")
	plt.title("Video game sales")
	plt.xticks(bar1+0.3, x)
	plt.legend()
	plt.show()

# Prints a matplotlib bar chart of sales from all parts of the world.
def data(conn):
	all_sales = []
	while len(all_sales) == 0:
		print("")
		print("Which video game would you like to see for sales data?")
		game_name = input()
		all_sales = get_Sales(game_name, conn)
	bar_sales(all_sales)

# Prints a matplotlib bar chart of sales for multiple games.
def data3(conn):
	print("")
	print("How many games would you like to compare? (You can compare 2 to 5 games): ")
	num = input()

	if num == "2": 
		game1_sales = []
		game2_sales = []
		while len(game1_sales) == 0:
			game1 = input("Enter in video game 1 here --> ")
			game1_sales = get_Sales(game1, conn)
		while len(game2_sales) == 0:
			game2 = input("Enter in video game 2 here --> ")
			game2_sales = get_Sales(game2, conn)
		bar_sales2(game1, game2, game1_sales, game2_sales)
	elif num == "3":
		game1_sales = []
		game2_sales = []
		game3_sales = []
		while len(game1_sales) == 0:
			game1 = input("Enter in video game 1 here --> ")
			game1_sales = get_Sales(game1, conn)
		while len(game2_sales) == 0:
			game2 = input("Enter in video game 2 here --> ")
			game2_sales = get_Sales(game2, conn)
		while len(game3_sales) == 0:
			game3 = input("Enter in video game 3 here --> ")
			game3_sales = get_Sales(game3, conn)
		bar_sales3(game1, game2, game3, game1_sales, game2_sales, game3_sales)
	elif num == "4":
		game1_sales = []
		game2_sales = []
		game3_sales = []
		game4_sales = []
		while len(game1_sales) == 0:
			game1 = input("Enter in video game 1 here --> ")
			game1_sales = get_Sales(game1, conn)
		while len(game2_sales) == 0:
			game2 = input("Enter in video game 2 here --> ")
			game2_sales = get_Sales(game2, conn)
		while len(game3_sales) == 0:
			game3 = input("Enter in video game 3 here --> ")
			game3_sales = get_Sales(game3, conn)
		while len(game4_sales) == 0:
			game4 = input("Enter in video game 4 here --> ")
			game4_sales = get_Sales(game4, conn)
		bar_sales4(game1, game2, game3, game4, game1_sales, game2_sales, game3_sales, game4_sales)
	elif num == "5":
		game1_sales = []
		game2_sales = []
		game3_sales = []
		game4_sales = []
		game5_sales = []
		while len(game1_sales) == 0:
			game1 = input("Enter in video game 1 here --> ")
			game1_sales = get_Sales(game1, conn)
		while len(game2_sales) == 0:
			game2 = input("Enter in video game 2 here --> ")
			game2_sales = get_Sales(game2, conn)
		while len(game3_sales) == 0:
			game3 = input("Enter in video game 3 here --> ")
			game3_sales = get_Sales(game3, conn)
		while len(game4_sales) == 0:
			game4 = input("Enter in video game 4 here --> ")
			game4_sales = get_Sales(game4, conn)
		while len(game5_sales) == 0:
			game5 = input("Enter in video game 5 here --> ")
			game5_sales = get_Sales(game5, conn)
		bar_sales5(game1, game2, game3, game4, game5, game1_sales, game2_sales, game3_sales, game4_sales, game5_sales)
	else:
		print("Invalid input please put a number between 2 and 5.")

def data_menu(conn):
	menu(5)
	val = input()
	while val != "0":
		if val == "1":
			data(conn)
		elif val == "2":
			data3(conn)
		elif val == "3":
			data2(conn)
		elif val == "4":
			data5(conn)
		time.sleep(.5)
		menu(5)
		val = input()
		if val == "0":
			print("\nHeading back to main menu ...")

# pie chart data
def data2(conn):
	genres = 'Action', 'Sports', 'Misc', 'Role-Playing', 'Shooter', 'Adventure', 'Racing', 'Platform', 'Simulation', 'Fighting', 'Strategy', 'Puzzle'
	sizes = [20, 14, 10, 9, 8, 8, 8, 5, 5, 5, 4, 4]
	colors = ['red', 'orangered', 'darkorange', 'orange', 'gold', 'yellow', 'mediumseagreen', 'springgreen', 'dodgerblue', 'deepskyblue', 'mediumorchid', 'violet']
	fig = plt.figure(figsize =(10, 7))
	plt.pie(sizes, labels = genres, autopct='%.1f%%', colors=colors)
	plt.title("Most Common Genres:")
	plt.legend(genres, loc="upper right")
	plt.show()

def get_Games(name, conn):
	with conn:
		game_genres = "SELECT Name, Genre FROM sales WHERE Name LIKE ?;"
		return conn.execute(game_genres, ("%{}%".format(name),)).fetchone()

def genre_chart(name, all_game_names, conn):
	x = ["Action", "Sports", "Misc", "Role-Playing", "Shooter", "Adventure", "Racing", "Platform", "Simulation", "Fighting", "Strategy", "Puzzle"]
	y = []
	for games in all_game_names:
		y.append(games)
	count_y = []
	action = conn.execute("SELECT COUNT(Genre) FROM sales WHERE Name LIKE ? AND Genre = 'Action'", ("%{}%".format(name),)).fetchone()
	count_y.append(action)
	sports = conn.execute("SELECT COUNT(Genre) FROM sales WHERE Name LIKE ? AND Genre = 'Sports'", ("%{}%".format(name),)).fetchone()
	count_y.append(sports)
	misc = conn.execute("SELECT COUNT(Genre) FROM sales WHERE Name LIKE ? AND Genre = 'Misc'", ("%{}%".format(name),)).fetchone()
	count_y.append(misc)
	role = conn.execute("SELECT COUNT(Genre) FROM sales WHERE Name LIKE ? AND Genre = 'Role-Playing'", ("%{}%".format(name),)).fetchone()
	count_y.append(role)
	shooter = conn.execute("SELECT COUNT(Genre) FROM sales WHERE Name LIKE ? AND Genre = 'Shooter'", ("%{}%".format(name),)).fetchone()
	count_y.append(shooter)
	adventure = conn.execute("SELECT COUNT(Genre) FROM sales WHERE Name LIKE ? AND Genre = 'Adventure'", ("%{}%".format(name),)).fetchone()
	count_y.append(adventure)
	race = conn.execute("SELECT COUNT(Genre) FROM sales WHERE Name LIKE ? AND Genre = 'Racing'", ("%{}%".format(name),)).fetchone()
	count_y.append(race)
	platform = conn.execute("SELECT COUNT(Genre) FROM sales WHERE Name LIKE ? AND Genre = 'Platform'", ("%{}%".format(name),)).fetchone()
	count_y.append(platform)
	sim = conn.execute("SELECT COUNT(Genre) FROM sales WHERE Name LIKE ? AND Genre = 'Simulation'", ("%{}%".format(name),)).fetchone()
	count_y.append(sim)
	fight = conn.execute("SELECT COUNT(Genre) FROM sales WHERE Name LIKE ? AND Genre = 'Fighting'", ("%{}%".format(name),)).fetchone()
	count_y.append(fight)
	strat = conn.execute("SELECT COUNT(Genre) FROM sales WHERE Name LIKE ? AND Genre = 'Strategy'", ("%{}%".format(name),)).fetchone()
	count_y.append(strat)
	puzzle = conn.execute("SELECT COUNT(Genre) FROM sales WHERE Name LIKE ? AND Genre = 'Puzzle'", ("%{}%".format(name),)).fetchone()
	count_y.append(puzzle)

	y2 = [i[0] for i in count_y]
	explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
	colors = ['red', 'orangered', 'darkorange', 'orange', 'gold', 'yellow', 'mediumseagreen', 'springgreen', 'dodgerblue', 'deepskyblue', 'mediumorchid', 'violet']
	fig = plt.figure(figsize =(13, 10))
	plt.pie(y2, autopct='%.2f%%', explode=explode, colors=colors)
	plt.title("Most Popular Genres Containing - " + name)
	plt.legend(x, loc="upper right")
	plt.show()

def data5(conn):
	print("\nWhich character/name would you like to see data for? (Please note: data is case specific) ")
	name = input()
	all_game_names = get_Games(name, conn)
	genre_chart(name, all_game_names, conn)

	
'''
A place to store the large ass strings. These are 
all various menus used within the program
'''
def menu(int):
	switcher = {
		0: 
'''
**********************************************
*       Welcome to the JAR Database          *

*  Here you will find data for over 16,000   *
*               video games!                 *
**********************************************

What would you like to explore in our database?

Please enter the number that is next to your choice
1. Search for games
2. Watch a particular game (via Twitch)
3. Look through data about games
0. Quit application
		''',
		
		1: 
'''
Multiple games match that search. Can you be more specific?
1. Choose a more specific name
2. Choose a year
3. Choose a genre
4. Choose a console of platform
5. Print the games you have so far
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
b. Global sales

Type the number(s) and/or letter(s) you want, in the order you want them.\n(If you would like them all, put a *): ",
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
''',
		5:
'''
*************************************
*    Welcome to the data section!   *

*   Here you will be able to view   *
*   data on any game(s) specified   *
*       by your input. Enjoy!       *
*************************************
What data would you like to see?

Please enter the number that is next to your choice:

1. Sales data for a single game
2. Sales data between multiple games
3. Chart of the most common genres in our database
4. Chart of games that contain a certain character or name? (example: Mario)
0. Quit and go back to main menu

'''
	}
	print(switcher.get(int, "ERROR"))


main()