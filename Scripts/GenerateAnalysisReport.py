import os
import sys

import UtilFunc



def getDataClass(fileInputs):
	dataClass = {}

	for key, fileName in fileInputs.iteritems():
		dataClass[key] = UtilFunc.parseDataFromFile(fileName)

	# print dataClass['Participation']
	return dataClass

def getDataSingle(dataClass):
	### output will be a list of analysis dictionaryies. 
	### 	Each person gets analysis data

	print '<test>{}</test>\n'.format(dataClass['Participation'])
	classSize = int(dataClass['Participation'][0]['ClassSize'])
	###only selects data for graduates. 
	###Total students is greater than the graduate class size.
	#dataParticipation = 
	dataPairAll = [[i for i in dataClass['PairAll'] if i['AlphaIndex_1'] == j] for j in range(classSize)]
	dataMem = [[i for i in dataClass['Memorable'] if i['AlphaIndex'] == j] for j in range(classSize)]	
	print dataMem[0]
	# dataGroup
	# dataSingleMemorySimilarity

	return

def writeToFile(groupData, individualData, pathOutput):

	return -1

########################
#####     MAIN     #####
########################
usageDescription = ['fileInput1 - Participation: A full path to a .csv file containing participation stats',
					'fileInput2 - Pair All: A full path to a .csv file containing relational pair scores between classmates',
					'fileInput3 - Memorable: A full path to a .csv file containing memorability scores for each classmates',
					'fileInput4 - Group Formation: A full path to a .csv file containing students organized into association groups',
					'fileInput5 - Single Memory Similarity: needs clarificaiton',
					'pathOutput: A full path to a directory where all graduates\'s reports will be saved']
UtilFunc.checkInputArgs(6,usageDescription)

fileInputs = {}
fileInputs['Participation'] = sys.argv[1]
fileInputs['PairAll'] = sys.argv[2]
fileInputs['Memorable'] = sys.argv[3]
fileInputs['GroupFormation'] = sys.argv[4]
# fileInputs['SingleMemorySimilarity'] = sys.argv[5]
pathOutput = sys.argv[6]

#TODO need to parse data from file
print fileInputs
dataClass = getDataClass(fileInputs)
dataSingle = getDataSingle(dataClass)

# writeToFile(dataClass, dataSingle, pathOutput)

# line = '0,1,2.64759564284,Aka,Chelsea,Andrade,Franco'
# line.replace('\r','').replace('\n','').split(',')