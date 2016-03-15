#PDF Report
#read all file names in a directory of indexed lists without reports
#for each file name
#	open a new files using name and number in the new file name
#	filter to get unique 09 names remembered. Use alphabetical number
#	filter to get 09 names forgotten.
#	filter to get unique non-09 remembered.
#	filter to get non-09 forgotten
#	
#	Format the list. Follow the pages doc as a reference
#		count # of each of the 4 categories
#		print names from each category
#	save file
#move file that was just read to a completed folder.

#Sources
# http://www.hoboes.com/Mimsy/hacks/multiple-column-pdf/
# http://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/
# https://github.com/mattjmorrison/ReportLab/blob/master/src/reportlab/graphics/charts/legends.py
# http://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/

import os
import sys

import UtilFunc
# from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, NextPageTemplate, PageBreak, PageTemplate
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
from reportlab.rl_config import defaultPageSize

#for pi chart
from reportlab.lib.pagesizes import cm, inch
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from reportlab.lib.colors import Color, PCMYKColor
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin


class MyDrawing(_DrawingEditorMixin,Drawing):
    def __init__(self,width=300,height=150,*args,**kw):
        apply(Drawing.__init__,(self,width,height)+args,kw)
        self._add(self,Pie(),name='chart',validate=None,desc=None)
        self.chart.x                    = 275
        self.chart.y                    = (self.height-self.chart.height)-26
        self.chart.slices.strokeWidth   = 0.5
        self.chart.slices.popout        = 1
        self.chart.direction            = 'clockwise'
        self.chart.height               = 150
        self.chart.width                = self.chart.height
        self.chart.startAngle           = -90
        self.chart.slices[0].popout     = 10
        self._add(self,Legend(),name='legend',validate=None,desc=None)
        self.legend.x                   = 0
        self.legend.y                   = 107
        self.legend.columnMaximum       = 4
        self.legend.boxAnchor           = 'nw'
        self.legend.subCols[1].align    = 'left'
        self.legend.strokeWidth         = 0
        self.legend.fontName            = 'Helvetica'
        self.legend.alignment           = 'right'   
        # these data can be read from external sources
        data                = [9, 7, 6, 4]
        categories          = ['A','B','C','D']
        colors              = [PCMYKColor(0,31,88,4), \
        					   PCMYKColor(0,10,88,4), \
        					   PCMYKColor(88,45,0,4), \
        					   PCMYKColor(88,0,66,4)]
#        colors              = [PCMYKColor(0,0,0,x) for x in (100,66,33,5)]
        self.chart.data     = data
        self.chart.labels   = map(str, self.chart.data)
        self.legend.colorNamePairs = zip(colors, categories)
        for i, color in enumerate(colors): self.chart.slices[i].fillColor  = color

    def setNewData(self,newData):
        data = [n[0] for n in newData]
        categories = [n[1] for n in newData]
        colors              = [PCMYKColor(0,31,88,4), \
        					   PCMYKColor(0,10,88,4), \
        					   PCMYKColor(88,45,0,0), \
        					   PCMYKColor(88,0,66,0)]
        self.chart.data     = data
        self.chart.labels   = map(str, self.chart.data)
        self.legend.colorNamePairs = zip(colors, categories)
        for i, color in enumerate(colors): self.chart.slices[i].fillColor  = color


def foot1(canvas,doc):
	canvas.saveState()
	canvas.setFont('Times-Roman',19)
	canvas.drawString(inch, 0.75 * inch, 'Page %d' % doc.page)
	canvas.restoreState()
def foot2(canvas,doc):
	canvas.saveState()
	canvas.setFont('Times-Roman',9)
	canvas.drawString(inch, 0.75 * inch, 'Page %d' % doc.page)
	canvas.restoreState()

def textStyle(txt, Elements, style, sep, klass=Paragraph):
	s = Spacer(0.2*inch, sep*inch)
	Elements.append(s)
	para = klass(txt, style)
	Elements.append(para)

def constructSingleColumnParagraphs(stringList):
	Elements = []

	styles = getSampleStyleSheet()
	
	HeaderStyle = styles['Heading1']
	ParaStyle = styles['Normal']
	PreStyle = styles['Code']

	Elements=[]

	Elements.append(NextPageTemplate('OneCol'))
	#Elements.append(PageBreak())

	for s in stringList:
		textStyle(s, Elements, style=ParaStyle, sep=0.1)

	return Elements

def writeIntro():
	Elements = []

	styles = getSampleStyleSheet()
	
	HeaderStyle = styles['Heading1']
	ParaStyle = styles['Normal']
	PreStyle = styles['Code']

	Elements=[]

	Elements.append(NextPageTemplate('OneCol'))
	#Elements.append(PageBreak())

	Title = 'Remembered Classmates from LLA Class of 2009'
	Abstract = 'This report shows the comparison of your list of remembered names '
	'with a list of names of students in the class of 2009 from the '
	'2006, 2007, 2008, and 2009 Loma Linda Academy high school yearbooks.'
	'The purpose is to allow you to reflect on those you did not remember to include,'
	' which may help you remember them in the future.'

	textStyle(Title, Elements, style=HeaderStyle, sep=0.3)
	textStyle(Abstract, Elements, style=ParaStyle, sep=0.1)

	return Elements

def writeColumnExplanation():

	Elements = []

	styles = getSampleStyleSheet()
	
	HeaderStyle = styles['Heading1']
	ParaStyle = styles['Normal']
	PreStyle = styles['Code']

	Elements=[]

	Elements.append(NextPageTemplate('OneCol'))
	#Elements.append(PageBreak())

	Example = 'The following pages will show a complete list of classmate\'s names listed in the ordered remembered.'
	'Names that were not remembered are sorted alphabetically by last names.'
	'Corrected names are included if the spelling differs from the names provided in the relevant yearbooks.'
	'In some cases, a classmate\'s common name was used instead of the name in the yearbook.'
	'An example is \'Yuki Chavez\' instead of \'Liliana Chavez\'.'

	textStyle(Example, Elements, style=ParaStyle, sep=0.1)

	return Elements

def writeEndingCredit():
	Elements = []

	styles = getSampleStyleSheet()
	
	HeaderStyle = styles['Heading1']
	ParaStyle = styles['Normal']
	PreStyle = styles['Code']

	Elements=[]

	Elements.append(NextPageTemplate('EndCol'))
	Elements.append(PageBreak())
	Intro = '<b>Report Automated By:</b>'
	Author = 'Ryan Mercer'
	URL = 'http://www.cdslug.com'
	email = 'cdslug@gmail.com'

	textStyle('{}<br/>{}<br/>{}<br/>{}'.format(Intro,Author,URL,email), Elements, style=ParaStyle, sep=0.1)

	return Elements

def constructTrippleColumns(leftList, middlelList, rightList, listTitles):
	namesPerPage = 57
	styles=getSampleStyleSheet()
	Elements=[]

	stringListMaster = []

	currentCol = 'left'
	list1Index = 0
	list2Index = 0
	list3Index = 0

	leftColIndex = 0
	middleColIndex = 0
	rightColIndex = 0

	iterationLength = (int(max([len(leftList),len(middlelList)])/namesPerPage) + 1)*namesPerPage*3

	for i in range(0,iterationLength):

		if currentCol == 'left':
			if leftColIndex == 0:
				stringListMaster.append('<b>{}</b><br/>\n'.format(listTitles[0]))
				leftColIndex += 1
			elif leftColIndex < namesPerPage:
				if list1Index < len(leftList):
					stringListMaster.append('{}<br/>\n'.format(leftList[list1Index]))
					list1Index += 1
					leftColIndex += 1
				else:
					stringListMaster.append('<br/>\n')
					leftColIndex += 1
			else:
				currentCol = 'middle'
				leftColIndex = 0

		elif currentCol == 'middle':
			if middleColIndex == 0:
				stringListMaster.append('<b>{}</b><br/>\n'.format(listTitles[1]))
				middleColIndex += 1
			elif middleColIndex < namesPerPage:
				if list2Index < len(middlelList):
					stringListMaster.append('{}<br/>\n'.format(middleList[list2Index]))
					list2Index += 1
					middleColIndex += 1
				else:
					stringListMaster.append('<br/>\n')
					middleColIndex += 1
			else:
				currentCol = 'right'
				middleColIndex = 0

		elif currentCol == 'right':
			if rightColIndex == 0:
				stringListMaster.append('<b>{}</b><br/>\n'.format(listTitles[2]))
				rightColIndex += 1
			elif rightColIndex < namesPerPage:
				if list3Index < len(rightList):
					stringListMaster.append('{}<br/>\n'.format(rightList[list3Index]))
					list3Index += 1
					rightColIndex += 1
				else:
					stringListMaster.append('<br/>\n')
					rightColIndex += 1
			else:
				currentCol = 'left'
				rightColIndex = 0



	stringMaster = ''
	for substr in stringListMaster:
	  stringMaster += substr


	Elements.append(NextPageTemplate('ThreeCol'))
	Elements.append(PageBreak())
	Elements.append(Paragraph(stringMaster,styles['Normal']))

	return Elements

def generateReport(inputFilePath, inputCompleteFilePath, errorFilePath, yearbookReferenceFilePath, outputFilePath):

	# if(inputFilePath[0] == '.'):
	# 	return -1

	name = inputFilePath.replace('.','_').split('_')[1]
	doc = BaseDocTemplate(outputFilePath,showBoundary=0)
	Elements = []

	#normal frame as for SimpleFlowDocument
	frameT = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height+25, id='normal')

	#Two Columns
	frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-inch+20, doc.height, id='col1')
	frame2 = Frame(doc.leftMargin+doc.width/2-inch+12+20, doc.bottomMargin, doc.width/3,
				   doc.height, id='col2')
	frame3 = Frame(doc.leftMargin + doc.width/2+inch+20 +20, doc.bottomMargin, doc.width/3,
				   doc.height, id='col3')

	frameB = Frame(doc.leftMargin+doc.width-100, doc.bottomMargin, 130, 70, id='normal')

	Elements += writeIntro()

	indexedNamesDict = UtilFunc.parseDataFromFile(inputFilePath)
	# with open(inputFilePath, 'r') as pfi:
	# indexedNames = pfi.readlines()
	# indexedNamesDict = []
	# for line in indexedNames:
	# 	(l0,l1,l2,l3,l4,l5,l6,l7) = line.replace('\r','').replace('\n','').split(',')
	# #AlphaIndex,WrittenIndex,WrittenLast,WrittenFirst,YearbookLast,YearbookFirst,Spelling,GraduatedLLA09
	# 	indexedNamesDict.append({'AlphaIndex(int)':l0,
	# 							'WrittenIndex(int)':l1,
	# 							'WrittenLast':l2,
	# 							'WrittenFirst':l3,
	# 							'YearbookLast':l4,
	# 							'YearbookFirst':l5,
	# 							'Spelling':l6,
	# 							'GraduatedLLA09':l7})
	rememberedGrad = []
	forgottenGrad = []
	rememberedNonGrad = []
	forgottenNonGrad = []

	for entry in indexedNamesDict:
		if entry['GraduatedLLA09'].lower() == 'yes':
			if entry['WrittenIndex(int)'][0] == '-':
				forgottenGrad.append(entry)
			else:
				rememberedGrad.append(entry)
		elif entry['GraduatedLLA09'].lower() == 'no':
			if entry['WrittenIndex(int)'][0] == '-':
				forgottenNonGrad.append(entry)
			else:
				rememberedNonGrad.append(entry)

	rgCount = len(set([n['AlphaIndex(int)'] for n in rememberedGrad]))
	fgCount = len(forgottenGrad)
	rngCount = len(set([n['AlphaIndex(int)'] for n in rememberedNonGrad]))
	fngCount = len(forgottenNonGrad)
	Elements += constructSingleColumnParagraphs(['<br/><b>{}</b> students graduated in \'09 and <br/>' +
												 '<b>{}</b> additional students attended in either \'06, \'07, or \'08.'.format(rgCount + fgCount,
												 																				rngCount + fngCount)])
	

	drawing = MyDrawing()
	newData = [(fgCount,'{} classmates were not remembered (\'09)'.format(fgCount)),
			   (rgCount,'{} classmates were remembered (\'09)'.format(rgCount)),
			   (fngCount,'{} classmates were not remembered (other)'.format(fngCount)),
			   (rngCount,'{} classmates were remembered (other)'.format(rngCount))]

	drawing.setNewData(newData)
	Elements.append(drawing)

	Elements += writeColumnExplanation()

	rememberedGradString = [(n['WrittenFirst'] + ' ' + n['WrittenLast'])
						   for n in rememberedGrad]
	rememberedGradStringSp = [(n['YearbookFirst'] + ' ' + n['YearbookLast'])
						     if n['Spelling(dec)'][0] != 1
						     else ''
						     for n in rememberedGrad]
	forgottenGradString = [n['YearbookFirst'] + ' ' + n['YearbookLast'] for n in forgottenGrad]
	
	rememberedNonGradString = [(n['WrittenFirst'] + ' ' + n['WrittenLast'])
							  for n in rememberedNonGrad]
	rememberedNonGradStringSp = [(n['YearbookFirst'] + ' ' + n['YearbookLast'])
						        if n['Spelling(dec)'][0] != 1
						        else ''
						        for n in rememberedNonGrad]						  
	forgottenNonGradString = [n['YearbookFirst'] + ' ' + n['YearbookLast'] for n in forgottenNonGrad]


	listTitles09 = ['Not Remembered in 09','Remembered in 09', 'Yearbook Spelling']
	listTitlesOther = ['Not Remembered in 06, 07, or 08', 'Remembered in 06, 07, or 08', 'Yearbook Spelling']
	Elements += constructTrippleColumns(forgottenGradString,rememberedGradString, rememberedGradStringSp, listTitles09)
	Elements += constructTrippleColumns(forgottenNonGradString,rememberedNonGradString, rememberedNonGradStringSp, listTitlesOther)


	Elements += writeEndingCredit()

	doc.addPageTemplates([PageTemplate(id='OneCol',frames=frameT,onPage=foot2),
				  PageTemplate(id='ThreeCol',frames=[frame1,frame2,frame3],onPage=foot2),
				  PageTemplate(id='EndCol',frames=frameB,onPage=foot2)
				  ])

	#start the construction of the pdf
	doc.build(Elements)


########################
#####     MAIN     #####
########################
if __name__ == '__main__':
	usageDescription = ['inputFilePath: A full path to a .csv file containing an indexed list of names remembered and forgotten',
						'inputCompleteFilePath: ',
						'errorFilePath: ',
						'yearbookReferenceFilePath: A full path to a .csv file containing all expected classmates names along with their alphabetical index, among other details. See full documentation for extensive details',
						'outputFilePath: A full path to a .pdf file']

	UtilFunc.checkInputArgs(5,usageDescription)

	inputFilePath = sys.argv[1]
	inputCompleteFilePath = sys.argv[2]
	errorFilePath = sys.argv[3]
	yearbookReferenceFilePath = sys.argv[4]
	outputFilePath = sys.argv[5]

	generateReport(inputFilePath,inputCompleteFilePath, errorFilePath, yearbookReferenceFilePath,outputFilePath)
