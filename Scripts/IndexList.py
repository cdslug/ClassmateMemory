import os
import sys
import shutil

import UtilFunc




def indexList(inputFilePath, inputCompleteFilePath, errorFilePath, yearbookReferenceFilePath, outputFilePath):

	names = []
	#list of dictionaries
	yearbookNames = UtilFunc.parseDataFromFile(yearbookReferenceFilePath)

	#list of dicitonaries
	namesOutput = []

	with open(inputFilePath, 'r') as fWN:
		for writtenIndex, line in enumerate(fWN):
			#could have been simpler, but sometimes last names are not included
			#may have to worry about only last name. Spell checker will reject that
			# lineSplit = line.replace('\n','').split(None,1)[::-1]
			lineSplit = line.replace('\n','').split(None,1)
			l0 = lineSplit[0]
			l1 = ''
			if len(lineSplit) > 1:
				l1 = lineSplit[1]
			else:
				l1 = '_'
			names.append({	'WrittenIndex':str(writtenIndex),
							'WrittenFirst':l0,
							'WrittenLast':l1})

	# with open(yearbookNamesFile, 'r') as fYBN:
	# 	for index, line in enumerate(fYBN):
	# 		#Skip the heading
	# 		if index > 0:
	# 			(l0,l1,l2,l3) = line.replace('\r','').replace('\n','').split(',')
	# 			yearbookNames.append({	'AlphaIndex':l0,
	# 									'YearbookLast':l1,
	# 									'YearbookFirst':l2,
	# 									'GraduatedLLA09':l3})


	namesOutput = []
	for name in names:
		jaroMatch = UtilFunc.matchName(name, yearbookNames)
		namesOutput.append(jaroMatch)

	# for n in namesOutput: #debugging
	# 	print(str(n) + '\n')

	#append missing names
	for ybn in yearbookNames:
		if ybn['AlphaIndex'] not in [no['AlphaIndex'] for no in namesOutput]:
			temp = ybn.copy()
			temp.update({	'WrittenIndex':'-',
							'WrittenLast':'',
							'WrittenFirst':'', 
							'Spelling':str(0)})
			namesOutput.append(temp)

	with open(outputFilePath,'w') as fOut:
		fOut.write('AlphaIndex,WrittenIndex,WrittenLast,WrittenFirst,YearbookLast,YearbookFirst,Spelling,GraduatedLLA09\n')
		for no in namesOutput:
			fOut.write('{},{},{},{},{},{},{},{}\n'.format(	no['AlphaIndex'],
				   											no['WrittenIndex'],
				   											no['WrittenLast'],
				   											no['WrittenFirst'],
				   											no['YearbookLast'],
				   											no['YearbookFirst'],
				   											no['Spelling'],
				   											no['GraduatedLLA09']))

	shutil.copy(inputFilePath,inputCompleteFilePath)
	os.remove(inputFilePath)
	return
########################
#####     MAIN     #####
########################
if __name__ == '__main__':
	usageDescription = ["inputFilePath: A full path to a .txt file that contains a list of full names separated by '\\n'",
						'inputCompleteFilePath: ',
						'errorFilePath: ',
						'yearbookReferenceFilePath: A full path to a .csv file containing all expected classmates names along with their alphabetical index, among other details. See full documentation for extensive details',
						'outputFilePath: A full path to a .csv file containing all names, both those included in the input file and those forgotten. They are indexed alphabetically and by input file ordering']

	UtilFunc.checkInputArgs(5,usageDescription)

	inputFilePath = sys.argv[1]
	inputCompleteFilePath = sys.argv[2]
	errorFilePath = sys.argv[3]
	yearbookReferenceFilePath = sys.argv[4]
	outputFilePath = sys.argv[5]

	indexList(inputFilePath,inputCompleteFilePath, errorFilePath, yearbookReferenceFilePath,outputFilePath)