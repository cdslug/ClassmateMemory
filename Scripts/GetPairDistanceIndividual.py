import os
import sys

import UtilFunc


def pairDistance(fileInput, yearbookNamesFile):
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
		print 'WARNING WARNING: Class Size is {} which is not {}!!!! *****\n'.format(classSize,classSizeConst) * 3
		print '\n\n'

	pairValues = [[0]*classSize]*classSize #initialize classSize x classSize list

	nameList = UtilFunc.parseDataFromFile(fileInput)
	# with open(fileInput, 'r') as fIn:
	# 	for index, line in enumerate(fIn):
	# 		#Skip the heading
	# 		if index > 0:
	# 			(l0,l1,l2,l3,l4,l5,l6,l7) = line.replace('\r','').replace('\n','').split(',')
	# 			nameList.append({'AlphaIndex(int)':l0,'WrittenIndex(int)':l1,'YearbookLast':l4,'YearbookFirst':l5})
		
		for index1, entry1 in enumerate(nameList):
			for index2, entry2 in enumerate(nameList):
				if index1 != index2:
					dim1 = entry1['AlphaIndex(int)']
					if dim1 == 'VERIFY':
						continue
					dim1 = int(dim1)
					dim2 = entry2['AlphaIndex(int)']
					if dim2 == 'VERIFY':
						continue
					dim2 = int(dim2)
					pos1 = entry1['WrittenIndex(int)']
					pos2 = entry2['WrittenIndex(int)']
					if pos1 == '-':
						continue
					if pos2 == '-':
						pos2 = classSize
					pos1 = int(pos1)
					pos2 = int(pos2)

					pairValues[dim1][dim2] = 1/float(abs(pos1 - pos2))
					pairValues[dim2][dim1] = pairValues[dim1][dim2] #redundancy for ease of use
	
	return {'pairValues':pairValues}

def writeToFile(pairValues, yearbookNamesFile, fileOutput):

	#list of dictionaries
	yearbookNames = []

	with open(yearbookNamesFile, 'r') as fYBN:
		for index, line in enumerate(fYBN):
			#Skip the heading
			if index > 0:
				(l0,l1,l2,l3) = line.replace('\r','').replace('\n','').split(',')
				yearbookNames.append({	'AlphaIndex(int)':l0,
										'YearbookLast':l1,
										'YearbookFirst':l2})

	with open(fileOutput,'w') as fOut:
		fOut.write('AlphaIndex_1(int),AlphaIndex_2(int),PairScore(dec),Last_1,First_1,Last_2,First_2\n')
		for index1, entry1 in enumerate(yearbookNames):
			for index2, entry2 in enumerate(yearbookNames):
				if index1 != index2:
					dim1 = int(entry1['AlphaIndex(int)'])
					dim2 = int(entry2['AlphaIndex(int)'])

					#TODO rename
					fOut.write('{},{},{},{},{},{},{}\n'.format(	dim1,
						   										dim2,
						   										pairValues[dim1][dim2],
						   										entry1['YearbookLast'],
						   										entry1['YearbookFirst'],
						   										entry2['YearbookLast'],
						   										entry2['YearbookFirst']))

	#TODO

########################
#####     MAIN     #####
########################
usageDescription = ['fileInput: A full path to a .csv file of indexed names',
					'yearbookNamesFile: A full path to a .csv file containing all expected classmates names along with their alphabetical index, among other details. See full documentation for extensive details',
					'fileOutput: A full path to a .csv file']
checkInputArgs(3,usageDescription)



fileInput = sys.argv[1]
yearbookNamesFile = sys.argv[2]
fileOutput = sys.argv[3]


pairValues = pairDistance(fileInput, yearbookNamesFile)['pairValues']

writeToFile(pairValues, yearbookNamesFile, fileOutput)

