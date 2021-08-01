# Auto PDF filler
import os
import csv
import sys
import pprint
from pdfjinja import PdfJinja
import shutil
import pathlib
import pypdftk

# glabal variables
datasetPath="ds1.csv"
templatePath="form1.pdf"
group="groupA"



#### <-------[ START OF FUNCTIONS]------->
# create list of dictionaries. One dict woud be one dataset. The whole list carries all data
def lister(csvPath):
	try:
		print("\nreading CSV from\n"+csvPath, file=sys.stderr)
		reader = csv.DictReader(open(csvPath, 'r'))
		theList = []
		for line in reader:
			theList.append(line)

		pprint.pprint(theList)
		return theList

	except Exception as e:
		print(e, file=sys.stderr)

# takes in list and writes PDFs of them
def PDFer(allData, pdfPath, group):
	try:
		print("\nreading PDF from\n"+pdfPath, file=sys.stderr)
		thePDF = PdfJinja(pdfPath)
		print("\ncreating filled PDFs ...")
		# will always overwrite if existing group name folder exists
		shutil.rmtree("./filled/"+group, ignore_errors=True)
		pathlib.Path('./filled/'+group).mkdir(parents=True)
		count = 0
		for x in allData:
			count = count + 1
			pdfout = thePDF(x)
			pdfout.write(open("./filled/"+group+"/filled" +"-"+
							  group+"-"+str(count)+".pdf", "wb"))

		print(str(count)+" files created for "+group)

	except Exception as e:
		print(e, file=sys.stderr)

# Reads PDFs from specified directory and compiles them into single PDF with many pages
def masher(pdfdir, group):
	allPDF = []
	for file in os.listdir(pdfdir):
		allPDF.append(os.path.normpath(os.path.join(pdfdir, file))	)

	try:
		# creates the "compiled" folder. If it already exists, do nothing
		pathlib.Path('./compiled').mkdir(parents=True, exist_ok=True)
		outFilePath = "./compiled/all-forms-"+group+".pdf"
		pypdftk.concat(allPDF, outFilePath)
		print("\n\nCompleted compiling PDFs!")
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		outFile = "all-forms-"+group+".pdf"

		return outFile

	except Exception as e:
		print(e)
		print("\nerror compiling PDFs\n")

#### <-------[END OF FUNCTIONS]------->


# Calling the functions
PDFer(lister(datasetPath), templatePath, group)
outFileName = masher("./filled/"+group, group)
print("output file name: "+outFileName+"\n\n")