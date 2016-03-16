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

	# pairValues = [[0]*classSize]*classSize #initialize classSize x classSize list #makes an error, probably list copying :(
	pairValues = [[0 for i in range(classSize)] for j in range(classSize)]

	nameList = UtilFunc.parseDataFromFile(fileInput)
	# with open(fileInput, 'r') as fIn:
	# 	for index, line in enumerate(fIn):
	# 		#Skip the heading
	# 		if index > 0:
	# 			(l0,l1,l2,l3,l4,l5,l6,l7) = line.replace('\r','').replace('\n','').split(',')
	# 			nameList.append({'AlphaIndex':l0,'WrittenIndex':l1,'YearbookLast':l4,'YearbookFirst':l5})
		
	for index1, entry1 in enumerate(nameList):
		for index2, entry2 in enumerate(nameList):
			if index1 != index2:
				dim1 = entry1['AlphaIndex']
				if dim1 == 'VERIFY':
					continue
				dim1 = int(dim1)

				dim2 = entry2['AlphaIndex']
				if dim2 == 'VERIFY':
					continue
				dim2 = int(dim2)

				pos1 = entry1['WrittenIndex']
				pos2 = entry2['WrittenIndex']
				if pos1 == '-' or pos2 == '-':
					continue
				# if pos2 == '-':
					# pos2 = classSize
				pos1 = int(pos1)
				pos2 = int(pos2)

				pairValues[dim1][dim2] = 1/float(abs(pos1 - pos2))
				# pairValues[dim2][dim1] = pairValues[dim1][dim2] #redundancy for ease of use
			# print 'dim1: {}\tdim2: {}\tpairValues:{}'.format(dim1,dim2,pairValues[dim1][dim2])
	return {'pairValues':pairValues}

def writeToFile(pairValues, yearbookNamesFile, fileOutput):

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
UtilFunc.checkInputArgs(3,usageDescription)



fileInput = sys.argv[1]
yearbookNamesFile = sys.argv[2]
fileOutput = sys.argv[3]


pairValues = pairDistance(fileInput, yearbookNamesFile)['pairValues']

writeToFile(pairValues, yearbookNamesFile, fileOutput)

