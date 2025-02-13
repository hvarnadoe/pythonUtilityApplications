import os
import sys
import pypdf
from tkinter import ttk
from tkinter.filedialog import askdirectory, askopenfilenames
from tkinter import *
'''
pyinstaller --onefile --icon="pdf.ico" --noconsole --add-data="pdf.ico;." pdf_combiner.py
'''
class RearrangeableListbox(Listbox):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.bind("<Button-1>", self.on_start)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_drop)
        self.curIndex = None

    def on_start(self, event):
        self.curIndex = self.nearest(event.y)

    def on_drag(self, event):
        if self.curIndex is not None:
            i = self.nearest(event.y)
            if i < self.curIndex:
                x = self.get(i)
                self.delete(i)
                self.insert(i + 1, x)
                self.curIndex = i
            elif i > self.curIndex:
                x = self.get(i)
                self.delete(i)
                self.insert(i - 1, x)
                self.curIndex = i

    def on_drop(self, event):
        self.curIndex = None

top = Tk(className=' PDF Merger Converter')
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:    
    base_path = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(base_path, 'pdf.ico')
top.iconbitmap(icon_path)

newFileName = StringVar()
destFolder = StringVar()
filenames = []
fileformat = 'png'
mess = StringVar()

top.geometry("500x500")

def show(listbox):
    mess.set('')
    global filenames
    filenames = askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    listbox.delete(0, END)
    for file in filenames:
        listbox.insert(END, file)

def select_folder():
    mess.set('')
    destFolder.set(askdirectory())
    
def merge():    
    merger = pypdf.PdfWriter()
    for pdf in filenames:
        merger.append(pdf)
    if newFileName.get():
        if destFolder.get():
            output = open(f'{destFolder.get()}/{newFileName.get()}.pdf', "wb")
        else:
            output = open(f'{newFileName.get()}.pdf', "wb")
    elif destFolder.get():
        output = open(f'{destFolder.get()}/merged_file.pdf', "wb")
    else:
        output = open('merged_file.pdf', "wb")
    merger.write(output)
    mess.set("Merge Completed")

def update_label(*args):
    label.config(text=mess.get())
def update_dest(*args):
    folderLabel.config(text=destFolder.get())

mess.trace_add("write", update_label)
destFolder.trace_add("write", update_dest)

Button(top, text="Open PDFs", command=lambda: show(box)).place(x=50, y=50)
Button(top, text="Select New Destination Folder", command=select_folder).place(x=50, y=75)
Button(top, text='Merge PDFs', command=merge).place(x=50, y=100)
entry = Entry(top, textvariable=newFileName)
label = Label(
    top,
    text='Enter new file name',
)
label.place(x= 250, y= 25)
entry.place(x=250, y= 50)
label = Label(
    top,
    text = mess.get()
)
label.place(x=150, y=105)
folderLabel = Label(
    top,
    text = destFolder.get()
)
folderLabel.place(x= 250, y= 75)
box = RearrangeableListbox(top, selectmode=SINGLE)
box.place(x=0, y=150, relwidth=1, height=300)

top.mainloop()