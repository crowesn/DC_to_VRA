#LUNAvalidate.py

import csv, re, datetime
from csvpython import easyCSV
from Tkinter import *
from tkFileDialog import askopenfilename
from operator import eq

print 'file compare check \n\n\n'

def BrowseFiles():#file explorer
	root=Tk()
	root.withdraw()
	filenameOUT = askopenfilename(filetypes=[("CSV files", "*.csv"), ("All the files", "*.*")], title="DRC to Luna Converter")
	filename = filenameOUT
	filepath = re.sub('(.*)/.*?$', '\\1/', filename)
	print filepath
	root.destroy()
	print '\n\nSelected file: \"' + re.sub('.*/(.*?)$', '\\1\"', filename)

	return filename, filepath





reStart = ''

while reStart == '' or reStart == 'y':
	inputfile, filepath = BrowseFiles()#'DRCtest.csv'

	#instantiate class
	g = easyCSV(inputfile)
	a = easyCSV(filepath + 'linkdata.txt')
	
	data = g.data
	linkdata = a.linkdata
	for row in linkdata:
		row[0] = re.sub('\.tif', '', row[0])
	
	#print linkdata
	
	build = g.empty_set
	
	LocCheck = g.column_by_header(data, 'Loc Check')
	ReproID = g.column_by_header(data, 'Reproduction Record ID')
	g.append_column(build, 'LocCheck', LocCheck)
	g.append_column(build, 'ReproID', ReproID)
	
	out = map(eq, linkdata, build[1:])
	
	for record in out:
		print record
		if record == False:
			print record
			print '\a'
			break
	print '\n\n\n\n\n'

	reStart = ''
	while reStart != 'y' and reStart != 'n':
		reStart = raw_input('\n\n\nWould you like to run validate again? (y/n)\n\n\n')




#raw_input(out)
#raw_input(linkdata[0])
