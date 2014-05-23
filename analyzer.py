import csv
import sys
#####################################################################
#####################################################################
#####################################################################

class Year:
	#sorted by year
	def __init__(self,year_num):
		self.year = year_num
		self.groups = dict()


	def add(self,row):
		"""This takes a row as input and generates a Person.
		It will add the Person to an Immigration Group
		 (e.g. Direct Hispanic Immigrant.) The Group object's
		 add method will organize the person further"""

		person = Person(row)
		if person.type != "other type":
			if person.type not in self.groups.keys():
				group = Group(person.type)
				group.add(person)
				self.groups[person.type] = group
			else:
				self.groups[person.type].add(person)

	def percentage_data(self):
		"""returns an array of rows of percentage data.
		Each row represents an immigration group and each column
		in the row represents the percentage of that immigration group
		that works in a certain field, such as Engineering"""
		rows = []
		for k,v in self.groups.items():
			"""v.percentages is a dictionary mapping the name of an 
			occupationfield to the percentage of v (which is an 
			immigration group) that works in that field.

			(e.g. v can be the group that represents Direct Hispanic Immigrants
				and v.percentages can be a dictionary of occupation fields like
				{"Blue Collar" : 0.20, "Engineering" : 0.10 ... and so on})
			"""
			rows.append(v.percentages)
		return rows

	def total_population_data(self):
		"""returns an array of rows of population data.
		Each row represents an immigration group and the column
		represents the total population of that group."""
		rows = []
		for k,v in self.groups.items():
			"""The following dictionary has the keys "Group" and "Total Population"
			that the csv writer class will use to write this group's total population"""

			dictionary = {"Group":v.name, "Total Population": v.total_population}
			rows.append(dictionary)
		return rows

	def average_income_data(self):
		"""This returns a table of values. The rows represent a combination
		of immigrant group / occupation field (e.g. Direct Hispanic Immigrants in Blue 
		Collar jobs or Chinese Descendants in Engineering jobs) and the average income
		of that group."""
		rows = []
		for k,v in self.groups.items():
			#k is the name of a group (e.g. "Direct Hispanic Immigrants")
			#v is the actual Group object
			for occupation,average_income in v.average_incomes.items():
				dictionary = {"Group":k, "Occupation":occupation, "Average Income":average_income, "Year":self.year}
				rows.append(dictionary)
		return rows

class Group:
	def __init__(self, name):
		self.name = name
		self.population_totals = dict()
		self.total_population = 0
		self.income_totals = dict()

		"""this is somewhat memoization. If these vals have 
		already been calculated they will be equal to those 
		values. They are not generated again and these 
		_vals are returned directly. 

		If a person is added or anything else happens that changes
		what these values SHOULD be equal to, these _vals are set to 
		false, so the next time that percentages or average_incomes 
		are called, these values will be recalculated.
		These _vals will be	set equal to the newly generated values."""
		self.percentage_vals = False
		self.average_incomes_vals = False


	def add(self, person):

		self.percentage_vals = False

		occupation = person.occupation
		self.total_population += person.weight

		#print(self.members)
		if occupation in self.population_totals.keys():
			self.population_totals[occupation] += person.weight
			self.income_totals[occupation] += person.weight*person.income
		else:
			self.population_totals[occupation] = person.weight
			self.income_totals[occupation] = person.weight*person.income

	def generate_percentages(self):

		self.percentage_vals = {"Group":self.name}
		#self.percentage_vals = dict()

		for occupation,total_pop in self.population_totals.items():
			self.percentage_vals[occupation] = total_pop*1.0 / self.total_population

	def generate_average_incomes(self):
		self.average_incomes_vals = dict()
		
		for occupation in self.income_totals.keys():
			total_income = self.income_totals[occupation]
			self.average_incomes_vals[occupation] = total_income/self.population_totals[occupation]

	@property
	def percentages(self):
		"""this is somewhat memoized. It returns percentage_vals,
		and generates percentage_vals before returning it if neccesary.

		It returns a dictionary mapping every occupation field it has 
		(e.g. "Blue Collar" or "Engineering") to the percentage of this
		group's population that works in that field"""
		if self.percentage_vals:
			return self.average_incomes_vals
		else:
			self.generate_percentages()
			return self.percentage_vals

	@property
	def average_incomes(self):
		"""this is somewhat memoized. It returns average_incomes_vals,
		and generates average_incomes_vals before returning it if neccesary.

		It returns a dictionary mapping every occupation field in this group 
		(e.g. "Blue Collar" or "Engineering") to the average income of people
		of this group in that occupation field"""
		if self.average_incomes_vals:
			return self.average_incomes_vals
		else:
			self.generate_average_incomes()
			return self.average_incomes_vals

class Person:
	def __init__(self,row):

		ancestry_code = int(row["ANCESTR1"])
		self.ancestry = Person.find_ancestry(ancestry_code)
		self.weight = float(row["PERWT"])
		birthplace_code = int(row["BPL"])
		self.birthplace = Person.find_birthplace(birthplace_code)
		occupation_code = int(row["OCC1990"])
		self.occupation = Person.find_occupation(occupation_code)
		self.year = int(row["YEAR"])
		self.type = self.find_type()
		self.weight = float(row["PERWT"])
		self.income = float(row["INCTOT"])*inflation_multiplier[self.year]

		

	def find_type(self):
		
		if self.ancestry == "White":
			if self.birthplace == "USA":
				return "Vanilla"
		if self.ancestry == "Hispanic":
			if self.birthplace == "USA":
				return "Hispanic Descendant"
			if self.birthplace == "Hispanic Country":
				return "Direct Hispanic Immigrant"
		if self.ancestry == "Chinese":
			if self.birthplace == "USA":
				return "Chinese Descendant"
			if self.birthplace == "China":
				return "Direct Chinese Immigrant"

		return "other type"
	
	def find(dictionary,code):
		for key,value in dictionary.items():
			if code in value:
				return key

	def find_ancestry(code):
		ans = Person.find(Person.ancestry_codes, code)
		if ans is not None:
			return ans
		return "other ancestry: "#+ str(code)
	def find_birthplace(code):
		ans = Person.find(Person.birthplace_codes, code)
		if ans is not None:
			return ans
		return "other birthplace: "#+ str(code)
	def find_occupation(code):
		ans = Person.find(Person.occupation_codes, code)
		if ans is not None:
			return ans
		return "Other Occupation"#+ str(code)


#####################################################################
#####################################################################
#####################################################################

#this adjusts for inflation to 2014 levels
inflation_multiplier = {1970: 1/0.2329, 1980:1/0.4946 , 1990: 1/0.78,\
	2000: 0.964 , 2010:  0.764, 2012: 1/1.38}

#the following codes can be found on IPUMS
Person.ancestry_codes = \
	{"Hispanic": set(range(200,297)),\
	"White": set(range(1,196)).union(set(range(900,995))),\
	"Chinese" : set(range(706,719))}

Person.birthplace_codes ={"Hispanic Country": set([200,210,250,300]),\
	"USA": set(range(1,100)),\
	"China": {500}}

Person.occupation_codes = \
	{\
	"Engineering": range(44,60),\
	"Math and Computational Science": range(64,69),\
	"Natural Science": range(69,84),\
	"Health":range(84,107),\
	"Post-Secondary Teachers":range(113,155),\
	"Blue Collar": range(473,890)}
	

years = {}


#####################################################################
#####################################################################
#####################################################################

print("~~~~~~~Demography 145AC CSV File Reader~~~~~~~")
should_calculate_progress = input("Do you want to see the program's progress in handling your file? (y/n)\n").lower()

if should_calculate_progress in {"y", "yes","yup"}:
	should_calculate_progress = True
else:
	should_calculate_progress = False #any answer that isn't yes is assumed to mean no


def find_input_file():
	file_name = input("What is the file name?\n")

	try:
	    f = open(file_name)
	    return f
	except (IOError, OSError) as e:
	    try_again = input("That file doesn't seem to exist! Try again? (y/n)\n").lower()
	    if try_again in {"y", "yes","yup"}:
	    	return find_input_file()
	    else:
	    	exit()


input_file = find_input_file()
if should_calculate_progress:
	print("Calculating Number of Rows. (note: this may take a while)")
	counter = csv.DictReader(input_file, delimiter=',')
	row_count = sum(1 for row in counter)
	input_file.seek(0)


reader = csv.DictReader(input_file, delimiter=',')



rows_read = 0

for i in reader:
	if should_calculate_progress:
		sys.stdout.flush()
		print("{0} / {1}\t{2:.2f}%".format(rows_read,row_count, (rows_read/row_count*100)))
		rows_read += 1
	
	"""adds each row to its appropriate year
	the year's add method will parse the row
	and store a Person object with its attributes"""
	if (i["YEAR"] in years.keys()):
		years[i["YEAR"]].add(i)
	else:
		years[i["YEAR"]] = Year(i["YEAR"])


ofile  = open('results.csv', "w", newline = "")
writer1 = csv.DictWriter(ofile, ["Year","Group", "Engineering", "Math and Computational Science","Natural Science","Health","Post-Secondary Teachers","Blue Collar","Other Occupation"], delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer2 = csv.DictWriter(ofile, ["Group","Total Population","Year"], delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer3 = csv.DictWriter(ofile, ["Group","Average Income","Occupation","Year"], delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

writer1.writeheader()
for k,year in years.items():
	for row in year.percentage_data():
		row["Year"] = year.year
		
		writer1.writerow(row)
writer2.writeheader()
for k,year in years.items():
	for row in year.total_population_data():
		row["Year"] = year.year
		writer2.writerow(row)
writer3.writeheader()
for k,year in years.items():
	
	for row in year.average_income_data():
		writer3.writerow(row)




ofile.close()