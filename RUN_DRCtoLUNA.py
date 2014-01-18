#	DRCtoLUNA.py

import csv, re, datetime
from csvpython import easyCSV
from Tkinter import *
from tkFileDialog import askopenfilename

################################
#                              #
#  Use easyCSV to take input   #
#  CSV; parse, edit, build,    # 
#  and output changed CSV.     #
#                              #
################################


print """  _____  _____   _____   _          _     _    _ _   _          
 |  __ \|  __ \ / ____| | |        | |   | |  | | \ | |   /\    
 | |  | | |__) | |      | |_ ___   | |   | |  | |  \| |  /  \   
 | |  | |  _  /| |      | __/ _ \  | |   | |  | | . ` | / /\ \  
 | |__| | | \ \| |____  | || (_) | | |___| |__| | |\  |/ ____ \ 
 |_____/|_|  \_\\\\_____|  \__\___/  |______\____/|_| \_/_/    \_\
                                                               
				Sean Crowe, Carolyn Hansen -- 09-09-2013"""

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

def Singlefy(x):#remove trailing 's' from plural nouns in list
	out = []
	for row in x:
		subbed = re.sub('s$', '', row)
		out.append(subbed)
	return out

def Plurify(x):#append 's' to singular nouns in list
	out = []
	for row in x:
		subbed = row + 's'
		out.append(subbed)
	return out

def LowerCase(x):#make all terms in list lowercase
	out = []
	for row in x:
		row = row.lower()
		out.append(row)
	return out


def countCheck(x):#verify number of subject and description fields
	check = x[0]
	if check.count('subject') > 3:
		print '\a\a\a\a\n\tCheck \'subject\' fields'
	if check.count('subject:lcsh') > 2:
		print '\a\a\a\a\n\tCheck \'subject:lsch\' fields'
	if check.count('format:medium') > 2:
		print '\a\a\a\a\\n\tCheck \'format:medium\' fields'
	if check.count('description') > 2:
		print '\a\a\a\a\n\tCheck \'description\' fields'
	if check.count('description:notes') != 2:
		print '\a\a\a\a\n\tCheck \'description:notes\' fields'
	if check.count('contributor:author') > 2:
		print '\a\a\a\a\n\tCheck \'contributor:author\' fields'
	return

def validate(x):#check for unexpected fields
	validateList = ['contributor:author','contributor:author','contributor:photographer','coverage:spatial','description:notes','description','description','date:created','date:digitized','format:medium','format:medium','format:extent','format:mimetype','publisher:OLinstitution','publisher:OLrepository','publisher:digital','relation:ispartof','relation:ispartofseries','rights:uri-*','rights-*','subject','subject','subject','subject:lcsh','subject:lcsh','description:notes','title','type','ResourceLocation']

	for record in x[0]:
		if record not in validateList:
			print '\a\a\a\a\nUnexpected field: \"%s\"' % record
	return


#Get starting REcord ID for sequence
StartNum = int(raw_input('\nStarting number from LinkData.txt sequence (start at 1): ')) - 1
inputfile, filepath = BrowseFiles()#'DRCtest.csv'

#instantiate class
g = easyCSV(inputfile)

#assign input data to variable
data = g.data
countCheck(data)#check number of input fields to make sure not leaving anything out
validate(data)#validate input fields, report on unexpected content

#build empty set and assign to variable
build = g.empty_set

###############################
#                             #
#  Build data for output csv  #
#                             #
###############################



#Work Record ID, Reproduction Record ID
ResourceLocation = g.column_by_header(data, 'ResourceLocation')
g.append_column(build, 'Loc Check', ResourceLocation)
#g.append_column(build, 'Work Record ID', range(StartNum, StartNum + len(data)))

#Thumbnail Title
ThumbnailTitle = g.column_by_header(data, 'title')
g.append_column(build, 'Thumbnail Title', ThumbnailTitle)

#Thumbnail Creator
g.change_header_name(data, 'contributor:author', 'contributor:author1')
g.change_header_name(data, 'contributor:author', 'contributor:author2')

contributorauthor1 = g.column_by_header(data, 'contributor:author1')
contributorauthor2 = g.column_by_header(data, 'contributor:author2')
if 'contributor:photographer' in g.headers:
	contributorphotographer = g.column_by_header(data, 'contributor:photographer')
	ThumbnailCreator = [b if a == '' else a for a, b in zip(*[contributorauthor2, contributorphotographer])]
else:
	ThumbnailCreator = contributorauthor2

g.append_column(build, 'Thumbnail Creator', ThumbnailCreator)

#Thumbnail Date

g.change_header_name(data, 'date:created', 'date:created1')
if 'date:created' in data[0]:
	g.change_header_name(data, 'date:created', 'date:created2')
for row in data:
	if row[data[0].index('date:created1')] == '':
		row[data[0].index('date:created1')] = row[data[0].index('date:created2')]

DateCreatedRaw = g.column_by_header(data, 'date:created1')
DateCreated = [re.sub('T.*', '', row) for row in DateCreatedRaw]
DateCreated = [re.sub('(\d\d\d\d)-(\d\d)-(\d\d)', '\\2/\\3/\\1', row) for row in DateCreated]
g.append_column(build, 'Thumbnail Date', DateCreated)

#Thumbnail Work Type

g.change_header_name(data, 'format:medium','formatmedium1')
g.change_header_name(data, 'format:medium','formatmedium2')
formatmedium1 = Singlefy(g.column_by_header(data, 'formatmedium1'))
formatmedium2 = Singlefy(g.column_by_header(data, 'formatmedium2'))

ThumbnailWorkType = [b if row == 'gelatin silver print' else 'negative (photographic)' for row, b in zip(formatmedium1, formatmedium2)]
g.append_column(build, 'Thumbnail Work Type', ThumbnailWorkType)



#Work Class
WorkClass = Plurify(LowerCase(g.column_by_header(data, 'type')))
g.append_column(build, 'Work Class', WorkClass)
#build = g.build_column(build, 'Work Class', 'photographs')

#WorkType
WorkType = [b if row == 'gelatin silver print' else 'negative (photographic)' for row, b in zip(formatmedium1, formatmedium2)]
g.append_column(build, 'Work Type', WorkType)

#Title
Title = g.column_by_header(data, 'title')
g.append_column(build, 'Title', Title)

#Title Type
build = g.build_column(build, 'Title Type', 'constructed title')

#Measurements
Measurements = g.column_by_header(data, 'format:extent')
f = lambda x:str(float(x.group(0)) * 2.54)
Measurements = [row.replace('"', '') for row in Measurements]
Measures = [re.sub('\d+', f, row) for row in Measurements]
Measurements = [re.sub('(.*)', ' cm (\\1 inches)', row) for row in Measurements]

Measures = [Measure + Measurement for Measure, Measurement in zip(Measures, Measurements)]

g.append_column(build, 'Measurements', Measures)

#Measurement Type
build = g.build_column(build, 'Measurement Type', 'overall')

#Material
Material = Singlefy(['gelatin silver negative' if re.search('acetate|cellulose', row) else row for row in LowerCase(formatmedium1)])
g.append_column(build, 'Material', Material)

#MaterialType
build = g.build_column(build, 'Material Type', 'medium')

#Material2
Material2 = ['paper (fiber product)' if row == 'gelatin silver print' else row for row in formatmedium1]
Material2 = ['dry plate negative' if row == 'glass negative' else row for row in LowerCase(Material2)]
g.append_column(build, 'Material2', Material2)

#Material Type2
MaterialType2 = ['support' if row == 'gelatin silver print' or row == 'gelatin silver negative' or row == 'acetate negative' else 'medium' for row in Material]
g.append_column(build, 'Material Type2', MaterialType2)

#Material3
if 'cellulose acetate' in formatmedium1:
	Material3 = ['acetate film' if row == 'cellulose acetate' else '' for row in formatmedium1]
	g.append_column(build, 'Material3', Material3)

#Material Type3
if 'Material3' in build[0]:
	MaterialType3 = ['support' if row != '' else '' for row in Material3]
	g.append_column(build, 'Material Type3', MaterialType3)

#Technique
build = g.build_column(build, 'Technique', 'photography')

#Technique2
Technique2 = ['dry plate process' if row == 'glass negative' else 'gelatin silver process' for row in LowerCase(Material)]
g.append_column(build, 'Technique2', Technique2)

#Creator (personal)
if 'contributor:photographer' in g.headers:
	contributorphotographer = g.column_by_header(data, 'contributor:photographer')
	g.append_column(build, 'Creator', contributorphotographer)
	PersonalCreatorType = ['personal name' if row != '' else '' for row in contributorphotographer]
	PeronalCreatorRole = ['photographer' if row != '' else '' for row in contributorphotographer]
	g.append_column(build, 'Creator Type', PersonalCreatorType)
	g.append_column(build, 'Creator Role', PeronalCreatorRole)

#Creator (corporate)
if 'contributor:photographer' in g.headers:
	contributorphotographer = g.column_by_header(data, 'contributor:photographer')
	Creator = [b if a == 'Unknown photographer' else a for a, b in zip(*[contributorauthor1, contributorauthor2])]
else:
	Creator = contributorauthor2

g.append_column(build, 'Creator', Creator)

#Creator Type
build = g.build_column(build, 'Creator Type', 'corporate name')

#Creator Role
build = g.build_column(build, 'Creator Role', 'governmental body')

#Creator Dates
#build = g.build_column(build, 'Creator Dates', '')

#Date
g.append_column(build, 'Date', DateCreatedRaw)#repeat

#Date Type
build = g.build_column(build, 'Date Type', 'creation')

#Location
Location = g.column_by_header(data, 'description:notes')
g.change_header_name(data, 'description:notes', 'geonote')
g.append_column(build, 'Location', Location)

#Location Type

LocationType = ['creation location' if row != '' else '' for row in Location]
g.append_column(build, 'Location Type', LocationType)

#Location2
if 'subject' in data[0]:
	Location2 = g.column_by_header(data, 'subject')
	g.change_header_name(data, 'subject', 'subject1')
	Location2 = [row + ' (Cincinnati, Ohio)' if row != '' else '' for row in Location2]
	g.append_column(build, 'Location2', Location2)

	#Location Type2
	LocationType2 = [re.sub('[a-zA-Z0-9].*', 'creation location', row) for row in Location2]
	g.append_column(build, 'Location Type2', LocationType2)

#Location3
if 'subject' in data[0]:
	Location3 = g.column_by_header(data, 'subject')
	g.change_header_name(data, 'subject', 'subject2')
	Location3 = [row + ' (Cincinnati, Ohio)' if row != '' else '' for row in Location3]
	g.append_column(build, 'Location3', Location3)
	
	#Location Type3
	LocationType3 = [re.sub('[a-zA-Z0-9].*', 'creation location', row) for row in Location3]
	g.append_column(build, 'Location Type3', LocationType3)

#Location4
if 'subject' in data[0]:
	Location4 = g.column_by_header(data, 'subject')
	g.change_header_name(data, 'subject', 'subject3')
	Location4 = [row + ' (Cincinnati, Ohio)' if row != '' else '' for row in Location4]
	g.append_column(build, 'Location4', Location4)
	
	#Location Type4
	LocationType4 = [re.sub('[a-zA-Z0-9].*', 'creation location', row) for row in Location4]
	g.append_column(build, 'Location Type4', LocationType4)

#Repository
Repository = g.column_by_header(data, 'publisher:OLrepository')
g.append_column(build, 'Repository', Repository)

#Repository Type
build = g.build_column(build, 'Repository Type', 'current repository')

#Style period
build = g.build_column(build, 'Style Period', 'Twentieth century')

#Culture
build = g.build_column(build, 'Culture', 'American')

#Subject
if 'subject1' in data[0]:
	Subject = g.column_by_header(data, 'subject1')
	Subject = [row + ' (Cincinnati, Ohio)' if row != '' else '' for row in Subject]
	g.append_column(build, 'Subject', Subject)

#Subject2
if 'subject2' in data[0]:
	Subject2 = g.column_by_header(data, 'subject2')
	Subject2 = [row + ' (Cincinnati, Ohio)' if row != '' else '' for row in Subject2]
	g.append_column(build, 'Subject2', Subject2)

#Subject 3
if 'subject3' in data[0]:
	Subject3 = g.column_by_header(data, 'subject3')
	Subject3 = [row + ' (Cincinnati, Ohio)' if row != '' else '' for row in Subject3]
	g.append_column(build, 'Subject3', Subject3)

#Subject 4
if 'subject:lcsh' in data[0]:
	Subject4 = g.column_by_header(data, 'subject:lcsh')
	g.change_header_name(data, 'subject:lcsh', 'subject:lcsh1')
	g.append_column(build, 'Subject4', Subject4)

	#Subject Type4
	SubjectType4 = ['LC subject heading' if row != '' else '' for row in Subject4]
	g.append_column(build, 'Subject Type4', SubjectType4)

#Subject 5
if 'subject:lcsh' in data[0]:
	Subject5 = g.column_by_header(data, 'subject:lcsh')
	g.change_header_name(data, 'subject:lcsh', 'subject:lcsh2')
	g.append_column(build, 'Subject5', Subject5)
	
	#Subject Type5
	SubjectType5 = ['LC subject heading' if row != '' else '' for row in Subject5]
	g.append_column(build, 'Subject Type5', SubjectType5)

#Related Work
RelatedWork = g.column_by_header(data, 'relation:ispartofseries')
g.append_column(build, 'Related Work', RelatedWork)

#Relation Type
build = g.build_column(build, 'Relation Type', 'part of')

#Description
if 'description' in data[0]:
	g.change_header_name(data, 'description', 'description1')
	Description = g.column_by_header(data, 'description1')
	Description = ['' if re.search('No information provided', row) else row for row in Description]
	for row in Description:
		if len(row) > 0:
			g.append_column(build, 'Description', Description)
			break


#Description2
if 'description' in data[0]:
	g.change_header_name(data, 'description', 'description2')
	Description2 = g.column_by_header(data, 'description2')
	Description2 = ['' if re.search('No information provided', row) else row for row in Description2]
	for row in Description2:
		if len(row) > 0:
			g.append_column(build, 'Description2', Description2)
			break

#Description3
if 'description:notes' in data[0]:
	g.change_header_name(data, 'description:notes', 'descriptionNotes')
	Description3 = g.column_by_header(data, 'descriptionNotes')
	g.append_column(build, 'Description3', Description3)

#Rights Statement
RightsStatement = g.column_by_header(data, 'rights:uri-*')
g.append_column(build, 'Rights Statement', RightsStatement)

#Rights statement2
RightsStatement2 = g.column_by_header(data, 'rights-*')
g.append_column(build, 'Rights Statement2', RightsStatement2)

#Reproduction Material
ReproductionMaterial = g.column_by_header(data, 'format:mimetype')
g.append_column(build, 'Reproduction Material', ReproductionMaterial)

#ReproductionDate
ReproductionDate = g.column_by_header(data, 'date:digitized')
g.append_column(build, 'Reproduction Date', ReproductionDate)

a = easyCSV(filepath + 'linkdata.txt')
linkdata = a.linkdata
strip_linkdata = []
for row in linkdata:
	if re.search('_a', row[0]):
		strip_linkdata.append(row[0][:-4])

buildout = []
for record in build:
	initrec = record[:]
	initrec.insert(0, initrec[0])
	buildout.append(initrec)
	if record[0] + '_a' in strip_linkdata:
		record[build[0].index('Thumbnail Title')] = record[build[0].index('Thumbnail Title')] + ' (back of photograph)'
		record[build[0].index('Title')] = record[build[0].index('Title')] + ' (back of photograph)'
		record.insert(0, record[0] + '_a')
		buildout.append(record)

g.insert_column(buildout, 'Work Record ID', range(StartNum, StartNum + len(buildout)), 2)
g.insert_column(buildout, 'Reproduction Record ID', range(StartNum, StartNum + len(buildout)), 2)

#Reproduction View Type
checkBack = g.column_by_header(buildout, 'Loc Check')
ReproductionViewType = ['Back of photographic print' if re.search('_a', row) else '' for row in checkBack]
for row in ReproductionViewType:
	if len(row) > 0:
		g.append_column(buildout, 'Reproduction View Type', ReproductionViewType)
		break
#output
g.outputCSV(buildout, re.sub('\.csv', '', inputfile) + 'OUT.csv')


#test bloc
print '\n\nOutput headers:\n\n'
print buildout[0]
raw_input('\n\nHit <ENTER> to exit')

