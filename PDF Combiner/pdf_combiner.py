import os
import sys
import pypdf
from tkinter import ttk
from tkinter.filedialog import askdirectory, askopenfilenames
from tkinter import *

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

top = Tk(className='PDF Merger Converter')
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
    global filenames
    filenames = askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    listbox.delete(0, END)
    for file in filenames:
        listbox.insert(END, file)

def select_folder():
    destFolder.set(askdirectory())

def print_file():
    global filenames
    mess.set(filenames.rsplit('.', 1)[0] + '.' + fileformat)

def merge():    
    merger = pypdf.PdfWriter()
    for pdf in filenames:
        merger.append(pdf)
    
    print(filenames[0].split('/')[-1])
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

Button(top, text="Open PDFs", command=lambda: show(box)).place(x=50, y=50)
Button(top, text="Select New Destination Folder", command=select_folder).place(x=50, y=75)
Button(top, text='Merge PDFs', command=merge).place(x=50, y=100)
entry = Entry(top, textvariable=newFileName)
label = Label(
    top,
    text='Enter new file name',
)
label.place(x = 250, y = 50)
entry.place(x=250, y=75)
box = RearrangeableListbox(top, selectmode=SINGLE)
box.place(x=0, y=150, relwidth=1, height=300)

top.mainloop()