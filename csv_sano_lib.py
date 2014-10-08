#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from datetime import *
import os.path


# read settings.ini helper methods
def read_line_helper(f):
	line = f.readline().strip()
	return read_helper_comma(read_helper_equals(line))
def read_helper_equals(f):
	return [x.strip() for x in f.split('=')]
def read_helper_comma(f):
	return [x.strip() for x in f[1].split(',')]
def read_helper_temp_line(f):
	return f.readline().strip()

# backup file
def backup(file):
	if (os.path.isfile(file)):
		with open(file, 'r') as f:
			bak = f.read()
		filename = file.split('.')
		filename.insert(1, 'bak')
		if len(filename) > 2:
			filename = "{0}-{1}.{2}".format(filename[0], filename[1], filename[2])
		else:
			filename = "{0}.{1}".format(filename[0], filename[1])
		with open(filename, 'w') as f:
			f.write(bak)

# read csv specific column from specific row
def get_data(file, delim, this_row, column):
	data = []
	# file_n = 0
	for fl in file:
		assert os.path.isfile(fl)
		with open(fl, 'rb') as f:
			reader = csv.reader(f, delimiter=';')
			i = 0
			do_break = 0
			for row in reader:
				# Check if date is the same
				if i > this_row - 1:
					try:
						date_previous = datetime.strptime(row[column - 2].split(' ')[0], '%d.%m.%Y').date()
					except ValueError:
						date_previous = datetime.strptime(row[column - 2].split(' ')[0], '%Y-%m-%d').date()
					if (date == date_previous):
						data[-1] = "n/d"
					if do_break == 1:
						break
				if i == this_row - 1:
					data.append(row[column - 1])
					try:
						date =  datetime.strptime(row[column - 2].split(' ')[0], '%d.%m.%Y').date()
					except ValueError:
						date = datetime.strptime(row[column - 2].split(' ')[0], '%Y-%m-%d').date()
					do_break = 1
				i += 1
	data.insert(0, date.today())
	return data

# append to csv file
def write_to_csv(file, delim, data):
	if os.path.isfile(file):
		backup(file)
	# else:
	# 	with open(file, 'w') as f:
	# 		titles = delim.join("B1")
	with open(file, 'ab') as f:
		# Line treminator prevent Windows to insert blank line between records
		writer = csv.writer(f, delimiter=delim, lineterminator='\n')
		writer.writerow(data)

# write_to_csv('csv-tes2.csv', ';', get_data('5', ';', 0, [0, 2]))

# read titles from csv
def read_titles(file, delim):
	assert os.path.isfile(file)
	with open(file, 'rb') as f:
		reader = csv.reader(f, delimiter=';')
		return reader.next()

# print read_titles('csv-tes2.csv', ';')

# Read month of data
def read_month(file, delim, year, month):
	assert os.path.isfile(file)
	day = 1
	if month < 10:
		month = str('0{0}'.format(month))
	else:
		month = str(month)
	selected = []
	select_date = datetime.strptime('{0}-{1}-{2}'. \
		format(year, month, day), '%Y-%m-%d').date()
	with open(file, 'rb') as f:
		reader = csv.reader(f, delimiter=delim)
		for row in reader:
			row_date = datetime.strptime('{0}'.format(row[0]), '%Y-%m-%d').date()
			if row_date.year == select_date.year and row_date.month == select_date.month:
				selected.append(row)
	return selected

# read all data and return it
def all_data(file, delim):
	"""
	Read all data from csv and return it
	"""
	assert os.path.isfile(file)
	data = []
	with open(file, 'rb') as f:
		reader = csv.reader(f, delimiter=delim)
		for row in reader:
			row[0] = datetime.strptime('{0}'.format(row[0]), '%Y-%m-%d').date()
			data.append()
	return data

