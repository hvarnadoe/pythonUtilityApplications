import os
import sys
from tkinter import ttk
from tkinter.filedialog import askdirectory, askopenfilenames
from tkinter import *
import pillow_heif
from PIL import Image

top = Tk(className=' Image File Converter')
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:    
    base_path = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(base_path, 'photo_icon.ico')
top.iconbitmap(icon_path)

filenames = []
fileformat = 'png'
foldername = ''
mess = StringVar()

top.geometry("500x500")
'''
pyinstaller --onefile --icon="photo_icon.ico" --noconsole --add-data="photo_icon.ico;." file_converter.py
'''
def show():
    global filenames

    filenames = askopenfilenames()
    if filenames:
        mess.set(f"Selected: {filenames}")
    else:
        mess.set("No file selected!")

def select_folder():
    global foldername
    foldername = askdirectory()

def convert():
    global filenames
    global fileformat
    global foldername

    if not filenames:
        mess.set("No file selected!")
        return    

    format_mapping = {
        "png": "PNG",
        "jpg": "JPEG",
        "ico": "ICO",
        "bmp": "BMP",
        "tiff": "TIFF",
        "webp": "WEBP",
        "pdf": "PDF"
    }

    
    if 'Select' not in combo.get():
        fileformat = combo.get()

    pillow_format = format_mapping.get(fileformat.lower(), None)
    if not pillow_format:
        mess.set(f"Unsupported format: {fileformat}")
        return
    mess.set('')
    try:
        for filename in filenames:
            if 'heif' in filename or 'heic' in filename:
                img = pillow_heif.read_heif(filename)
                image = Image.frombytes(
                    img.mode,
                    img.size,
                    img.data,
                    "raw",
                )
            else:
                image = Image.open(filename)

            if pillow_format == "JPEG" and image.mode == "RGBA":
                image = image.convert("RGB")

            if foldername:
                filename = foldername + '/' + filename.split('/')[-1]

            new_filename = filename.rsplit('.', 1)[0] + '.' + fileformat
            image.save(new_filename, format=pillow_format)
            mess.set(f"{mess.get()}File converted and saved as {new_filename}\n")

    except Exception as e:
        mess.set(f"Error: {e}")

def print_file():
    global filenames
    mess.set(filenames.rsplit('.', 1)[0] + '.' + fileformat)


Button(top, text="Open File", command=show).place(x=50, y=50)
Button(top, text="Select New Destination Folder", command=select_folder).place(x=50, y=75)
Button(top, text='Convert File', command=convert).place(x=50, y=100)

combo = ttk.Combobox(
    state="readonly",
    values=["png", "jpg", "ico", "bmp", "tiff", "webp", "pdf"]
)
combo.place(x=200, y=50)
combo.set('Select Format (png)')

label = Label(
    top,
    anchor=N,
    textvariable=mess,
    height=50,
    width=50,
    bd=3,
    font=("Arial", 8, "bold"),
    justify=LEFT,
    underline=0,
    wraplength=250
)
label.place(x = 50, y = 150)
top.mainloop()
