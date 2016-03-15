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
import FixRawList.py
import IndexList.py
import GenerateReport.py

def fileLength(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1




def getNumberFromNameInFile(name, yearbookReferenceFilePath):
	yearbookNames = UtilFunc.parseDataFromFile(yearbookReferenceFilePath)
	jaroMatchIndex = UtilFunc.matchName(name, yearbookNames)['AlphaIndex']

	return jaroMatchIndex

def fixRawList(name, number, pathInput, pathOutput):
	fileInput		= os.path.join(pathInput,'Input/RawList_{}_{}.txt'.format(name,number))
	fileComplete	= os.path.join(pathInput,'Complete/RawList_{}_{}.txt'.format(name,number))
	fileError		= os.path.join(pathInput,'Error/RawList_{}_{}.txt'.format(name,number))
	fileOutput		= os.path.join(pathOutput, 'Input/CheckedList_{}_{}.txt'.format(name,number))
	
	print(fileInput)
	try:
		print('FixingRawList')
		subprocess.call(['python', 'FixRawList.py', fileInput, fileOutput])
		print(os.listdir(os.path.join(pathInput, 'Input')))
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
	pathInput 	= os.path.join(pathInput, 'Complete')
	fileOutput 	= os.path.join(pathOutput, 'ParticipationStatistics.csv')
	subprocess.call(['python', 'CalculateParticipationStats.py', pathInput, fileOutput])

def getPairDistanceIndividual(name, number, pathInput, pathResource, pathOutput):
	fileInput		= os.path.join(pathInput, 'Input/IndexedList_{}_{}.csv'.format(name,number))
	fileResource	= os.path.join(pathResource, 'Resource/IndexedYearbook.csv')
	fileComplete	= os.path.join(pathInput, 'Complete/IndexedList_{}_{}.csv'.format(name,number))
	fileError		= os.path.join(pathInput, 'Error/IndexedList_{}_{}.csv'.format(name,number))
	fileOutput		= os.path.join(pathOutput, 'Input/PairScores_{}_{}.csv'.format(name,number))

	try:
		print('getPairDistance_Individual')
		subprocess.call(['python', 'GetPairDistanceIndividual.py', fileInput, fileResource, fileOutput])
		shutil.copyfile(fileInput,fileComplete)
		os.remove(fileInput)
	except OSError:
		pass

def getPairDistanceAll(pathInput,pathResource,pathOutput):
	fileInput 		= os.path.join(pathInput, 'Input')
	fileResource 	= os.path.join(pathResource, 'Resource/IndexedYearbook.csv')
	fileOutput 		= os.path.join(pathOutput, 'Output/PairScores_All.csv')
	try:
		print('getPairDistanceAll')
		subprocess.call(['python', 'GetPairDistanceAll.py', fileInput, fileResource, fileOutput])
	except OSError:
		pass

def findMostMemorable(pathInput,pathResource,pathOutput):
	fileInput 		= os.path.join(pathInput, 'Complete')
	fileResource 	= os.path.join(pathResource, 'Resource/IndexedYearbook.csv')
	fileOutput 		= os.path.join(pathOutput, 'MemorableScores.csv')
	try:
		print('findMostMemorable')
		subprocess.call(['python', 'FindMostMemorable.py', fileInput, fileResource, fileOutput])
	except OSError:
		pass


def buildGroupsFromPairs(pathInput, pathResource, pathOutput):
	fileInput 		= os.path.join(pathInput, 'Output/PairScores_All.csv')
	fileResource 	= os.path.join(pathResource, 'Resource/IndexedYearbook.csv')
	fileOutput 		= os.path.join(pathOutput, 'GroupScores.csv')
	try:
		print('buildGroupsFromPairs')
		subprocess.call(['python', 'BuildGroupsFromPairs2.py', fileInput, fileResource, fileOutput])
	except OSError:
		pass

def checkSingleMemorySimilarity(pathInput, pathResource, pathOutput):
	fileInput 		= os.path.join(pathInput, 'Input')
	fileResource 	= os.path.join(pathResource, 'Resource/IndexedYearbook.csv')
	fileOutput 		= os.path.join(pathOutput, 'IndividualSimilarity.csv')
	try:
		print('buildGroupsFromPairs')
		subprocess.call(['python', 'CheckSingleMemorySimilarity.py', fileInput, fileResource, fileOutput])
	except OSError:
		pass

def checkGroupMemorySimilarity(pathInput1, pathInput2, pathResource, pathOutput):
	fileInput 		= os.path.join(pathInput, 'Output/PairScores_All.csv')
	fileResource 	= os.path.join(pathResource, 'Resource/IndexedYearbook.csv')
	fileOutput 		= os.path.join(pathOutput, 'GroupSimilarity.csv')
	try:
		print('buildGroupsFromPairs')
		subprocess.call(['python', 'CheckGroupSimilarity.py', fileInput1, fileInput2, fileResource, fileOutput])
	except OSError:
		pass

def generateAnalysisReport(pathInput1, pathInput2, pathInput3, pathInput4, pathInput5, pathOutput):
	fileInput1 		= os.path.join(pathInput1, 'ParticipationScores.csv')
	fileInput2 		= os.path.join(pathInput2, 'PairScores.csv')
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
usageDescription = ['working Directory: full path to the data working directory'
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
moduleFunctions = [
		{'ModuleFunction':FixRawList.fixrawList,		'ModuleName':'RawList',		'ModulePath',''},
		{'ModuleFunction':IndexList.indexList,			'ModuleName':'IndexList',	'ModulePath',''},
		{'ModuleFunciton':GenerateReport.GenerateReport,'ModuleName':'Reporting',	'ModulePath',''},
		{'ModuleFunction':(lambda w, x, y, z : None),	'ModuleName':'Report',		'ModulePath',''}]

subPath = os.path.join(parentPath,'1_ListData')
UtilFunc.prepareDirectories(subPath)
subPath2List = [os.path.join(subPath,sp2) for sp2 in ['0_Raw','1_Index','2_Reporting','3_FinalListReport']]
for index2,subPath2 in enumerate(subPath2List):
	UtilFunc.prepareDirectory(subPath2)
	#index = first character of subdirectory, value is full path of directory
	moduleFunctions[index2]['ModulePath'] = subPath2
	subPath3List = [os.path.join(subPath2,sp3) for sp3 in ['Input','InputComplete','Output','Error']]
	for subPath3 in subPath3List:
		UtilFunc.prepareDirectory(subPath3)


#####     LIST DATA WORK    #####
### Loop over all module directories
###		Loop over each person
###		Loop over all module directories (explanation below)
### This will seem wonky and redundant, but it allows for single processing of each person
### If there's a file that was corrected and placed in midstream input, it will be processed also
### I believe single processing when possible is best for catching issues
### The outer most loop takes care of files trapped midstream

rawListing = os.listdir(os.path.join(pathRaw, 'Input'))
### I am relating main module functions and the directories they work in by Alphabet Indecies
for mf1 in moduleFunctions:
	fileListing = os.listdir(os.path.join(mf1['ModulePath'],'Input'))

	for fileName in fileListing:
		#sometimes there are hidden files that break the script
		if fileName[0] == '.':
			continue
		name = UtilFunc.parseNameFromFile(fileName)
		number = UtilFunc.parseNumberFromFile(fileName))
		#TODO: decide if this should be done as a prep step
		if number == '':
			number = getNumberFromNameInFile(name, yearbookReferenceFilePath)
			fileNameWithNumber = UtilFunc.appendNumberToFileName(fileName,number)
			shutil.copy(fileName,fileNameWithNumber)
			os.remove(fileName)
			fileName = fileNameWithNumber
		print 'Parsing: name = {}\t number = {}'.format(name,number)

		outputFilePathPrevious = ''
		for mf2 in moduleFunctions:
			inputFilePath = 		'{}/Input/{}_Input_{}_{}.csv'.format(	mf2['ModulePath'],
																			mf2['ModuleName'],
																			name,
																			number))
			inputCompleteFilePath = '{}/InputComplete/{}_Input_{}_{}.csv'.format(	mf2['ModulePath'],
																			mf2['ModuleName'],
																			name,
																			number))
			errorFilePath = 		'{}/Error/{}_Input_{}_{}.csv'.format(	mf2['ModulePath'],
																			mf2['ModuleName'],
																			name,
																			number))
			outputFilePath = 		'{}/Output/{}_Output_{}_{}.csv'.format(	mf2['ModulePath'],
																			mf2['ModuleName'],
																			name,
																			number))
			### copy from stage n-1 output to stage n input																number))
			if outputFilePathPrevious != '':
				shutil.copy(outputFilePathPrevious,inputFilePath)

			func = mf['ModuleFunction']
			func(	inputFilePath
					inputCompleteFilePath,
					errorFilePath, 
					yearbookReferenceFilePathPath,
					outputFilePath)

			outputFilePathPrevious = outputFilePath



#####     ANALYSIS DATA PREP     #####
subPath = '2_Analysis'
pathAnalysis = pathList = UtilFunc.prepareDirectories(subPath,parentPath)['resultingPath'] #TODO: what is this about?


subPath = 'A_Participation'
pathParticipation = UtilFunc.prepareDirectories(subPath, pathAnalysis)['resultingPath']

subPath = 'B_PairSingle'
pathPairIndividual = UtilFunc.prepareDirectories(subPath, pathAnalysis)['resultingPath']
for subDir in ['Input','Complete','Error']:
	UtilFunc.prepareDirectories(os.path.join(subPath, subDir), pathList)['resultingPath']

subPath = 'C_PairAll'
pathPairAll = UtilFunc.prepareDirectories(subPath, pathAnalysis)['resultingPath']
for subDir in ['Input','Error','Output']:
	UtilFunc.prepareDirectories(os.path.join(subPath, subDir), pathList)['resultingPath']

subPath = 'D_Memorable'
pathMem = UtilFunc.prepareDirectories(subPath, pathAnalysis)['resultingPath']

subPath = 'E_GroupFormation'
pathGroup = UtilFunc.prepareDirectories(subPath, pathAnalysis)['resultingPath']

subPath = 'F_SingleMemorySimilarity'
pathIndiSim = UtilFunc.prepareDirectories(subPath, pathAnalysis)['resultingPath']

### I do not have enough data to complete this
# subPath = 'LETTER_GroupSimilarity'
# pathGroupSim = prepareDirectories(subPath, path)['resultingPath']

subPath = 'G_FinalAnalysisReport'
pathFinalAnalysis = UtilFunc.prepareDirectories(subPath, pathAnalysis)['resultingPath']


#####     ANALYSIS DATA WORK    #####
calculateParticipation(pathReport, pathParticipation)
pairIndividualListing = os.listdir(os.path.join(pathPairIndividual, 'Input'))
for fileInput in pairIndividualListing:
	if(fileInput[0] =='.'):
		continue
	name = UtilFunc.parseNameFromFile(fileInput)
	number = getNumberFromNameInFile(name, yearbookReferenceFilePath)
	getPairDistanceIndividual(name, number, pathPairIndividual, pathIndex, pathPairAll)

getPairDistanceAll(pathPairAll, pathIndex, pathPairAll)
findMostMemorable(pathReport, pathIndex, pathMem)
buildGroupsFromPairs(pathPairAll, pathIndex, pathGroup)
#checkIndividualSimilarity()
generateAnalysisReport(pathParticipation, pathPairAll, pathMem, pathGroup, pathIndiSim, pathFinalAnalysis)

#create an error folder for each stage in case. Send file there if a test fails
#generate an error report with all files that are left in each folder