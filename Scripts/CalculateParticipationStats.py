import os
import sys
import numpy

import UtilFunc

def countListedNames(pathInput):
	
	fileListing = os.listdir(pathInput)
	participantCounts = {'TotalListed':{'count':[],'classSize':[]}, 
						 'Grad09Listed':{'count':[],'classSize':[]}}
	classSizeTotal = 0
	classSizeGrad09 = 0
	classSizeSet = False
	classmateIndexes = []
	for fileInput in fileListing:
		#sometimes there are hidden files that break the script
		if(fileInput[0] == '.'):
			continue

		fileData = UtilFunc.parseDataFromFile(os.path.join(pathInput,fileInput))
		counterTotal = 0
		counterGrad09 = 0
		for line in fileData:
			if line['WrittenIndex'] != '-':
				counterTotal += 1
				if line['GraduatedLLA09'] == 'Yes':
					counterGrad09 += 1
			if classSizeSet == False and line['AlphaIndex'] not in classmateIndexes:
				if line['GraduatedLLA09'] == 'Yes':
					classSizeGrad09 += 1
				classSizeTotal += 1
				classmateIndexes.append(line['AlphaIndex'])
		classSizeSet = True
		# with open(os.path.join(pathInput, fileInput), 'r') as fIn:
		# 	counterTotal = 0
		# 	counterGrad09 = 0
		# 	for index2, line in enumerate(fIn):
		# 		#Skip the heading
		# 		if index2 > 0:
		# 			(l0,l1,l2,l3,l4,l5,l6,l7) = line.replace('\r','').replace('\n','').split(',')
		# 			if l1 != '-':
		# 				counterTotal += 1
		# 				if l7 == 'Yes':
		# 					counterGrad09 += 1
		# 			if classSizeSet == False and int(l0) not in classmateIndexes:
		# 				if l7 == 'Yes':
		# 					classSizeGrad09 += 1
		# 				classSizeTotal += 1
		# 				classmateIndexes.append(int(l0))
		# 	classSizeSet = True
			# print 'index: ' + str(index1) + '\tcounter: ' + str(counter) + '\t' + fileInput 
			# print counterGrad09
		participantCounts['TotalListed']['count'].append(counterTotal)
		participantCounts['Grad09Listed']['count'].append(counterGrad09)
		participantCounts['TotalListed']['classSize'] = classSizeTotal
		participantCounts['Grad09Listed']['classSize'] = classSizeGrad09
				  
	return participantCounts

def calculateStats(listOfCounts):
	stats = {}
	stats['ClassSize'] = listOfCounts['classSize']
	stats['SampleSize'] = len(listOfCounts['count'])
	stats['Min'] = numpy.min(listOfCounts['count'])
	stats['Max'] = numpy.max(listOfCounts['count'])
	stats['Mean'] = numpy.mean(listOfCounts['count'])
	stats['STD'] = numpy.std(listOfCounts['count'])

	print listOfCounts
	
	return stats

def writeToFile(dataStats, fileOutput):
	with open(fileOutput,'w') as fOut:
		for index, (key, value) in enumerate(dataStats.iteritems()):
			fOut.write(str(key))
			if index + 1 == len(dataStats):
				fOut.write('\n')
			else:
				fOut.write(',')
		for index, (key, value) in enumerate(dataStats.iteritems()):
			fOut.write(str(value))
			if index + 1 < len(dataStats):
				fOut.write(',')

########################
#####     MAIN     #####
########################
usageDescription = ['pathInput: A full path to a directory with indexed list files',
					'fileOutput: A full path to a .csv file']
UtilFunc.checkInputArgs(2, usageDescription)

pathInput = sys.argv[1]
fileOutput = sys.argv[2]

participantCounts = countListedNames(pathInput)
# statsOfTotal = calculateStats([i['TotalListed'] for i in participantCounts])
statsofGrad09 = calculateStats(participantCounts['Grad09Listed'])
writeToFile(statsofGrad09, fileOutput)
