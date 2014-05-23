This is a program that parses IPUMS census data. It is still in progress and uncommented. 
It uses python's csv library to read .csv files and categorize the values into years, ethnic groups, and occupation fields. 
It outputs data on income, total population, and the percentage of various immigrant groups in certain job fields.

To use this program, put the .csv file in the same folder as analyzer.py

using terminal (or command prompt) navigate to the same folder as analyzer.py

Type in "python3 -i analyzer.py."

The file name is test.csv

Keep in mind that if you choose to monitor progress, the program will first check the number of rows in the input file which will take some time. 

Output goes into results.csv, which will have three tables: occupation data, population data, and income data.

