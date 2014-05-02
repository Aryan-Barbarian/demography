import csv

class Year:
	#sorted by year
	def __init__(self,year_num):
		self.year = year_num
		self.groups = dict()
	def add(self,row):
		person = Person(row)
		if person.type != "other type":
			if person.type not in self.groups.keys():
				group = Group(person.type)
				group.add(person)
				self.groups[person.type] = group
			else:
				self.groups[person.type].add(person)

	def percentage_data(self):
		rows = []
		for k,v in self.groups.items():
			rows.append(v.percentages)
		return rows

	def total_population_data(self):
		rows = []
		for k,v in self.groups.items():
			dictionary = {"Group":v.name, "Total Population": v.total_population, "Year":self.year}
			#print(dictionary)
			rows.append(dictionary)
		return rows
	def wage_data(self):
		rows = []
		for k,v in self.groups.items():
			for occupation,average_wage in v.wages:
				dictionary = {"Occupation": occupation, "Group":k, "Average Wage":average_wage, "Year":self.year}
				rows.append(dictionary)
		return rows

class Group:
	#all members are of the same group (hispanic descendants, for example)
	#sorted by occupation
	def __init__(self, name):
		self.name = name
		self.members = dict()
		self.population_totals = dict()
		self.wage_totals = dict()
		

		self.total_population = 0
		self.percentage_vals = False
		self.wage_vals = False

	def add(self, person):
		self.percentage_vals = False

		occupation = person.occupation
		self.total_population += person.weight

		if occupation in self.members.keys():
			self.members[occupation].append(person)
			self.population_totals[occupation] += person.weight
			self.wage_totals[occupation] += person.income
		else:
			self.members[occupation] = [person]
			self.population_totals[occupation] = person.weight
			self.wage_totals[occupation] = person.income

	def generate_percentages(self):
		self.percentage_vals = {"Group":self.name}
		

		for k,v in self.totals.items():
			self.percentage_vals[k] = v*1.0 / self.total_population
	def generate_wages(self):
		self.wage_vals = {"Group":self.name}

		for k,v in self.wage_totals.items():
			self.wage_vals[k] = v / self.population_totals[k]


	@property
	def percentages(self):
		if self.percentage_vals:
			return self.percentage_vals
		else:
			self.generate_percentages()
			return self.percentage_vals

	@property
	def wages(self):
		if self.wage_vals:
			return self.wage_vals
		else:
			self.generate_wages()
			return self.wage_vals

class Person:
	def __init__(self,row):

		ancestry_code = int(row["ANCESTR1"])
		self.ancestry = Person.find_ancestry(ancestry_code)
		self.weight = float(row["PERWT"])
		birthplace_code = int(row["BPL"])
		self.birthplace = Person.find_birthplace(birthplace_code)
		occupation_code = int(row["OCC1990"])
		self.occupation = Person.find_occupation(occupation_code)

		self.income = float(row["INCTOT"])
		self.type = self.find_type()
		self.weight = float(row["PERWT"])

		

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
	

years = {"0":Year(0)}

with open('usa_00015.csv') as csvfile:
	spamreader = csv.DictReader(csvfile, delimiter=',')
	#print(spamreader.fieldnames)
	#spamreader[0]
	for i in spamreader:
		#print(i)
		if (i["YEAR"] in years.keys()):
			years[i["YEAR"]].add(i)
		else:
			years[i["YEAR"]] = Year(i["YEAR"])
			print(i["YEAR"])

ofile  = open('results.csv', "w", newline = "")
params1 = ["Year","Group", "Engineering", "Math and Computational Science","Natural Science","Health","Post-Secondary Teachers","Blue Collar","Other Occupation"]
params2 = ["Group","Total Population","Year"]
params3 = ["Group","Occupation","Average Income","Year"]

writer1 = csv.DictWriter(ofile, params, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer2 = csv.DictWriter(ofile, params2, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer3 = csv.DictWriter(ofile, params3, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

writer1.writerow({a:a for a in params1})
writer2.writerow({a:a for a in params2})
writer3.writerow({a:a for a in params3})

for k,year in years.items():
	for row in year.percentage_data():
		row["Year"] = year.year
		#print(row)
		writer1.writerow(row)


for k,year in years.items():
	for row in year.total_population_data():
		writer2.writerow(row)

for k,year in years.items():
	for row in year.wage_data():
		writer3.writerow(row)




ofile.close()