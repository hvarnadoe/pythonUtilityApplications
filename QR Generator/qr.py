import qrcode
import os
import sys
from tkinter import ttk
from tkinter.filedialog import askdirectory, askopenfilenames
from tkinter import *

'''
pyinstaller --onefile --icon="qr-code.ico" --noconsole --add-data="qr-code.ico;." qr.py
'''

top = Tk(className=' QR Code Generator')
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:    
    base_path = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(base_path, 'qr-code.ico')
top.iconbitmap(icon_path)

newFileName = StringVar()
destFolder = StringVar()
url = StringVar()

top.geometry("500x500")

def select_folder():
    destFolder.set(askdirectory())

def generateQR():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url.get())
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    filename = 'new_qr_code.png'
    if newFileName.get():
        if destFolder.get():
            filename = open(f'{destFolder.get()}/{newFileName.get()}.png', "wb")
        else:
            filename = open(f'{newFileName.get()}.png', "wb")
    elif destFolder.get():
        filename = open(f'{destFolder.get()}/new_qr_code.png', "wb")

    img.show()
    img.save(filename)

label = Label(
    top,
    text='Paste URL',
)
label.place(x = 50, y = 50)
entry = Entry(top, textvariable=url)
entry.place(x=50, y=75)
Button(top, text="Select New Destination Folder", command=select_folder).place(x=50, y=100)
Button(top, text='Generate QR Code', command=generateQR).place(x=50, y=125)
entry2 = Entry(top, textvariable=newFileName)
label2 = Label(
    top,
    text='Enter new file name',
)
label2.place(x = 250, y = 50)
entry2.place(x=250, y=75)

top.mainloop()