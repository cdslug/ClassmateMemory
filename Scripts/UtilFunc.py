import os
import sys 
import Levenshtein

def checkInputArgs(numInputs, usageDescription=[]):
	#TODO: need to standardize the description of usageDescription
	#I should consult a help or man page
	if len(sys.argv) != numInputs + 1:
		outputText = 'Error: Incorrect usage. Script requires {} input arguments.\n'.format(numInputs)
		for num,arg in enumerate(usageDescription):
			outputText += 'Arg {})	{}\n'.format(num + 1, arg)
		sys.exit(outputText)
	return 

def fileLength(fname):
	i = 0
	line = []
	with open(fname) as f:
		for i, line in enumerate(f):
			pass
	return i + 1 if not (i == 0 and line == []) else i

def parseNameFromFile(fileName):
	sections = fileName.replace('_','.').split('.')
	# print(sections)
	### sometimes with a new person's raw file, there's not a number
	if(sections[-2].isdigit()):
		return sections[-3]
	else:
		return sections[-2]

def parseNumberFromFile(fileName):
	sections = fileName.replace('_','.').split('.')
	# print(sections)
	if(len(sections) == 5 and sections[-2].isdigit()):
		return sections[-2]
	else:
		return ''

def appendNumberToFileName(fileName,number):
	assert number.isdigit(),'Input Error: number must be a string representing a positive integer'

	fileNameParts = fileName.split('.')
	fileNameParts[0] += '_{}'.format(number)
	fileName = '.'.join(fileNameParts)
	return fileName

def interpretString(string):
	ret = string
	try:
		ret = float(string)
	except ValueError:
		try:
			ret = int(string)
		except ValueError:
			pass
	return ret

def parseDataFromFile(fileInput):
	#list of dictionaries
	# print '\n' + fileInput + '\n'
	fileData = []

	with open(fileInput, 'r') as fin:
		keys = [] ### Dictionary keys read from the csv heading
		for index, line in enumerate(fin):
			if index == 0:
				keys = line.replace('\r','').replace('\n','').split(',')
				# print str(keys) + '\n'
			else:
				lineData = line.replace('\r','').replace('\n','').split(',')
				assert len(lineData) == len(keys),(	'File Format Error: provided .csv file' 
													'does not have matching keys and values.\n'
													'keys: {}\n'
													'line #{} values: {}\n{}'.format(keys,index, lineData,fileInput))
				tempDict = {}
				for index2,k in enumerate(keys):
					tempDict[k] = interpretString(lineData[index2])

				fileData.append(tempDict)
	return fileData

def prepareDirectory(newPath):
	#Input:
	#	name: name of desired directory
	#	inputPath: path to prepare the desired directory
	#Output:
	#	resultingPath: inputPath appended with name of desired directory

	### check if the parent path exists
	parentPath = '/'.join(newPath.split('/')[:-1])
	if not os.path.exists(parentPath):
		sys.exit('Error: {} does not exist'.format(parentPath))

	### There's a possiblity for a race condition
	### but it's unlikely these directories will be deleted immediately after checking if they exist
	if not os.path.exists(newPath):
		try:
			os.makedirs(newPath)
		except OSError:
			sys.exit('Error: could not create {}\nCheck permissions.'.format(newPath))
	return

def getSortedJaroScoreList(name, refIndexNames):
	scoredIndexedNames = []
	for r in refIndexNames:
		jaroTests = []
		test1 = Levenshtein.jaro(name['WrittenFirst'].lower().replace(' ',''), r['YearbookFirst'].lower().replace(' ',''))
		test2 = Levenshtein.jaro(name['WrittenLast'].lower().replace(' ',''), r['YearbookLast'].lower().replace(' ',''))
		jaroTests.append((test1,test2))

		test1 = Levenshtein.jaro(name['WrittenFirst'].lower().replace(' ',''), r['YearbookLast'].lower().replace(' ',''))
		test2 = Levenshtein.jaro(name['WrittenLast'].lower().replace(' ',''), r['YearbookFirst'].lower().replace(' ',''))
		jaroTests.append((test1,test2))

		test1 = Levenshtein.jaro((name['WrittenFirst'] + name['WrittenLast']).lower().replace(' ',''), (r['YearbookFirst'] + r['YearbookLast']).lower().replace(' ',''))
		test2 = test1
		jaroTests.append((test1,test2))

		test1 = Levenshtein.jaro((name['WrittenFirst'] + name['WrittenLast']).lower().replace(' ',''), (r['YearbookLast'] + r['YearbookFirst']).lower().replace(' ',''))
		test2 = test1
		jaroTests.append((test1,test2))
				
		jaroScore = max(map(lambda t:(t[0] + t[1])/2, jaroTests))

		spellingDict = {'Spelling':str(jaroScore)}
		spellingDict.update(r)
		# print(str(spellingDict) + '\n')
		scoredIndexedNames.append(spellingDict)
		if jaroScore == 1: #if you found an exact match, exit early
			break

	return sorted(scoredIndexedNames, key=lambda k: k['Spelling'], reverse=True)

def matchName(name, refIndexNames, debugInput = None):
	#Input:
	#	name: single list of [last,first]
	#	refIndexNames: list of all names in form [index, last, first]
	#Output:
	#	indexedName: closest match of the name. 
	#					If the jaro score was too low, then return index '-' and oritinal name
	CONST_MIN_ACCEPTABLE_SCORE = 0.85
	CONST_NUM_SPELLING_SUGGESTIONS = 3

	sortedScoreList = getSortedJaroScoreList(name, refIndexNames)
	# for n in sortedScoreList:
	# 	print(n['YearbookFirst'] + ' ' + n['YearbookLast'] + ' ' + str(n['Spelling']))

	matchedEntry = {'YearbookFirst':'',
					'YearbookLast':'',
					'AlphaIndex':'VERIFY_INDEX',
					'GraduatedLLA09':'',
					'Spelling':'0.0'}

	matchedEntry.update(name)


	if float(sortedScoreList[0]['Spelling']) < CONST_MIN_ACCEPTABLE_SCORE:
		if debugInput != None:
			debugInput = str(debugInput)
			try:
				index = int(debugInput) - 1
				matchedEntry.update(sortedScoreList[index])
			except ValueError:
				pass
		else:
			correctMatchIndex = 0

			indexOffset = 0
			while True:
				print 'Does \'{} {}\' match any of the names below?'.format(name['WrittenFirst'],name['WrittenLast'])
				#todo: handle end of list of suggestions
				for index in range(0,CONST_NUM_SPELLING_SUGGESTIONS):
					if index + indexOffset >= len(sortedScoreList):
						break
					print('{}: {} {} {}'.format(str(index + indexOffset),
												sortedScoreList[index + indexOffset]['YearbookFirst'],
												sortedScoreList[index + indexOffset]['YearbookLast'],
												sortedScoreList[index + indexOffset]['Spelling']))
				print('-1: Name not listed')
				print('-2: Give up matching')

				try:
					correctMatchIndex = int(raw_input('Enter the number: '))
				except ValueError:
					continue

				if correctMatchIndex < -2:
					print '### Input Error: must be an integer between -2 and {}'.format(index + indexOffset)
				elif correctMatchIndex == -2:
					break
				else:
					if correctMatchIndex in range(0,CONST_NUM_SPELLING_SUGGESTIONS + indexOffset):
						matchedEntry.update(sortedScoreList[correctMatchIndex])
						break
					elif correctMatchIndex == -1:
						indexOffset += CONST_NUM_SPELLING_SUGGESTIONS
					elif correctMatchIndex == -2:
						print('You Gave Up!')
						break
					else:
						continue
			
	#matching with high confidence
	else:
		matchedEntry.update(sortedScoreList[0])
		
	return matchedEntry
