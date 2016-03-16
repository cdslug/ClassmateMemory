#!/usr/bin/env python

### References:
###		Lutz, Mark (2013-06-12). Learning Python (p. 60). O'Reilly Media. Kindle Edition. 

### ClassmateBatch.py
### Runs all other scripts
import os
import sys
import subprocess
import shutil
import re
import Levenshtein

import UtilFunc #custom module
import FixRawList
import IndexList
import GenerateReport


def getNumberFromNameInFile(name, yearbookReferenceFilePath):
	nameSep = re.findall('[A-Z][^A-Z]*',name)
	# print '### name:{0} nameSep: {1}'.format(name, nameSep)
	nameDict = {'WrittenLast':''.join(nameSep[0:-1]),'WrittenFirst':nameSep[-1]}
	yearbookNames = UtilFunc.parseDataFromFile(yearbookReferenceFilePath)
	jaroMatchIndex = UtilFunc.matchName(nameDict, yearbookNames)['AlphaIndex']

	return jaroMatchIndex

def fixRawList(name, number, pathInput, pathOutput):
	fileInput		= os.path.join(pathInput,'Input/RawList_{}_{}.txt'.format(name,number))
	fileComplete	= os.path.join(pathInput,'Complete/RawList_{}_{}.txt'.format(name,number))
	fileError		= os.path.join(pathInput,'Error/RawList_{}_{}.txt'.format(name,number))
	fileOutput		= os.path.join(pathOutput, 'Input/CheckedList_{}_{}.txt'.format(name,number))
	
	# print(fileInput)
	try:
		print('FixingRawList')
		subprocess.call(['python', 'FixRawList.py', fileInput, fileOutput])
		# print(os.listdir(os.path.join(pathInput, 'Input')))
		shutil.copyfile(fileInput,fileComplete)
		os.remove(fileInput)
	except OSError:
		pass

def indexList(name, number, pathInput, pathOutput):
	fileInput		= os.path.join(pathInput,'Input/CheckedList_{}_{}.txt'.format(name,number))
	fileResource	= os.path.join(pathInput,'Resource/IndexedYearbook.csv') #need to confirm resource is a directory
	fileComplete	= os.path.join(pathInput,'Complete/CheckedList_{}_{}.txt'.format(name,number))
	fileError		= os.path.join(pathInput,'Error/CheckedList_{}_{}.txt'.format(name,number))
	fileOutput		= os.path.join(pathInput,'Input/IndexedList_{}_{}.csv'.format(name,number))

	try:
		print('IndexingList')
		subprocess.call(['python', 'IndexList.py', fileInput, fileResource, fileOutput])
		shutil.copyfile(fileInput,fileComplete)
		os.remove(fileInput)
	except OSError:
		pass

def generateReport(name, number, pathInput, pathOutput1, pathOutput2):
	fileInput		= os.path.join(pathInput,'Input/IndexedList_{}_{}.csv'.format(name,number))
	fileComplete1	= os.path.join(pathInput,'Complete/IndexedList_{}_{}.csv'.format(name,number))
	filecomplete2	= os.path.join(pathOutput2,'Input/IndexedList_{}_{}.csv'.format(name,number))
	fileError		= os.path.join(pathInput,'Error/IndexedList_{}_{}.csv'.format(name,number))
	fileOutput		= os.path.join(pathOutput1,'Report_{}_{}.pdf'.format(name,number))

	try:
		print('GeneratingReport')
		subprocess.call(['python', 'GenerateReport.py', fileInput, fileOutput])
		shutil.copyfile(fileInput,fileComplete1)
		shutil.copyfile(fileInput,fileComplete2)
		os.remove(fileInput)
	except OSError:
		pass

def calculateParticipation(pathInput, pathOutput):
	pathInput 	= os.path.join(pathInput, 'Output')
	fileOutput 	= os.path.join(pathOutput, 'ParticipationStatistics.csv')
	subprocess.call(['python', 'CalculateParticipationStats.py', pathInput, fileOutput])

def getPairDistanceIndividual(name, number, pathInput, pathResource, pathOutput):
	# fileInput		= os.path.join(pathInput, 'Input/IndexedList_{}_{}.csv'.format(name,number))
	# fileResource	= os.path.join(pathResource, 'Resource/IndexedYearbook.csv')
	fileResource	= pathResource
	fileInput	= os.path.join(pathInput, 'Input/IndexList_Output_{}_{}.csv'.format(name,number))
	fileError		= os.path.join(pathInput, 'Error/IndexList_{}_{}.csv'.format(name,number))
	fileOutput		= os.path.join(pathOutput, 'Input/PairScores_{}_{}.csv'.format(name,number))

	try:
		print('getPairDistance_Individual')
		subprocess.call(['python', 'GetPairDistanceIndividual.py', fileInput, fileResource, fileOutput])
		# shutil.copyfile(fileInput,fileComplete)
		# os.remove(fileInput)
	except OSError:
		pass

def getPairDistanceAll(pathInput,pathResource,pathOutput):
	fileInput 		= os.path.join(pathInput, 'Input')
	# fileResource 	= os.path.join(pathResource, 'Resource/IndexedYearbook.csv')
	fileResource	= pathResource
	fileOutput 		= os.path.join(pathOutput, 'Output/PairScores_All.csv')
	try:
		print('getPairDistanceAll')
		subprocess.call(['python', 'GetPairDistanceAll.py', fileInput, fileResource, fileOutput])
	except OSError:
		pass

def findMostMemorable(pathInput,pathResource,pathOutput):
	fileInput 		= os.path.join(pathInput, 'Output')
	# fileResource 	= os.path.join(pathResource, 'Resource/IndexedYearbook.csv')
	fileResource	= pathResource
	fileOutput 		= os.path.join(pathOutput, 'MemorableScores.csv')
	try:
		print('findMostMemorable')
		subprocess.call(['python', 'FindMostMemorable.py', fileInput, fileResource, fileOutput])
	except OSError:
		pass


def buildGroupsFromPairs(pathInput, pathResource, pathOutput):
	fileInput 		= os.path.join(pathInput, 'Output/PairScores_All.csv')
	# fileResource 	= os.path.join(pathResource, 'Resource/IndexedYearbook.csv')
	fileResource	= pathResource
	fileOutput 		= os.path.join(pathOutput, 'GroupScores.csv')
	try:
		print('buildGroupsFromPairs')
		subprocess.call(['python', 'BuildGroupsFromPairs.py', fileInput, fileResource, fileOutput])
	except OSError:
		pass

def checkSingleMemorySimilarity(pathInput, pathResource, pathOutput):
	fileInput 		= os.path.join(pathInput, 'Input')
	# fileResource 	= os.path.join(pathResource, 'Resource/IndexedYearbook.csv')
	fileResource	= pathResource
	fileOutput 		= os.path.join(pathOutput, 'IndividualSimilarity.csv')
	try:
		print('buildGroupsFromPairs')
		subprocess.call(['python', 'CheckSingleMemorySimilarity.py', fileInput, fileResource, fileOutput])
	except OSError:
		pass

def checkGroupMemorySimilarity(pathInput1, pathInput2, pathResource, pathOutput):
	fileInput 		= os.path.join(pathInput, 'Output/PairScores_All.csv')
	# fileResource 	= os.path.join(pathResource, 'Resource/IndexedYearbook.csv')
	fileResource	= pathResource
	fileOutput 		= os.path.join(pathOutput, 'GroupSimilarity.csv')
	try:
		print('buildGroupsFromPairs')
		subprocess.call(['python', 'CheckGroupSimilarity.py', fileInput1, fileInput2, fileResource, fileOutput])
	except OSError:
		pass

def generateAnalysisReport(pathInput1, pathInput2, pathInput3, pathInput4, pathInput5, pathOutput):
	fileInput1 		= os.path.join(pathInput1, 'ParticipationStatistics.csv')
	fileInput2 		= os.path.join(pathInput2, 'PairScores_All.csv')
	fileInput3		= os.path.join(pathInput3, 'MemorableScores.csv')
	fileInput4		= os.path.join(pathInput4, 'GroupScores.csv')
	fileInput5 		= os.path.join(pathInput5, 'IndividualSimilarity.csv')
	# fileInput6 		= pathInput6 + '/GroupSimilaryity.csv'
	# a specific fileOutput is provided. The report script will write all reports
	try:
		print('GeneratingAnalysisReport')
		subprocess.call(['python', 'GenerateAnalysisReport.py', fileInput1, fileInput2, fileInput3, fileInput4, fileInput5, pathOutput])
		#any change to the inputs will require regenerating all reports. 
	except OSError:
		pass

########################
#####     MAIN     #####
########################
usageDescription = ['working Directory: full path to the data working directory']
UtilFunc.checkInputArgs(1, usageDescription)

parentPath = sys.argv[1]

#####     REFERENCE PREP     #####

subPath = os.path.join(parentPath,'0_ReferenceFiles')
UtilFunc.prepareDirectory(subPath)
#TODO: decide if I need to verify that this file exists now, or when functions need to use it
yearbookReferenceFilePath = os.path.join(subPath,'IndexedYearbook.csv')

#####     LIST DATA PREP     #####
###each stage saves its output to it's own output folder, 
###then a messenger function copies over output of one stage to input of the next
### ModulePath is set with supPath2 in the first for-loop below
moduleFunctions = [
		{'ModuleFunction':FixRawList.fixRawList,		'ModuleName':'RawList',		'ModulePath':'', 'OutputExt':'.csv'},
		{'ModuleFunction':IndexList.indexList,			'ModuleName':'IndexList',	'ModulePath':'', 'OutputExt':'.csv'},
		{'ModuleFunction':GenerateReport.generateReport,'ModuleName':'Reporting',	'ModulePath':'', 'OutputExt':'.pdf'}]

subPath = os.path.join(parentPath,'1_ListData')
UtilFunc.prepareDirectory(subPath)
subPath2List = [os.path.join(subPath,sp2) for sp2 in ['0_Raw','1_Index','2_Reporting']]
for index2,subPath2 in enumerate(subPath2List):
	UtilFunc.prepareDirectory(subPath2)
	#index = first character of subdirectory, value is full path of directory
	moduleFunctions[index2]['ModulePath'] = subPath2
	subPath3List = [os.path.join(subPath2,sp3) for sp3 in ['Input','InputComplete','Output','Error']]
	for subPath3 in subPath3List:
		UtilFunc.prepareDirectory(subPath3) #TODO: for simplicity, modify prepareDirectory to make entire directory path if non existant


#####     LIST DATA WORK    #####
### Loop over all module directories
###		Loop over each person
###		Loop over all module directories (explanation below)
### This will seem wonky and redundant, but it allows for single processing of each person
### If there's a file that was corrected and placed in midstream input, it will be processed also
### I believe single processing when possible is best for catching issues
### The outer most loop takes care of files trapped midstream

# rawListing = os.listdir(os.path.join(pathRaw, 'Input'))
### I am relating main module functions and the directories they work in by Alphabet Indecies
for moduleIndex1,mf1 in enumerate(moduleFunctions):
	inputPath = os.path.join(mf1['ModulePath'],'Input')
	fileListing = [os.path.join(inputPath,f) for f in os.listdir(inputPath)]
	# print 'mf1	{}'.format(fileListing)
	for fileName in fileListing:
		# print 'name\t{}]'.format(fileListing)
		#sometimes there are hidden files that break the script
		if fileName.split('/')[-1][0] == '.':
			continue
		name = UtilFunc.parseNameFromFile(fileName)
		number = UtilFunc.parseNumberFromFile(fileName)
		# print '### fileName: {0}'.format(fileName)
		# print '### name: {}, number: {}'.format(name, number)
		#TODO: decide if this should be done as a prep step
		if number == '':
			number = str(getNumberFromNameInFile(name, yearbookReferenceFilePath))
			# print '### Numer: {0}'.format(number)
			fileNameWithNumber = UtilFunc.appendNumberToFileName(fileName,number)
			shutil.copy(fileName,fileNameWithNumber)
			os.remove(fileName)
			fileName = fileNameWithNumber
		# print 'Parsing: name = {0}\t number = {1}'.format(name,number)

		outputFilePathPrevious = ''
		for mf2 in moduleFunctions[moduleIndex1:]:

			inputFilePath = 		'{0}/Input/{1}_Input_{2}_{3}.csv'.format(	mf2['ModulePath'],
																				mf2['ModuleName'],
																				name,
																				number)
			inputCompleteFilePath = '{0}/InputComplete/{1}_Input_{2}_{3}.csv'.format(	mf2['ModulePath'],
																				mf2['ModuleName'],
																				name,
																				number)
			errorFilePath = 		'{0}/Error/{1}_Input_{2}_{3}.csv'.format(	mf2['ModulePath'],
																				mf2['ModuleName'],
																				name,
																				number)
			outputFilePath = 		'{0}/Output/{1}_Output_{2}_{3}{4}'.format(	mf2['ModulePath'],
																				mf2['ModuleName'],
																				name,
																				number,
																				mf2['OutputExt'])
			# print 'mf2\t{}'.format(inputFilePath)
			### copy from stage n-1 output to stage n input																number))
			if outputFilePathPrevious != '':
				shutil.copy(outputFilePathPrevious,inputFilePath)

			func = mf2['ModuleFunction']
			func(	inputFilePath,
					inputCompleteFilePath,
					errorFilePath, 
					yearbookReferenceFilePath,
					outputFilePath)

			outputFilePathPrevious = outputFilePath



#####     ANALYSIS DATA PREP     #####
subPath = '2_Analysis'
pathAnalysis = pathList = UtilFunc.prepareDirectory(os.path.join(parentPath,subPath)) #TODO: what is this about?


subPath = '0_Participation'
pathParticipation = UtilFunc.prepareDirectory(os.path.join(pathAnalysis,subPath))

subPath = '1_PairSingle'
pathPairIndividual = UtilFunc.prepareDirectory(os.path.join(pathAnalysis,subPath))
for subDir in ['Input','Complete','Error']:
	UtilFunc.prepareDirectory(os.path.join(pathAnalysis,subPath, subDir))

subPath = '2_PairAll'
pathPairAll = UtilFunc.prepareDirectory(os.path.join(pathAnalysis,subPath))
for subDir in ['Input','Error','Output']:
	UtilFunc.prepareDirectory(os.path.join(pathAnalysis,subPath, subDir))

subPath = '3_Memorable'
pathMem = UtilFunc.prepareDirectory(os.path.join(pathAnalysis,subPath))

subPath = '4_GroupFormation'
pathGroup = UtilFunc.prepareDirectory(os.path.join(pathAnalysis,subPath))

subPath = '5_SingleMemorySimilarity'
pathIndiSim = UtilFunc.prepareDirectory(os.path.join(pathAnalysis,subPath))

### I do not have enough data to complete this
# subPath = 'LETTER_GroupSimilarity'
# pathGroupSim = prepareDirectories(subPath, path)['resultingPath']

subPath = '6_FinalAnalysisReport'
pathFinalAnalysis = UtilFunc.prepareDirectory(os.path.join(pathAnalysis,subPath))

pathIndex = moduleFunctions[1]['ModulePath']
pathReport = moduleFunctions[2]['ModulePath']

#####     ANALYSIS DATA WORK    #####
calculateParticipation(pathIndex, pathParticipation)
indexOutputListing = os.listdir(os.path.join(pathIndex, 'Output'))
for f in indexOutputListing:
	shutil.copy(os.path.join(pathIndex,'Output',f),os.path.join(pathPairIndividual,'Input'))
pairIndividualListing = os.listdir(os.path.join(pathPairIndividual,'Input'))
for fileInput in pairIndividualListing:
	if(fileInput[0] =='.'):
		continue
	name = UtilFunc.parseNameFromFile(fileInput)
	number = getNumberFromNameInFile(name, yearbookReferenceFilePath)
	getPairDistanceIndividual(name, number, pathPairIndividual, yearbookReferenceFilePath, pathPairAll)

getPairDistanceAll(pathPairAll, yearbookReferenceFilePath, pathPairAll)
findMostMemorable(pathIndex, yearbookReferenceFilePath, pathMem)
buildGroupsFromPairs(pathPairAll, yearbookReferenceFilePath, pathGroup)
#checkIndividualSimilarity()
generateAnalysisReport(pathParticipation, os.path.join(pathPairAll,'Output'), pathMem, pathGroup, pathIndiSim, pathFinalAnalysis)

#create an error folder for each stage in case. Send file there if a test fails
#generate an error report with all files that are left in each folder