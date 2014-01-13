#csv_python
from itertools import izip
import csv
def BrowseFiles():#open file explorer
	root=Tk()
	root.withdraw()
	filenameOUT = askopenfilename(filetypes=[("CSV files", "*.csv"), ("All the files", "*.*")], title="DRC to Luna Converter")

class easyCSV:
	def __init__(self, csv_file):
		t = csv.reader(open(csv_file), dialect='excel')
		data = [row for row in t]
		self.headers = data[0]
		self.data = data
		self.empty_set = [[] for x in xrange(len(data))]
		self.linkdata = [row[0].split('\t') for row in data]

	def change_header_name(self, data, find, replace):
		index = data[0].index(find)
		data[0].remove(find)
		data[0].insert(index, replace)
		return	data

	def column_by_header(self, data, header):
		x = []
		for row in data:
			x.append(row[data[0].index(header)])
		return x

	def delete_column_by_header(self, data, header):
		index = data.index(header)
		for row in data:
			del row[index]
		return data

	def insert_column(self, data, name, column, index_after):
		column[0] = name
		for (row, value) in izip(data, column):
			row.insert(index_after, value)
		return data

	def append_column(self, data, name, column):
		column[0] = name
		for (row, value) in izip(data, column):
			row.append(value)
		return data

	def build_column(self, data, input_header, static_value):
		data[0].append(input_header)
		for row in data[1:]:
			row.append(static_value)
		return data

	def outputCSV(self, data, filename):
		with open(filename, 'wb') as f:
			writer = csv.writer(f, dialect='excel')
			writer.writerows(data)
		return
