import os
import filecmp
import re
from dateutil.relativedelta import *
from datetime import date


def getData(file):
# get a list of dictionary objects from the file
#Input: file name
#Ouput: return a list of dictionary objects where
#the keys are from the first row in the data. and the values are each of the other rows
	
	inFile = open(file, 'r').read()

	lst1 = []
	lines = inFile.split('\n')
	for l in lines:
		cells = l.split(',')
		lst1.append(cells)

	first_line = lst1[0]
	lst2 = lst1[1:]
	lst_of_dict = []
	for x in lst2:
		d = {}
		for idx in range(len(x)):
			d[first_line[idx]] = x[idx]
		lst_of_dict.append(d)

	return lst_of_dict


def mySort(data,col):
# Sort based on key/column
#Input: list of dictionaries and col (key) to sort on
#Output: Return the first item in the sorted list as a string of just: firstName lastName
	
	sorted_data = sorted(data, key=lambda x: x[col])

	firstName = sorted_data[0]['First']
	lastName = sorted_data[0]['Last']
	output = firstName + " " + lastName
	
	return output


def classSizes(data):
# Create a histogram
# Input: list of dictionaries
# Output: Return a list of tuples sorted by the number of students in that class in
# descending order
# [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]
	
	fresh = 0
	soph = 0
	jun = 0
	sen = 0
	for student in data:
		if student['Class'] == 'Freshman':
			fresh += 1
		elif student['Class'] == 'Sophomore':
			soph += 1
		elif student['Class'] == 'Junior':
			jun += 1
		else:
			sen += 1

	classes_dict = {'Freshman':fresh, 'Sophomore':soph, 'Junior':jun, 'Senior':sen}
	sorted_classes = sorted(classes_dict.items(), key=lambda x: x[1], reverse=True)

	return sorted_classes


def findMonth(a):
# Find the most common birth month form this data
# Input: list of dictionaries
# Output: Return the month (1-12) that had the most births in the data

	dates = []
	for student in a:
		dates.append(student['DOB'])

	months = []
	for date in dates:
		x = re.findall('(\d{1,2})/\d{1,2}/\d{4}', date)
		months += x

	freq = {}
	for month in months:
		if month not in freq:
			freq[month] = 0
		freq[month] += 1

	sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

	return int(sorted_freq[0][0])


def mySortPrint(a,col,fileName):
#Similar to mySort, but instead of returning single
#Student, the sorted data is saved to a csv file.
# as fist,last,email
#Input: list of dictionaries, col (key) to sort by and output file name
#Output: No return value, but the file is written

	outFile = open(fileName, 'w')

	sorted_data = sorted(a, key=lambda x: x[col])

	for student in sorted_data:
		first = student['First']
		last = student['Last']
		email = student['Email']
		outFile.write('{},{},{}\n'.format(first, last, email))

	outFile.close()


def findAge(a):
# def findAge(a):
# Input: list of dictionaries
# Output: Return the average age of the students and round that age to the nearest
# integer.  You will need to work with the DOB and the current date to find the current
# age in years.

	today = date.today()
	current_year = today.year
	current_month = today.month
	current_day = today.day

	total_age = 0
	for student in a:
		dob = student['DOB']
		year = re.findall('\d{1,2}/\d{1,2}/(\d{1,4})', dob)
		month = re.findall('(\d{1,2})/\d{1,2}/\d{1,4}', dob)
		day = re.findall('\d{1,2}/(\d{1,2})/\d{1,4}', dob)

		date_of_birth = date(int(year[0]), int(month[0]), int(day[0]))

		age = abs(today - date_of_birth)
		age_in_days = int((str(age)).split()[0])
		age_in_years = age_in_days / 365

		total_age += age_in_years

	avg_age = total_age / len(a)

	return int(avg_age)


################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ", end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB.csv')
	total += test(type(data),type([]),50)

	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',25)
	total += test(mySort(data2,'First'),'Adam Rocha',25)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',25)
	total += test(mySort(data2,'Last'),'Elijah Adams',25)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',25)
	total += test(mySort(data2,'Email'),'Orli Humphrey',25)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],25)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],25)

	print("\nThe most common month of the year to be born is:")
	total += test(findMonth(data),3,15)
	total += test(findMonth(data2),3,15)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,20)

	print("\nTest of extra credit: Calcuate average age")
	total += test(findAge(data), 40, 5)
	total += test(findAge(data2), 42, 5)

	print("Your final score is " + str(total))

# Standard boilerplate to call the main() function that tests all your code
if __name__ == '__main__':
    main()
