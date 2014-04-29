import csv

class Year:
	def __init__(self,year_num):
		self.year = year_num
		vanilla = list()
		hispanic_direct = list()
		hispanic_descendant = list()
	def add(self,row):
		person = Person(row)
		#FIX THIS


class Person:
	def __init__(self,row):
		Person.ancestry_codes = {"Hispanic": {},\
								 "White": {},\
								 "Chinese": {}}\
		Person.birthplace_codes ={"Hispanic Country": {},\
								 "USA": {},\
								 "China": {}}\
		Person.occupation_codes = {"Science": {},\
								 "Engineering": {},\
								 "Blue Collar": {}}\

		ancestry_code = int(row["ANCESTR1"])
		self.ancestry = Person.find_ancestry(ancestry_code)
		self.weight = float(row["PERWT"])
		birthplace_code = int(row["BPL"])
		self.birthplace = Person.find_birthplace(birthplace_code)
		occupation_code = int(row["OCC1990"])
		self.occupation = Person.find_occupation(occupation_code)
	
	def find(dictionary,code):
		for key,value in dictionary.items():
			if code in value:
				return key

	def find_ancestry(code):
		return find(Person.ancestry_codes, code)
	def find_birthplace(code):
		return find(Person.birthplace_codes, code)
	def find_occupation(code):
		return find(Person.occupation_codes, code)
	

years = {"0":Year(0)}

with open('usa_00006.csv') as csvfile:
	spamreader = csv.DictReader(csvfile, delimiter=',')
	print(spamreader.fieldnames)
	#spamreader[0]
	for i in spamreader:
		print(i)
		if (i["YEAR"] in years.keys()):
			years[i["YEARS"]].add(i)
		