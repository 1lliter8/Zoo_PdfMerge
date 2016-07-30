from PyPDF2 import PdfFileReader, PdfFileWriter
from PyQt4 import QtCore, QtGui, uic
import sys

form_class = uic.loadUiType('merge.ui')[0]

class Merge(QtGui.QWidget, form_class):
	def __init__(self, info, parent = None):
		QtGui.QWidget.__init__(self, parent)
		self.setupUi(self)
		
		self.openButton.clicked.connect(self.btn_getFiles)
		self.emptyButton.clicked.connect(self.btn_clearList)
		self.mergeButton.clicked.connect(self.btn_expFiles)
	
	def btn_getFiles(self):
		files = QtGui.QFileDialog.getOpenFileNames(self, 'Select one or more files to open', '/home', 'PDFs (*.pdf)')
		self.pdfList.addItems(files)
	
	def btn_clearList(self):
		self.pdfList.clear()
	
	def btn_expFiles(self):
		files = []
		for i in xrange(self.pdfList.count()):
			files.append(self.pdfList.item(i).text())
		
		mask = PdfFileReader(file('mask.pdf', 'rb'))
		newpdf = PdfFileWriter()
	
		for filename in files:
			x = PdfFileReader(file(filename, 'rb'))
			x_p1 = x.getPage(0)
			x_p2 = x.getPage(1)
			mask_p1 = mask.getPage(0)
			x_p1.mergePage(mask_p1)
			x_p1.compressContentStreams()
			
			newpdf.addPage(x_p1)
			newpdf.addPage(x_p2)
			
		name = QtGui.QFileDialog.getSaveFileName(self, 'Save as', '/home', selectedFilter='*.pdf')
		
		with file(name, 'wb') as output:
			newpdf.write(output)

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = Merge(form_class)
	myapp.show()
	sys.exit(app.exec_())