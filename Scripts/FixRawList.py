#fixRawList.py
import os
import sys
import shutil

import UtilFunc


def fixRawList(inputFilePath, inputCompleteFilePath, outputFilePath, errorFilePath = None, yearbookReferenceFilePath = None, ):

	fileLines = []
	with open(inputFilePath,'r') as fIn:
		fileLines = fIn.readlines()

	names = []
	### step 1) convert all separation characters to ','
	### step 2) split based on ','
	### step 3) strip white space
	with open(outputFilePath,'w') as fOut:
		for l in fileLines:
			lWork = l.replace('\r',',').replace('\n',',').split(',')
			for lw in lWork:
				lw = lw.strip()
				if lw != '':
					names.append(lw)
		for n in names:
			fOut.write('{}\n'.format(n))

	shutil.copy(inputFilePath,inputCompleteFilePath)
	os.remove(inputFilePath)
	return

########################
#####     MAIN     #####
########################
if __name__ == '__main__':
	usageDescription = ["inputFilePath: A full path to a .txt file that contains a list of full names separated by '\\n' or ','",
						'inputCompleteFilePath: ',
						'errorFilePath: ',
						'yearbookReferenceFilePath: A full path to a .csv file containing all expected classmates names along with their alphabetical index, among other details. See full documentation for extensive details',
						'outputFilePath: A full path to a .csv file']

	UtilFunc.checkInputArgs(5,usageDescription)

	inputFilePath = sys.argv[1]
	inputCompleteFilePath = sys.argv[2]
	errorFilePath = sys.argv[3]
	yearbookReferenceFilePath = sys.argv[4]
	outputFilePath = sys.argv[5]

	fixRawList(inputFilePath,inputCompleteFilePath, errorFilePath, yearbookReferenceFilePath,outputFilePath)