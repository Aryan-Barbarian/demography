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
			dictionary = {"Group":v.name, "Total Population": v.total_population}
			#print(dictionary)
			rows.append(dictionary)
		return rows

	def average_income_data(self):
		rows = []
		for k,v in self.groups.items():
			#print(v.average_incomes)
			for occupation,average_income in v.average_incomes.items():
				#print("Average income:",average_income)
				dictionary = {"Group":k, "Occupation":occupation, "Average Income":average_income, "Year":self.year}
				rows.append(dictionary)
		return rows

class Group:
	#sorted by occupation
	def __init__(self, name):
		self.name = name
		self.members = dict()
		self.population_totals = dict()
		self.total_population = 0
		self.income_totals = dict()

		self.percentage_vals = False
		self.average_incomes_vals = False


	def add(self, person):
		self.percentage_vals = False

		occupation = person.occupation
		self.total_population += person.weight


		if occupation in self.members.keys():
			self.members[occupation].append(person)
			self.population_totals[occupation] += person.weight
			self.income_totals[occupation] += person.weight*person.income
		else:
			self.members[occupation] = [person]
			self.population_totals[occupation] = person.weight
			self.income_totals[occupation] = person.weight*person.income

	def generate_percentages(self):
		self.percentage_vals = {"Group":self.name}
		#self.percentage_vals = dict()

		for occupation,total_pop in self.population_totals.items():
			self.percentage_vals[occupation] = total_pop*1.0 / self.total_population

		#print(self.percentage_vals)

	def generate_average_incomes(self):
		self.average_incomes_vals = dict()
		#print(self.income_totals)
		
		for occupation in self.income_totals.keys():
			total_income = self.income_totals[occupation]
			self.average_incomes_vals[occupation] = total_income/self.population_totals[occupation]

		#print(self.average_incomes)

	@property
	def percentages(self):
		if self.percentage_vals:
			return self.average_incomes_vals
		else:
			self.generate_percentages()
			return self.percentage_vals

	@property
	def average_incomes(self):
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

		self.type = self.find_type()
		self.weight = float(row["PERWT"])
		self.income = float(row["INCTOT"])

		

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

with open('usa_00016.csv') as csvfile:
	spamreader = csv.DictReader(csvfile, delimiter=',')
	#print(spamreader.fieldnames)
	#spamreader[0]
	should_stop = False
	timer = 1000
	for i in spamreader:
		timer -= 1
		if should_stop:
			break
		if timer < 0:
			should_stop = True

		#print(i)
		if (i["YEAR"] in years.keys()):
			
			years[i["YEAR"]].add(i)
			
		else:
			years[i["YEAR"]] = Year(i["YEAR"])
			#print(i["YEAR"])

ofile  = open('results.csv', "w", newline = "")
params = ["Year","Group", "Engineering", "Math and Computational Science","Natural Science","Health","Post-Secondary Teachers","Blue Collar","Other Occupation"]
writer1 = csv.DictWriter(ofile, params, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer2 = csv.DictWriter(ofile, ["Group","Total Population","Year"], delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer3 = csv.DictWriter(ofile, ["Group","Average Income","Occupation","Year"], delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

writer1.writeheader()
for k,year in years.items():
	for row in year.percentage_data():
		row["Year"] = year.year
		#print(row)
		writer1.writerow(row)
writer2.writeheader()
for k,year in years.items():
	for row in year.total_population_data():
		row["Year"] = year.year
		writer2.writerow(row)
writer3.writeheader()
for k,year in years.items():
	print(year.average_income_data())
	for row in year.average_income_data():
		writer3.writerow(row)




ofile.close()