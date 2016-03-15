import os
import sys
import math
import random

def checkInputArgs():
	numInputs = 4
	if len(sys.argv) != numInputs + 1:
		sys.exit("Error: Incorrect usage. Script requires " + str(numInputs) + " input arguments.")

#1	Iterate over each person's pairScore file.
#	Check every other person to see who they are most similar to.
#	Similarity should be both raw order and pairScores
#		This requires the Indexed lists and the pairScores files

def fileLength(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def parseNumberFromFileName(fileName):
	sections = fileName.replace("_",".").split(".")
	print(sections)
	if(len(sections) != 4):
		return ""
	else:
		return sections[2]

def loadIndexedFile(fileInput, classSize):
	alpha2Written = [0 for i in range(classSize)]
	with open(fileInput, 'r') as pIn:
		for index, line in enumerate(pIn):
			#Skip the heading
			if index > 0:
				(l0,l1,l2,l3,l4,l5,l6,l7) = line.replace("\r","").replace("\n","").split(",")
				#print "l0 = " + l0 + "\tl1 = " + l1
				if l1 == "-":
					alpha2Written[int(l0)] = -1
				elif l0 == "VERIFY":
					continue
				else:
					alpha2Written[int(l0)] = int(l1)

	return alpha2Written




def getOrderSimilarity(pathInput, yearbookNamesFile):
	#This function finds similarity scores of the order a list of names was written
	#Iterate though all indexed files
	#
	classSizeConst = 184;  #need to make more general
	classSize = fileLength(yearbookNamesFile) - 1 # -1 for headers
	if classSizeConst != classSize:
		print "\n\n\n"
		print "WARNING WARNING: Class Size is " + str(classSize) + " which is not 184!!!! *****"
		print "WARNING WARNING: Class Size is " + str(classSize) + " which is not 184!!!! *****"
		print "WARNING WARNING: Class Size is " + str(classSize) + " which is not 184!!!! *****"
		print "\n\n\n"

	fileList = []
	indexedListing = os.listdir(pathInput)
	for fileInput in indexedListing:
		if(fileInput[0] =="."):
			continue
		fileList.append(fileInput)

	orderSimilarityScores = [[0 for i in range(classSize)] for j in range(classSize)]
	for fileIndex1 in range(len(fileList)):
		alphaIndex1 = int(parseNumberFromFileName(fileList[fileIndex1]))
		#print "111111- alpha index 1: " + str(alphaIndex1) + " -111111"
		alpha2Written1 = loadIndexedFile(pathInput + "/" + fileList[fileIndex1], classSize)

		for fileIndex2 in range(len(fileList)):
			if fileIndex2 > fileIndex1:
				alphaIndex2 = int(parseNumberFromFileName(fileList[fileIndex2]))
				#print "2222222- alpha index 1: " + str(alphaIndex1) + " -222222"
				alpha2Written2 = loadIndexedFile(pathInput + "/" + fileList[fileIndex2], classSize)

				if len(alpha2Written1) != len(alpha2Written2):
					print "WARNING WARNING WARNING, Indexed Files have different length"
					print "Line Length: " + str(len(alpha2Written1)) + "\t" + fileList[fileIndex1]
					print "Line Length: " + str(len(alpha2Written2)) + "\t" + fileList[fileIndex2]
				for index in range(len(alpha2Written1)):
					#skip people who were forgotten
					if alpha2Written1[index] == -1 or alpha2Written2[index] == -1:
						continue
					orderSimilarityScores[alphaIndex1][alphaIndex2] += 1/float( 1 + abs(alpha2Written1[index] - alpha2Written2[index]))
					#duplication for ease of access
					orderSimilarityScores[alphaIndex2][alphaIndex1] += 1/float(1 + abs(alpha2Written1[index] - alpha2Written2[index]))
	return orderSimilarityScores

def loadPairScoresFile(fileInput, classSize):
	pairScores = [[0 for i in range(classSize)] for j in range(classSize)]
	with open(fileInput, 'r') as pIn:
		for index, line in enumerate(pIn):
			#Skip the heading
			if index > 0:
				(l0,l1,l2,l3,l4,l5,l6) = line.replace("\r","").replace("\n","").split(",")
				#print "l0 = " + l0 + "\tl1 = " + l1
				pairScores[int(l0)][int(l1)] = float(l2)

	return pairScores

def getPairSimilarity(pathInput, yearbookNamesFile):
	#This function finds similarity scores of the pair score list of names was written
	#Iterate though all pair score files
	#
	classSizeConst = 184;  #need to make more general
	classSize = fileLength(yearbookNamesFile) - 1 # -1 for headers
	if classSizeConst != classSize:
		print "\n\n\n"
		print "WARNING WARNING: Class Size is " + str(classSize) + " which is not 184!!!! *****"
		print "WARNING WARNING: Class Size is " + str(classSize) + " which is not 184!!!! *****"
		print "WARNING WARNING: Class Size is " + str(classSize) + " which is not 184!!!! *****"
		print "\n\n\n"

	fileList = []
	indexedListing = os.listdir(pathInput)
	for fileInput in indexedListing:
		if(fileInput[0] =="."):
			continue
		fileList.append(fileInput)

	pairSimilarityScores = [[0 for i in range(classSize)] for j in range(classSize)]
	for fileIndex1 in range(len(fileList)):
		alphaIndex1 = int(parseNumberFromFileName(fileList[fileIndex1]))
		#print "111111- alpha index 1: " + str(alphaIndex1) + " -111111"
		pairScores1 = loadPairScoresFile(pathInput + "/" + fileList[fileIndex1], classSize)

		for fileIndex2 in range(len(fileList)):
			if fileIndex2 > fileIndex1:
				alphaIndex2 = int(parseNumberFromFileName(fileList[fileIndex2]))
				#print "2222222- alpha index 1: " + str(alphaIndex1) + " -222222"
				pairScores2 = loadPairScoresFile(pathInput + "/" + fileList[fileIndex2], classSize)

				if len(pairScores1) != len(pairScores2):
					print "WARNING WARNING WARNING, Indexed Files have different length"
					print "Line Length: " + str(len(alpha2Written1)) + "\t" + fileList[fileIndex1]
					print "Line Length: " + str(len(alpha2Written2)) + "\t" + fileList[fileIndex2]

				pairScoreCount = 0
				for index1 in range(len(pairScores1)):
					#skip people who were forgotten
					for index2 in range(len(pairScores2)):
						if index2 > index1:
							if pairScores1[index1][index2] != 0 and pairScores2[index1][index2] != 0:
								pairSimilarityScores[alphaIndex1][alphaIndex2] += 1/float( 1 + abs(pairScores1[index1][index2] - pairScores2[index1][index2]))
								#duplication for ease of access
								pairSimilarityScores[alphaIndex2][alphaIndex1] += 1/float(1 + abs(pairScores1[index1][index2] - pairScores2[index1][index2]))
								pairScoreCount += 1
								#TODO need to normalize the scores somehow. They favor the person who remembered the most
				#normalizing the similarity score so people who remembered more are not given an advantage.
				pairSimilarityScores[alphaIndex1][alphaIndex2] /= pairScoreCount
				#duplication for ease of access
				pairSimilarityScores[alphaIndex2][alphaIndex1] /= pairScoreCount
	return pairSimilarityScores
	

def writeToFile(orderScorePairValues, pairScorePairValues, yearbookNamesFile, fileOutput):

	#list of dictionaries
	yearbookNames = []

	with open(yearbookNamesFile, 'r') as fYBN:
		for index, line in enumerate(fYBN):
			#Skip the heading
			if index > 0:
				(l0,l1,l2,l3) = line.replace("\r","").replace("\n","").split(",")
				yearbookNames.append({"AlphaIndex":l0,"YearbookLast":l1,"YearbookFirst":l2})

	with open(fileOutput,'w') as fOut:
		fOut.write("AlphaIndex_1,AlphaIndex_2,OrderScore,PairScore,Last_1,First_1,Last_2,First_2\n")
		for index1, entry1 in enumerate(yearbookNames):
			for index2, entry2 in enumerate(yearbookNames):
				if index1 != index2:
					dim1 = int(entry1["AlphaIndex"])
					dim2 = int(entry2["AlphaIndex"])

					#TODO rename
					fOut.write( str(dim1) + "," + \
						   		str(dim2) + "," + \
						   		str(orderScorePairValues[dim1][dim2]) + "," + \
						   		str(pairScorePairValues[dim1][dim2]) + "," + \
						   		entry1["YearbookLast"] + "," + \
						   		entry1["YearbookFirst"] + "," + \
						   		entry2["YearbookLast"] + "," + \
						   		entry2["YearbookFirst"] + "\n")
########################
#####     MAIN     #####
########################

checkInputArgs()

pathInputIndexed = sys.argv[1]
pathInputPairs = sys.argv[2]
yearbookNamesFile = sys.argv[3]
fileOutput = sys.argv[4]

orderSimilarityScores = getOrderSimilarity(pathInputIndexed, yearbookNamesFile)
pairSimilarityScores = getPairSimilarity(pathInputPairs, yearbookNamesFile)
#groupDataWithNames = attachNames(groupData,yearbookNamesFile)
writeToFile(orderSimilarityScores, pairSimilarityScores, yearbookNamesFile, fileOutput)