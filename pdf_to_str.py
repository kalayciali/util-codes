from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open

def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laParams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laParams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content

filename = "file2.txt"
# for pdf file within local computer
pdfFile = open('./file3.pdf', 'rb')
# pdfFile = urlopen('http://pythonscraping.com/pages/warandpeace/chapter1.pdf')
# pdfFile is binary
outputString = readPDF(pdfFile)

with open(filename, 'w+') as f:
    f.write(outputString)

pdfFile.close()


