#
# Pdf file combiner v1
# 
# author: n33r4j
#
# Stuff to do:
# 1. Add a 'remove file' button.
# 2. Add 'drag and drop' functionality.
# 3. Improve GUI layout and style.
# 4. Perform tests.


import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import PyPDF2, os


# Create root window

path = r'C:\Users\neera\Documents'
current_script_location = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()
root.title('PDF File Combiner v1')
root.resizable(False, True)
root.geometry('650x300')
root.iconphoto(False, tk.PhotoImage(file=os.path.join(current_script_location,'images\pdf_combiner_logo_64x64_v1.png')))

files_added = {}      # Mapping buttons to corresponding labels on the left
files_to_combine = [] # List of filenames
row_counter = 2       # Counter for adding the widgets for a new file


heading_label = tk.Label(text="Add files to be combined", font=("Helvetica", 12))
AF_label_1 = tk.Label(text="", anchor='e', width=70, bg="#ffffff") # Added Files (AF)

# Callback function for picking files.
def select_file(parent_button):
    
    filetypes = (
        ('pdf files', '*.pdf'),
        ('All files', '*.*')
    )
    
    # returns the filename that you select from GUI.
    filename = fd.askopenfilename(
        title = 'Open a file',
        initialdir=path,
        filetypes=filetypes
    )
    
    # Show the filepath on the label corresponding to the button.
    files_added[parent_button].config(text = filename)
    files_to_combine.append(filename)
    
    # if filename:
        # showinfo(
            # title='Selected File',
            # message=filename
        # )
    # else:


# Open button
open_button_1 = ttk.Button(
    root,
    text='Choose a .pdf file',
)

files_added[open_button_1] = AF_label_1
open_button_1.config(command=lambda:select_file(open_button_1))

# Callback function for adding a new label and button to add files.
def add_file():
    file_label = tk.Label(text="", anchor='e', width=70, bg="#ffffff") # Added Files (AF)
    # added_files_labels.append(file_label)
    open_file_button = ttk.Button(
        root,
        text='Choose a .pdf file',
    )
    
    global files_added
    files_added[open_file_button] = file_label
    open_file_button.config(command=lambda:select_file(open_file_button))
    
    global row_counter
    file_label.grid(row=row_counter,column=0, columnspan=5, padx=10)
    open_file_button.grid(row=row_counter,column=6)
    row_counter += 1
    add_file_button_1.grid(row=row_counter,column=6)
    combine_button.grid(row=row_counter+1,column=2)

# Callback function for combining PDFs and saving the combined file.
def combine_PDFs():
    # save_location = tk.filedialog.askdirectory()
    print("Combining the following files in this order:")
    pdfWriter = PyPDF2.PdfFileWriter()
    for filename in files_to_combine:
        if filename:
            print(filename)
            pdfFile = open(filename,'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFile)
            for pageNum in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
            # pdfFile.close()
            # Keep the input files open while writing the output file.
            # Issue with PyPDF2 [https://github.com/mstamy2/PyPDF2/issues/293#issuecomment-403420175]
            
    # pdfOutputfile = open(path+r'\Masters Y1 - T3\GSOE9011 - Eng PG Coursework Research Skills\Job Postings\combined_PDF.pdf', 'wb')
    pdfOutputfile = fd.asksaveasfile(mode='wb', title='Choose save location and filename', filetypes=(('pdf files', '*.pdf'),('All files', '*.*')))
    pdfWriter.write(pdfOutputfile)
    pdfOutputfile.close()
    print("Files combined!")
    

add_file_button_1 = ttk.Button(
    root,
    text='+',
    command=add_file
)

combine_button = ttk.Button(
    root,
    text='Combine PDFs',
    command=combine_PDFs
)

# Positioning the widgets on a grid.
heading_label.grid(row=0,column=0, columnspan=6, pady=10)
AF_label_1.grid(row=1,column=0, columnspan=5, padx=10)
open_button_1.grid(row=1,column=6)
add_file_button_1.grid(row=2,column=6)
combine_button.grid(row=row_counter+1,column=2)

# Run Application
root.mainloop()