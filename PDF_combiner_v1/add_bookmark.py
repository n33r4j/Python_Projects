# Add bookmark to pdf
# Does not work !

from PyPDF2 import PdfFileWriter, PdfFileReader

path = r'C:\Users\neera\Documents\Python Scripts\Python_Github_repo\Python_Projects\PDF_combiner_v1'

output = PdfFileWriter()
input = PdfFileReader(open(path+r'\pdf_file_02.pdf', 'rb'))

print("Encrypted ?:", input.isEncrypted)

if input.isEncrypted:
    input.decrypt('')
    
print(input.getNumPages())
output.addPage(input.getPage(3))
output.addBookmark('Hello, World Bookmark', 0, parent=None)
output.setPageMode("/UseOutlines")

# outputStream = open(path + r'result.pdf', 'wb')
# output.write(outputStream)
# outputStream.close()