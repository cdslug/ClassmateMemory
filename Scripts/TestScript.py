import os
import sys
import unittest

import UtilFunc

import FixRawList
import IndexList
# import GenerateReport

# import CalculateParticipationStats
# import GetPairDistanceIndividual
# import GetPairDistanceAll
# import FindMostMemorable
# import BuildGroupsFromPairs2
# import CheckSingleMemorySimilarity

def printLargeTitle(title):
	titleLength = len(title)
	print '#' * (20 + 8 + titleLength)
	print '#####     Testing {}     #####'.format(title)
	print '#' * (20 + 8 + titleLength) + '\n'

def printSmallTitle(title):
	print '###   {}   ###\n'.format(title)


class UtilFuncTest(unittest.TestCase):

	def setUp(self):
		UtilFunc.prepareDirectory(os.path.join(sys.path[0],'TestFiles/UtilFunc'))
		
		self.refData = UtilFunc.parseDataFromFile('/Users/cdslug/Dropbox/Projects/Tech/Programming/Remembered Classmates/ReportingWork refactored/0_ReferenceFiles/IndexedYearbook.csv')
		###TODO: prepare test files
     
	# ending the test
	def tearDown(self):
		###TODO: delete test files so outdated files cannot accidentally be used.
		###			do not need to delete output files
		x = 1
	# test checkInputArgs_01
	#@unittest2.skip("classmateTest:test_A:skipped")
	def test_checkInputArgs_01(self):
		self.assertIsNone(UtilFunc.checkInputArgs(len(sys.argv)-1,['Failed if showing']))
     
    # test fileLength
	def test_fileLength_01(self):
		###TODO: determine if ending a file with '\n' means the blank line counts towards the file length
		self.assertEqual( UtilFunc.fileLength(os.path.join(sys.path[0],'TestFiles/UtilFunc/fileLength1.txt')) , 5 )

	def test_fileLength_02(self):
		self.assertEqual( UtilFunc.fileLength(os.path.join(sys.path[0],'TestFiles/UtilFunc/fileLength2.txt')) , 0 )
	
	def test_fileLength_03(self):
		self.assertEqual( UtilFunc.fileLength(os.path.join(sys.path[0],'TestFiles/UtilFunc/fileLength3.txt')) , 1 )
	
	def test_fileLength_04(self):
		self.assertEqual( UtilFunc.fileLength(os.path.join(sys.path[0],'TestFiles/UtilFunc/fileLength4.txt')) , 2 )


	def test_parseNameFromFile_01(self):
 		self.assertEqual( UtilFunc.parseNameFromFile('parentPath/Word_Input_LastFirst_3.py') , 'LastFirst' )
	
	def test_parseNameFromFile_02(self):
		self.assertEqual( UtilFunc.parseNameFromFile('parentPath/Word_Input_LastFirst_03.py') , 'LastFirst' )
	
	def test_parseNameFromFile_03(self):
		self.assertEqual( UtilFunc.parseNameFromFile('parentPath/Word_Input_LastFirst.py') , 'LastFirst' )

	def test_parseNumberFromFile_01(self):
		self.assertEqual( UtilFunc.parseNumberFromFile('parentPath/Word_Input_LastFirst_3.py') , '3' )
	
	def test_parseNumberFromFile_02(self):
		self.assertEqual( UtilFunc.parseNumberFromFile('parentPath/Word_Input_LastFirst.py') , '' )
	
	def test_parseNumberFromFile_03(self):
		self.assertEqual( UtilFunc.parseNumberFromFile('parentPath/Word_Input_LastFirst_-3.py') , '' )


	def test_appendNumberToFileName_01(self):
		self.assertEqual( UtilFunc.appendNumberToFileName('parentPath/Word_Input_LastFirst.py','3') , 'parentPath/Word_Input_LastFirst_3.py' )
	
	def test_appendNumberToFileName_02(self):
		self.assertEqual( UtilFunc.appendNumberToFileName('parentPath/Word_Input_LastFirst.py','3') , 'parentPath/Word_Input_LastFirst_3.py' )
	
	# @unittest.skip('UtilFuncTest:test_appendNumberToFileName_03')
	def test_appendNumberToFileName_03(self):
		self.skipTest('Decide if needed')
		self.assertEqual( UtilFunc.appendNumberToFileName('parentPath/Word_Input_LastFirst.py','-3') , 'parentPath/Word_Input_LastFirst_3.py' )
	
	def test_appendNumberToFileName_04(self):
		self.skipTest('Decide if needed')
		self.assertEqual( UtilFunc.appendNumberToFileName('parentPath/Word_Input_LastFirst.py',3) , 'parentPath/Word_Input_LastFirst_3.py' )


	def test_interpretString_01(self):
		self.assertEqual( UtilFunc.interpretString(''),'')
	
	def test_interpretString_02(self):
		self.assertEqual( UtilFunc.interpretString('1'),1)
	
	def test_interpretString_03(self):
		self.assertEqual( UtilFunc.interpretString('1.0'),1.0)
	
	def test_interpretString_04(self):
		self.assertEqual( UtilFunc.interpretString('1one'),'1one')


	def test_parseDataFromFile_01(self):
		expectedResult = [{'one':1,'two':2,'three':3},{'one':4.0,'two':5.0,'three':6.0}]
		inputFile = os.path.join(sys.path[0],'TestFiles/UtilFunc/parseDataFromFile1.txt')
		self.assertEqual( UtilFunc.parseDataFromFile(inputFile) , expectedResult )


	def test_prepareDirectory_01(self):
		testPath = os.path.join(sys.path[0],'TestFiles/UtilFunc/DummyDir1')
		UtilFunc.prepareDirectory(testPath)
		self.assertEqual( os.path.exists(testPath), True )

	# self.refData = UtilFunc.parseDataFromFile('/Users/cdslug/Dropbox/Projects/Tech/Programming/Remembered Classmates/ReportingWork refactored/0_ReferenceFiles/IndexedYearbook.csv')
	
	def test_matchName_01(self):
		name = [{'WrittenLast':'Mercer','WrittenFirst':'Ryan'},['Mercer','Ryan'],0]
		returnValue = UtilFunc.matchName(name[0],self.refData,name[2])
		self.assertEqual([returnValue['YearbookLast'],returnValue['YearbookFirst']],name[1])

	def test_matchName_02(self):
		name = [{'WrittenLast':'Mercei','WrittenFirst':'Rian'},['Mercer','Ryan'],0]
		returnValue = UtilFunc.matchName(name[0],self.refData,name[2])
		self.assertEqual([returnValue['YearbookLast'],returnValue['YearbookFirst']],name[1])

	def test_matchName_03(self):
		name = [{'WrittenLast':'MERCER','WrittenFirst':'RYAN'},['Mercer','Ryan'],0]
		returnValue = UtilFunc.matchName(name[0],self.refData,name[2])
		self.assertEqual([returnValue['YearbookLast'],returnValue['YearbookFirst']],name[1])

	def test_matchName_04(self):
		name = [{'WrittenLast':'MercerRyan','WrittenFirst':''},['Mercer','Ryan'],0]
		returnValue = UtilFunc.matchName(name[0],self.refData,name[2])
		self.assertEqual([returnValue['YearbookLast'],returnValue['YearbookFirst']],name[1])

	def test_matchName_05(self):
		name = [{'WrittenLast':'Scott Lunsford','WrittenFirst':'Erik'},['Lunsford','Erik-Scott'],0]
		returnValue = UtilFunc.matchName(name[0],self.refData,name[2])
		self.assertEqual([returnValue['YearbookLast'],returnValue['YearbookFirst']],name[1])

	def test_matchName_06(self):
		name = [{'WrittenLast':'Lunsford','WrittenFirst':'Erik-Scott'},['Lunsford','Erik-Scott'],0]
		returnValue = UtilFunc.matchName(name[0],self.refData,name[2])
		self.assertEqual([returnValue['YearbookLast'],returnValue['YearbookFirst']],name[1])

	def test_matchName_07(self):
		name = [{'WrittenLast':'Min','WrittenFirst':'Twins'},['Min','Nicolas'],None]
		returnValue = UtilFunc.matchName(name[0],self.refData,name[2])
		self.assertEqual([returnValue['YearbookLast'],returnValue['YearbookFirst']],name[1])


class RawListTest(unittest.TestCase):
	def setUp(self):
		UtilFunc.prepareDirectory(os.path.join(sys.path[0],'TestFiles/FixRawList'))
		UtilFunc.prepareDirectory(os.path.join(sys.path[0],'TestFiles/FixRawList/Input'))
		UtilFunc.prepareDirectory(os.path.join(sys.path[0],'TestFiles/FixRawList/InputComplete'))
		UtilFunc.prepareDirectory(os.path.join(sys.path[0],'TestFiles/FixRawList/Output'))

		self.inputFile = 		os.path.join(sys.path[0],'TestFiles/FixRawList/Input/fixRawList1_Input_MercerRyan_14.txt')
		self.inputCompleteFile = os.path.join(sys.path[0],'TestFiles/FixRawList/InputComplete/fixRawList1_Input_MercerRyan_14.txt')
		self.outputFile = 		os.path.join(sys.path[0],'TestFiles/FixRawList/Output/fixRawList1_Output_MercerRyan_14.txt')

		self.names = ['Ryan Mercer','Erik Scott Lunsford','Andrew Muinos','Yuki Chavez','Charles Eaton','Kunal Shah','Eric Crawford','Matthew MacDonald','Lisa']
		with open(self.inputFile, 'w') as f:
			###name1 is normal with a '\n' after
			###name2 has 3 parts
			###name3 has a ','
			###name4 has a ',' and '\n' after
			###name5 has a ',' (preparing for next)
			###name6 has a ' ' before and ',\n ' after
			###name7 is part of testing name6
			###name7-8 is blank
			###name8 has a '\r' after
			###name9 has only 1 part
			f.write('{}\n{}\n{},{},\n{}, {},\n {},\'\',{}\r{}'.format(	self.names[0],
																		self.names[1],
																		self.names[2],
																		self.names[3],
																		self.names[4],
																		self.names[5],
																		self.names[6],
																		self.names[7],
																		self.names[8]))
			FixRawList.fixRawList(self.inputFile,self.inputCompleteFile,self.outputFile)

	# def tearDown(self):



	def test_setUp_01(self):
		print self.twat
		self.assertFalse( os.path.exists(self.inputFile))
	
	def test_setUp_02(self):
		self.assertTrue( os.path.exists(self.inputCompleteFile))
	
	def test_setUp_03(self):
		self.assertTrue( os.path.exists(self.outputFile))
	
	def test_fixRawList_01(self):
		with open(self.outputFile,'r') as f:
			lines = [l.strip() for l in f.readlines()]
			# self.assertListEqual(lines,self.names)
			# self.assertEqual( lines[0] , names[0] )
			# self.assertEqual( lines[1] , names[1] )
			# self.assertEqual( lines[2] , names[2] )
			# self.assertEqual( lines[3] , names[3] )
			# self.assertEqual( lines[4] , names[4] )
			# self.assertEqual( lines[5] , names[5] )
			# self.assertEqual( lines[6] , names[6] )
			# self.assertEqual( lines[7] , names[7] )
			# self.assertEqual( lines[8] , names[8] )

# class IndexListTest(unittest.TestCase):
# 	def setUp(self):
# 		UtilFunc.prepareDirectory(os.path.join(sys.path[0],'TestFiles/IndexList'))

# 	def tearDown(self):



# class GenerateReportTest(unittest.TestCase):
# 	def setUp(self):

# 	def tearDown(self):


# class CalculateParticipationStatsTest(unittest.TestCase):


# class GetPairDistanceIndividualTest(unittest.TestCase):
# 	def setUp(self):

# 	def tearDown(self):

# class GetPairDistanceAllTest(unittest.TestCase):
# 	def setUp(self):

# 	def tearDown(self):

# class FindMostMemorableTest(unittest.TestCase):
# 	def setUp(self):

# 	def tearDown(self):

# class BuildGroupsFromPairs2Test(unittest.TestCase):
# 	def setUp(self):

# 	def tearDown(self):

# class CheckSingleMemorySimilarityTest(unittest.TestCase):
# 	def setUp(self):

# 	def tearDown(self):

#runs all tests
def testScript():
	testedModules = {	'UtilFunc':testUtilFunc,
						'FixRawList':testRawList,
						'IndexList':testIndexList,
						'GenerateReport':testGenerateReport,
						'CalculateParticipationStats':testCalculateParticipationStats,
						'GetPairDistanceIndividual':testGetPairDistanceIndividual,
						'GetPairDistanceAll':testGetPairDistanceAll,
						'FindMostMemorable':testFindMostMemorable,
						'BuildGroupsFromPairs2':testBuildGroupsFromPairs2,
						'CheckSingleMemorySimilarity':testCheckSingleMemorySimilarity
					}
	selectedModules = sys.argv[1:]
	#test all if no modules listed
	if selectedModules == []:
		selectedModules = testedModules

	failCount = 0
	for modulePath in selectedModules:
		moduleSplit = modulePath.replace('/','.').split('.')
		moduleName = moduleSplit[-2] if moduleSplit[-1] == 'py' else moduleSplit[-1]

		if moduleName in testedModules:
			#run the test function attached to the dicitonary
			failCount += testedModules[moduleName]()
		else:
			print 'ERROR: module \'{}\' not found. Use one of the following {}'.format(moduleName,testedModules.keys())

	if failCount == 0:
		printLargeTitle('Complete: All Tests Passed!')
	else:
		printLargeTitle('Complete: {} Failed Test{} :('.format(failCount,'s' if failCount != 1 else ''))

if __name__ == '__main__':
	testList = [UtilFuncTest,
				RawListTest#,
				# IndexListTest,
				# GenerateReportTest,
				# CalculateParticipationStatsTest,
				# GetPairDistanceIndividualTest,
				# GetPairDistanceAllTest,
				# FindMostMemorableTest,
				# BuildGroupsFromPairs2Test,
				# CheckSingleMemorySimilarityTest
				]
	testLoad = unittest.TestLoader()
	# classmateSuite = unittest.TestSuite()
	caseList = []
	for testCase in testList:
		testSuite = testLoad.loadTestsFromTestCase(testCase)
		caseList.append(testSuite)
	classmateSuite = unittest.TestSuite(caseList)

	classmateRunner = unittest.TextTestRunner(verbosity=2)
	classmateResult = classmateRunner.run(classmateSuite)

	print
	print "---- START OF TEST RESULTS"
	print classmateResult
	print
	print "classmateResult::errors"
	print classmateResult.errors
	print
	print "classmateResult::failures"
	print classmateResult.failures
	print
	print "classmateResult::skipped"
	print classmateResult.skipped
	print
	print "classmateResult::successful"
	print classmateResult.wasSuccessful()
	print
	print "classmateResult::test-run"
	print classmateResult.testsRun
	print "---- END OF TEST RESULTS"
	print
	# testScript()