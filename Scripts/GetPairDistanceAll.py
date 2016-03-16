#Sources

import os
import sys

import UtilFunc

def checkInputArgs():
	if len(sys.argv) != 4:
		sys.exit('Error: Incorrect usage. Script requires 3 input arguments.')

def fileLength(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

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
	classSize = fileLength(yearbookNamesFile) - 1 # -1 for headers
	if classSizeConst != classSize:
		print '\n\n\n'
		print 'WARNING WARNING: Class Size is ' + str(classSize) + ' which is not 184!!!! *****'
		print 'WARNING WARNING: Class Size is ' + str(classSize) + ' which is not 184!!!! *****'
		print 'WARNING WARNING: Class Size is ' + str(classSize) + ' which is not 184!!!! *****'
		print '\n\n\n'

	# pairValueSum = [[0]*classSize]*classSize #initialize classSize x classSize list #bug in this
	pairValueSum = [[0 for i in range(classSize)] for j in range(classSize)]

	indexListing = os.listdir(pathInput)
	participantCount = 0.0
	for fileInput in indexListing:
		if fileInput[0] == '.':
			continue
		else:
			participantCount += 1

		print '#{}\t{}'.format(participantCount,fileInput)
		fileData = UtilFunc.parseDataFromFile(os.path.join(pathInput,fileInput))
		for p in fileData:
			pairValueSum[p['AlphaIndex_1']][p['AlphaIndex_2']] += float(p['PairScore'])
		# with open(os.path.join(pathInput, fileInput), 'r') as fIn:
		# 	for index, line in enumerate(fIn):
		# 		#Skip the heading
		# 		if index > 0:
		# 			(alphaIndex_1,alphaIndex_2,pairScore,last_1,first_1,last_2,first_2) = line.replace('\r','').replace('\n','').split(',')
		# 			pairValueSum[int(alphaIndex_1)][int(alphaIndex_2)] += float(pairScore)
		
	# print pairValueSum
	# print 'WHAT: {}'.format(float(participantCount))
	# print 'CHECKIT: {}'.format(pairValueSum[0][0]/float(participantCount))
	tempDict = {}
	for index1 in range(classSize):
		# if index1 == 0:
		# 	print 'only once'
		for index2 in range(classSize):
			# if (index1,index2) not in tempDict:
			# 	tempDict[(index1,index2)] = 0
			# else:
				# print 'REPeAT!!!'
			#normalize the pair value number by dividing it by the number of participants
			#TODO: add division by zero error handling
			pairValueSum[index1][index2] /= float(participantCount)
			# print pairValueSum[index1][index2]
	print pairValueSum[0][0]
	return {'pairValueSum':pairValueSum}

def writeToFile(pairValueSum, yearbookNamesFile, fileOutput):

	#list of dictionaries
	yearbookNames = UtilFunc.parseDataFromFile(yearbookNamesFile)

	with open(fileOutput,'w') as fOut:
		fOut.write('AlphaIndex_1,AlphaIndex_2,PairScore,Last_1,First_1,Last_2,First_2\n')
		for index1, entry1 in enumerate(yearbookNames):
			for index2, entry2 in enumerate(yearbookNames):
				if index1 != index2:
					dim1 = int(entry1['AlphaIndex'])
					dim2 = int(entry2['AlphaIndex'])

					#TODO rename
					fOut.write('{},{},{},{},{},{},{}\n'.format(	dim1,
						   										dim2,
						   										pairValueSum[dim1][dim2],
						   										entry1['YearbookLast'],
						   										entry1['YearbookFirst'],
						   										entry2['YearbookLast'],
						   										entry2['YearbookFirst']))

	#TODO

########################
#####     MAIN     #####
########################
usageDescription = ['pathInput: A full path to a directory containing .csv file result of individual pair distances',
					'yearbookNamesFile: A full path to a .csv file containing all expected classmates names along with their alphabetical index, among other details. See full documentation for extensive details',
					'fileOutput: A full path to a .csv file']
UtilFunc.checkInputArgs(3, usageDescription)

pathInput = sys.argv[1]
yearbookNamesFile = sys.argv[2]
fileOutput = sys.argv[3]

pairValueSum = sumPairDistance(pathInput, yearbookNamesFile)['pairValueSum']

writeToFile(pairValueSum, yearbookNamesFile, fileOutput)

