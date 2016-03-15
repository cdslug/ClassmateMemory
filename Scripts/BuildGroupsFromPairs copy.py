import os
import sys
import math

def checkInputArgs():
	if len(sys.argv) != 4:
		sys.exit("Error: Incorrect usage. Script requires 3 input arguments.")

def nextOptimalMember(existingMemberIndexes, pairMatrix):
	#There may be a conflict if two have the same score
	maxScore = 0
	tempScore = 0
	newMemberIndex = 0
	for index1 in range(len(pairMatrix)):
		if index1 not in existingMemberIndexes:
			tempScore = 0
			for index2 in existingMemberIndexes:
				tempScore += float(pairMatrix[index1][index2])
			if tempScore > maxScore:
				maxScore = tempScore
				newMemberIndex = index1

	return {"newMemberIndex":newMemberIndex,"newMemberPairScores":maxScore}

def buildGroups(fileInput):

	pairList = []
	
	with open(fileInput, 'r') as fIn:
		for index, line in enumerate(fIn):
			#Skip the heading
			if index > 0:
				(l0,l1,l2,l3,l4,l5,l6) = line.replace("\r","").replace("\n","").split(",")
				pairList.append({"AlphaIndex_1":int(l0),"AlphaIndex_2":int(l1),"PairScore":float(l2),"Last_1":l3,"First_1":l4,"Last_2":l5,"First_2":l6})
	
	classSize = int(math.sqrt(len(pairList))) + 1 #+1 because of ignorning when index = index
	pairMatrix = [[0 for i in range(classSize)] for j in range(classSize)]
	for pair in pairList:
		index1 = pair["AlphaIndex_1"]
		index2 = pair["AlphaIndex_2"]
		pairMatrix[index1][index2] = pair["PairScore"]
		pairMatrix[index2][index1] = pair["PairScore"]

	sortedPairList = sorted(pairList, key=lambda pairs: pairs["PairScore"])[::-1]

	groupNumber = 0
	groupScoreOld = 0;
	groupScoreNew = 0;
	groupData = []
	scoreHistory = [{"Score":0,"AlphaIndex":-1}] #contains dict of score and one member alphIndex

	skipOnEven = 0
	for index1 in range(len(sortedPairList)):
		skipOnEven += 1
		if skipOnEven % 2 == 0:
			continue
		pair = sortedPairList[index1]
		# print(sortedPairList[15])

		#repeating function
		#add first two names
		#go through  afterwards and pair up the AlphaIndex with first and last name
		#todo this, us the reference file which has idexes and names paired up
		groupMemberIndexes = [] #used to record members already in the group
		tempGroupData = []
		groupScoreOld = groupScoreNew = pair["PairScore"]
		tempGroupData.append({"GroupNumber":groupNumber,"GroupScore":groupScoreNew,"AlphaIndex":pair["AlphaIndex_1"]})
		tempGroupData.append({"GroupNumber":groupNumber,"GroupScore":groupScoreNew,"AlphaIndex":pair["AlphaIndex_2"]})
		groupMemberIndexes.append(pair["AlphaIndex_1"])
		groupMemberIndexes.append(pair["AlphaIndex_2"])

		ratioOld = float(0)
		while True:
			newMember = nextOptimalMember(groupMemberIndexes, pairMatrix)
			groupScoreNew = groupScoreOld + newMember["newMemberPairScores"]

			# print(str(newMember) + \
			# 	  "\n" + str(float(groupScoreNew/groupScoreOld)))
			if groupScoreOld < 0.00001:
				break
			ratioNew = float(groupScoreNew/groupScoreOld)
			#if ratioNew > ratioOld: # try with exponents now that the score is updated correctly
			powerFilter = 1.5
			if groupScoreNew / (float(len(groupMemberIndexes) + 1)**powerFilter) > groupScoreOld / (float(len(groupMemberIndexes))**powerFilter) and \
			   len(groupMemberIndexes) < 10:
				ratioOld = ratioNew
				groupScoreOld = groupScoreNew
				groupMemberIndexes.append(newMember["newMemberIndex"])
				tempGroupData.append({"GroupNumber":groupNumber,"GroupScore":groupScoreNew,"AlphaIndex":newMember["newMemberIndex"]})
			else:
				gn = tempGroupData[0]["GroupNumber"]			
				gs = groupScoreOld/(len(tempGroupData)-1) #old becase new was not large enough to pass the test
				if gs > 40 and 107 not in groupMemberIndexes and 12 not in groupMemberIndexes:
					uniqueGroup = False
					if gs in [i["Score"] for i in scoreHistory]:
						uniqueGroup = False
					else:
						scoreHistory.append({"Score":gs,"AlphaIndex":groupMemberIndexes[0]})
						uniqueGroup = True
					if uniqueGroup == True:
						for entry in tempGroupData:
							ai = entry["AlphaIndex"]
							groupData.append({"GroupNumber":gn,"GroupScore":gs,"AlphaIndex":ai})
						groupNumber += 1
						if gn % 1000 == 0:
							print(gn)
				break
		
		

	return groupData

def attachNames(groupData,yearbookNamesFile):

	yearbookNames = []
	with open(yearbookNamesFile, 'r') as fYBN:
		for index, line in enumerate(fYBN):
			#Skip the heading
			if index > 0:
				(l0,l1,l2,l3) = line.replace("\r","").replace("\n","").split(",")
				yearbookNames.append({"AlphaIndex":int(l0),"YearbookLast":l1,"YearbookFirst":l2})

	groupDataWithNames = []
	for groupMember in groupData:
		gn = int(groupMember["GroupNumber"])
		gs = float(groupMember["GroupScore"])
		ai = int(groupMember["AlphaIndex"])
		ln = yearbookNames[ai]["YearbookLast"]
		fn = yearbookNames[ai]["YearbookFirst"]
		entry = {"GroupNumber":gn,"GroupScore":gs,"AlphaIndex":ai,"YearbookLast":ln,"YearbookFirst":fn}
		groupDataWithNames.append(entry)

	return groupDataWithNames

def writeToFile(data, fileOutput):
	with open(fileOutput,'w') as fOut:
		fOut.write("GroupNumber,GroupScore,AlphaIndex,YearbookLast,YearbookFirst\n")
		for entry in data:
			fOut.write( str(entry["GroupNumber"]) + "," + \
				   		str(entry["GroupScore"]) + "," + \
				   		str(entry["AlphaIndex"]) + "," + \
				   		entry["YearbookLast"] + "," + \
				   		entry["YearbookFirst"] + "\n")

########################
#####     MAIN     #####
########################

checkInputArgs()

fileInput = sys.argv[1]
yearbookNamesFile = sys.argv[2]
fileOutput = sys.argv[3]

groupData = buildGroups(fileInput)
groupDataWithNames = attachNames(groupData,yearbookNamesFile)
writeToFile(groupDataWithNames, fileOutput)