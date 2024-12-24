import whisper
import ffmpeg
import os
import sys
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter import *

top = Tk(className='Video Transcriber')
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:    
    base_path = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(base_path, 'video-marketing.ico')
top.iconbitmap(icon_path)
top.geometry("500x500")

def transcribe_video():
    try:
        if not filename:
            mess.set("No video file selected!")
            return

        audio_path = "temp_audio.wav"
        mess.set(f"Processing video file: {filename}")

        ffmpeg.input(filename).output(audio_path).run(quiet=True)
        mess.set(f"{mess.get()}\nAudio extracted to: {audio_path}")

        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        mess.set(f"{mess.get()}\nTranscription completed.")
        
        if newFileName.get():
            if destFolder.get():
                text_file_path = f'{destFolder.get()}/{newFileName.get()}.txt'
            else:
                text_file_path = f'{newFileName.get()}.txt'
        elif destFolder.get():
            text_file_path = f'{destFolder.get()}/merged_file.txt'
        else:
            text_file_path = 'transcription.txt'
        with open(text_file_path, "w", encoding="utf-8") as text_file:
            text_file.write(result['text'])
        
        mess.set(f"{mess.get()}\nTranscription saved to: {text_file_path}")

    except ffmpeg._run.Error as e:
        mess.set(f"{mess.get()}\nFFmpeg error: {e}")
    except Exception as e:
        mess.set(f"{mess.get()}\nAn error occurred: {e}")

def select_folder():
    destFolder.set(askdirectory())

def show():
    global filename
    filename = askopenfilename(
        filetypes=[
            ("Video Files", "*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.mpeg *.mpg *.3gp *.webm"),
            ("MP4 Files", "*.mp4"),
            ("MKV Files", "*.mkv"),
            ("AVI Files", "*.avi"),
            ("MOV Files", "*.mov"),
            ("WMV Files", "*.wmv"),
            ("FLV Files", "*.flv"),
            ("MPEG Files", "*.mpeg *.mpg"),
            ("3GP Files", "*.3gp"),
            ("WebM Files", "*.webm"),
        ]
    )
    if filename:
        mess.set(f"Opened: {filename}")
    else:
        mess.set("No file selected.")

newFileName = StringVar()
destFolder = StringVar()
mess = StringVar()
filename = ""

# Buttons and UI Elements
Button(top, text="Open Video", command=show).place(x=50, y=50)
Button(top, text="Select New Destination Folder", command=select_folder).place(x=50, y=75)
Button(top, text='Transcribe Video', command=transcribe_video).place(x=50, y=100)

entry = Entry(top, textvariable=newFileName)
entry.place(x=250, y=75)

file_label = Label(top, text='Enter file name:')
file_label.place(x=250, y=50)

message_label = Label(
    top,
    anchor=N,
    textvariable=mess,
    height=25,
    width=50,
    bd=3,
    font=("Arial", 8, "bold"),
    justify=LEFT,
    wraplength=400
)
message_label.place(x=50, y=150)

top.mainloop()
