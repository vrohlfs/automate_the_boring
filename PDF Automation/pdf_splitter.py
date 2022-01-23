from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import re
import PyPDF2

def getPagebreakList(file_name: str)->list:
    
    pdf_file = PyPDF2.PdfFileReader(file_name)
    num_pages = pdf_file.getNumPages()
    page_breaks = list()
    codes = list()

    for i in range(0, num_pages):
        PageObj = pdf_file.getPage(i)
        Text = PageObj.extractText() 

        if re.search(r"Atta ID:", Text):
            # THIS ASSUMES THAT ATTA ID ARE 4 DIGITS, FOLLOWED BY HYPHEN, THEN 3 DIGITS (E.G. 7475-018)
            code = re.search(r"[0-9]{4}-[0-9]{3}Atta ID:", Text)
            codes.append(code.group(0)[0:8])
            page_breaks.append(i)
    
    return page_breaks, codes


inputpdf = PdfFileReader(open("pdf_sample_file.pdf", "rb"))
num_pages = inputpdf.numPages
page_breaks, codes = getPagebreakList('pdf_sample_file.pdf')
mergedObject = PdfFileMerger()


i=0
for i in page_breaks:
    position = page_breaks.index(i)
    output = PdfFileWriter()
    try:
        for j in range(i, page_breaks[position+1]):
            output.addPage(inputpdf.getPage(j))
        with open("ATTA_ID_%s.pdf" % codes[position], "wb") as outputStream:
            output.write(outputStream)
    except: 
        for j in range(i, num_pages):
            output.addPage(inputpdf.getPage(j))
        with open("ATTA_ID_%s.pdf" % codes[position], "wb") as outputStream:
            output.write(outputStream)

