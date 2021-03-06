#Sources

import os
import sys

import UtilFunc

def sumPairDistance(pathInput, yearbookNamesFile):
#Input:
#		pathInput: path of DIRECTORY with indexed list .csv files
#		yearbookNamesFile: path to name reference FILE
#		pathOutput: name of .csv output file

#Ouput:		
#		Returns a 2D list of name pairs
#Steps:
#		1) open indexedList
#		2) n^2 iterate over the list of indexed values, updating the 2D list of nameValues
#			be careful not to inlude duplicate name-values and same name values

	classSizeConst = 184;  #need to make more general
	classSize = UtilFunc.fileLength(yearbookNamesFile) - 1 # -1 for headers
	if classSizeConst != classSize:
		print '\n\n\n'
		print 'WARNING WARNING: Class Size is ' + str(classSize) + ' which is not 184!!!! *****'
		print 'WARNING WARNING: Class Size is ' + str(classSize) + ' which is not 184!!!! *****'
		print 'WARNING WARNING: Class Size is ' + str(classSize) + ' which is not 184!!!! *****'
		print '\n\n\n'

	memValueSum = [{'score':0.0,'hits':0.0} for j in range(classSize)] #initialize values to zero

	indexListing = os.listdir(pathInput)
	participantCount = 0.0
	for fileInput in indexListing:
		if fileInput[0] == '.':
			continue
		else:
			participantCount += 1

		nameList = UtilFunc.parseDataFromFile(os.path.join(pathInput, fileInput))
			
		for index1, entry1 in enumerate(nameList):
			dim1 = entry1['AlphaIndex']
			if dim1 == 'VERIFY':
				continue
			dim1 = int(dim1)
			pos1 = entry1['WrittenIndex']
			if pos1 == '-':
				continue
			pos1 = int(pos1) + 1

			memValueSum[dim1]['score'] += 1/float(pos1)
			memValueSum[dim1]['hits'] += 1
	for index in range(len(memValueSum)):
		try:
			memValueSum[index]['score'] /= float(memValueSum[index]['hits'])
		except ZeroDivisionError:
			pass #if it's division by 0, then the score will be zero, but this is an assumption
	return {'memValueSum':memValueSum}

def writeToFile(memValueSum, yearbookNamesFile, fileOutput):

	#list of dictionaries
	yearbookNames = UtilFunc.parseDataFromFile(yearbookNamesFile)

	with open(fileOutput,'w') as fOut:
		fOut.write('AlphaIndex,MemerableScore,NumberOfLists,YearbookLast,YearbookFirst,GraduatedLLA09\n')
		for index1, entry1 in enumerate(yearbookNames):
			dim1 = int(entry1['AlphaIndex'])

			#TODO rename
			fOut.write('{},{},{},{},{},{}\n'.format(	dim1,
				   									memValueSum[dim1]['score'],
				   									memValueSum[dim1]['hits'],
				   									entry1['YearbookLast'],
				   									entry1['YearbookFirst'],
				   									entry1['GraduatedLLA09']))

	#TODO

########################
#####     MAIN     #####
########################
usageDescription = ['pathInput: A full path to a .csv file containing indexed remembered names',
					'yearbookNamesFile: A full path to a .csv file containing all expected classmates names along with their alphabetical index, among other details. See full documentation for extensive details',
					'fileOutput: A full path to a .csv file']
UtilFunc.checkInputArgs(3,usageDescription)

pathInput = sys.argv[1]
yearbookNamesFile = sys.argv[2]
fileOutput = sys.argv[3]

memValueSum = sumPairDistance(pathInput, yearbookNamesFile)['memValueSum']

writeToFile(memValueSum, yearbookNamesFile, fileOutput)

