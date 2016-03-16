import os
import sys
import math
import random

import UtilFunc

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

	return {'newMemberIndex':newMemberIndex,'newMemberPairScores':maxScore}

def bestGroup(randomMember, groups2Members, members2Groups, pairMatrix):
	meanGroupScoreBest = 0
	bestGroup = -1
	cutoffScore = 0.05
	for pos,group in enumerate(groups2Members):
		if len(group) == 0:
			continue
		meanGroupScore = 0
		for groupMember in group:
			meanGroupScore = meanGroupScore + pairMatrix[randomMember][groupMember]
		meanGroupScore = meanGroupScore / float(len(group))
		#print 'meanGroupScore' + str(meanGroupScore) + ' Best = ' + str(meanGroupScoreBest)
		if meanGroupScore < cutoffScore:
			continue
		elif meanGroupScore > meanGroupScoreBest:
			meanGroupScoreBest = meanGroupScore
			bestGroup = pos
			#print 'bestGroup' + str(bestGroup)

	#print bestGroup
	return bestGroup

def getGroupScore(group, pairMatrix):
	#print group
	score = 0
	for index1 in range(len(group)):
		for index2 in range(len(group)):
			if index2 > index1:
				score += pairMatrix[group[index1]][group[index2]]
				#print pairMatrix[index1][index2]
	return score

def buildGroups(fileInput):

	pairList = UtilFunc.parseDataFromFile(fileInput)
	
	# with open(fileInput, 'r') as fIn:
	# 	for index, line in enumerate(fIn):
	# 		#Skip the heading
	# 		if index > 0:
	# 			(l0,l1,l2,l3,l4,l5,l6) = line.replace('\r','').replace('\n','').split(',')
	# 			pairList.append({	'AlphaIndex_1':int(l0),
	# 								'AlphaIndex_2':int(l1),
	# 								'PairScore':float(l2),
	# 								'Last_1':l3,
	# 								'First_1':l4,
	# 								'Last_2':l5,
	# 								'First_2':l6})

	classSize = int(math.ceil(math.sqrt(len(pairList)))) #fancy because of ignorning when index = index
	pairMatrix = [[0 for i in range(classSize)] for j in range(classSize)]
	for pair in pairList:
		index1 = pair['AlphaIndex_1']
		index2 = pair['AlphaIndex_2']
		pairMatrix[index1][index2] = pair['PairScore']
		pairMatrix[index2][index1] = pair['PairScore']

	sortedPairList = sorted(pairList, key=lambda pairs: pairs['PairScore'])[::-1]

	groupNumber = 0
	groupScoreOld = 0;
	groupScoreNew = 0;
	groupData = []
	scoreHistory = [{'Score':0,'AlphaIndex':-1}] #contains dict of score and one member alphIndex
#0A) Divide classmates into groups of 2
#1) Iterate over people until there are very few members changing
#	It might help to randomly choose members for each iteration, or go back and forth
#	Maybe I should keep track of the classmates that keep jumping back and forth
#2) keep a global list of groups that can change
#	need to figure out how to access/store/change group numbers and members
#3) For a classmate, check to see which group he/she has the strongest average pair score with
#	
#Info 1) keep of a list of groups to members and members to groups


	groupNumber = 0
	initialGroupSize = 1
	groups2Members = [[] for l in range((classSize//initialGroupSize) + 1)] #initialize empty lists
	members2Groups = [[] for l in range(classSize)]

	order = [x for x in range(classSize)]
	random.shuffle(order)
	for pos,randomMember in enumerate(order):
		groups2Members[pos//initialGroupSize].append(randomMember)
		members2Groups[randomMember] = pos//initialGroupSize

	#print 'order: ' + str(order)
	#print 'groups2Members' + str(groups2Members)
	numberGroupChanges = classSize
	n = 0
	print 'ClassSize: {}'.format(classSize)
	# while numberGroupChanges > classSize * 0.01:
	for r in range(len(order)//3): #range was found by observation of data
		numberGroupChanges = 0
		random.shuffle(order)
		groups2MembersTemp = groups2Members
		for randomMember in order:
			bg = bestGroup(randomMember, groups2Members, members2Groups, pairMatrix)
			if bg != members2Groups[randomMember] and bg != -1:
				#print 'OLD'
				groupScoreOld = getGroupScore(groups2Members[bg], pairMatrix)
				#print 'NEW'
				#print groups2Members[bg] + [randomMember]
				groupScoreNew = getGroupScore(groups2Members[bg] + [randomMember], pairMatrix)
				#print 'groupScoreNew' + str(groupScoreNew)

				#print 'old score: ' + str(groupScoreOld) + ', new score: ' + str(groupScoreNew)
			#if ratioNew > ratioOld: # try with exponents now that the score is updated correctly
				powerFilter = 1.5
				if True or groupScoreNew / (float(len(groups2Members[bg]) + 1)**powerFilter) > groupScoreOld / (float(len(groups2Members[bg]))**powerFilter) and \
				   len(groups2Members[bg]) < 50:
					groups2Members[members2Groups[randomMember]].remove(randomMember)
					#if len(groups2Members[members2Groups[randomMember]]) == 0:
						#print '000 Group Shrunk to Zero! 000'
					groups2Members[bg].append(randomMember)
					#print 'Classmate Changed Groups  ' + str(randomMember)
					members2Groups[randomMember] = bg
					numberGroupChanges += 1
		n = n+1
		print 'iteration #{}, numberGroupChanges: {}'.format(n,numberGroupChanges)

	#print 'groups2Members' + str(groups2Members)

	for memberNumber,groupNumber in enumerate(members2Groups):
		groupScore = groups2Members[groupNumber]
		groupData.append({	'GroupNumber':groupNumber,
							'GroupScore':getGroupScore(groupScore,pairMatrix),
							'AlphaIndex':memberNumber})
	return sorted(groupData, key=lambda gd: gd['GroupNumber'])


def attachNames(groupData,yearbookNamesFile):

	yearbookNames = UtilFunc.parseDataFromFile(yearbookNamesFile)

	groupDataWithNames = []
	for groupMember in groupData:
		gn = int(groupMember['GroupNumber'])
		gs = float(groupMember['GroupScore'])
		ai = int(groupMember['AlphaIndex'])
		ln = yearbookNames[ai]['YearbookLast']
		fn = yearbookNames[ai]['YearbookFirst']
		entry = {	'GroupNumber':gn,
					'GroupScore':gs,
					'AlphaIndex':ai,
					'YearbookLast':ln,
					'YearbookFirst':fn}
		groupDataWithNames.append(entry)

	return groupDataWithNames

def writeToFile(data, fileOutput):
	with open(fileOutput,'w') as fOut:
		fOut.write('GroupNumber,GroupScore,AlphaIndex,YearbookLast,YearbookFirst\n')
		for entry in data:
			fOut.write('{},{},{},{},{}\n'.format(	entry['GroupNumber'],
				   								entry['GroupScore'],
				   								entry['AlphaIndex'],
				   								entry['YearbookLast'],
				   								entry['YearbookFirst']))

########################
#####     MAIN     #####
########################
usageDescription = ['fileInput: A full path to a .csv file containing nXn pair scores',
					'yearbookNamesFile: A full path to a .csv file containing all expected classmates names along with their alphabetical index, among other details. See full documentation for extensive details',
					'fileOutput: A full path to a .csv file']
UtilFunc.checkInputArgs(3)

fileInput = sys.argv[1]
yearbookNamesFile = sys.argv[2]
fileOutput = sys.argv[3]

groupData = buildGroups(fileInput)
groupDataWithNames = attachNames(groupData,yearbookNamesFile)
writeToFile(groupDataWithNames, fileOutput)