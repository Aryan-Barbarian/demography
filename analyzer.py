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

	def data(self):
		rows = []
		for k,v in self.groups.items():
			rows.append(v.percentages)
		return rows

class Group:
	#sorted by occupation
	def __init__(self, name):
		self.name = name
		self.members = dict()
		self.totals = dict()
		self.total_population = 0
		self.percentage_vals = False

	def add(self, person):
		self.percentage_vals = False

		occupation = person.occupation
		self.total_population += person.weight

		if occupation in self.members.keys():
			self.members[occupation].append(person)
			self.totals[occupation] += person.weight
		else:
			self.members[occupation] = [person]
			self.totals[occupation] = person.weight

	def generate_percentages(self):
		self.percentage_vals = {"Group":self.name}
		#self.percentage_vals = dict()

		for k,v in self.totals.items():
			self.percentage_vals[k] = v*1.0 / self.total_population

	@property
	def percentages(self):
		if self.percentage_vals:
			return self.percentages
		else:
			self.generate_percentages()
			return self.percentage_vals






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
		return "other occupation"#+ str(code)

Person.ancestry_codes = \
	{"Hispanic": set(range(200,297)),\
	"White": set(range(1,196)).union(set(range(900,995))),\
	"Chinese" : set(range(706,719))}

Person.birthplace_codes ={"Hispanic Country": set([200,210,250,300]),\
						 "USA": set(range(1,100)),\
						 "China": {500}}

Person.occupation_codes = {"Science": set(range(37,155)),\
						 "Engineering": {},\
						 "Blue Collar": {}}
	

years = {"0":Year(0)}

with open('usa_00011.csv') as csvfile:
	spamreader = csv.DictReader(csvfile, delimiter=',')
	#print(spamreader.fieldnames)
	#spamreader[0]
	for i in spamreader:
		#print(i)
		if (i["YEAR"] in years.keys()):
			years[i["YEAR"]].add(i)
		else:
			years[i["YEAR"]] = Year(i["YEAR"])


test1 = years["2000"].groups["Hispanic Descendant"]
test2 = years["2000"]


ofile  = open('results.csv', "w", newline = "")
params = ["Year","Group", "other occupation", "Science"]
writer = csv.DictWriter(ofile, params, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerow({a:a for a in params})
for k,year in years.items():

	for row in year.data():
		row["Year"] = year.year
		#print(row)
		writer.writerow(row)


ofile.close()