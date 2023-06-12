from modules.sanware_carter import *
from ai_config import *

from tkinter import *
import tkinter.font as tkFont
import tkinter as tk

def send_message():
    sentence = messageWindow.get("1.0", "end-1c")

    messageWindow.delete("1.0", "end")

    SendToCarter(sentence, User, APIkey)

    with open("CarterResponse.txt") as f:
        ResponseOutput = f.read()

    chatWindow.insert("end", f"\n{User}: {sentence}")
    chatWindow.insert("end", f"\n{UIName}: {ResponseOutput}")
    chatWindow.see("end")

    speak(ResponseOutput)

def StartVC():
    VoiceCommand(UIName, User)

    with open("CarterResponse.txt") as f:
        ResponseOutput = f.read()

    chatWindow.insert("end", f"\n{User}: {sentence}")
    chatWindow.insert("end", f"\n{UIName}: {ResponseOutput}")
    chatWindow.see("end")

    speak(ResponseOutput)

# Create tkinter window
root = Tk()

root.title(f"{UIName.upper()}")
#setting window size
width=407
height=183
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)

root.attributes('-alpha',0.85)

chatWindow = Text(root, bd=1, bg="black", width=50, height=8, fg="yellow")
chatWindow.place(x=10,y=20,width=224,height=90)

messageWindow = Text(root, bg="lightblue", width=30, height=4, fg="black")
messageWindow.place(x=10,y=120,width=224,height=53)

SpeakButton=tk.Button(root)
SpeakButton["bg"] = "#a78d8d"
ft = tkFont.Font(family='Helvetica',size=14)
SpeakButton["font"] = ft
SpeakButton["fg"] = "#000000"
SpeakButton["justify"] = "center"
SpeakButton["text"] = "Speak"
SpeakButton.place(x=320,y=120,width=74,height=52)
SpeakButton["command"] = StartVC

SendButton=tk.Button(root)
SendButton["bg"] = "#a99b9b"
ft = tkFont.Font(family='Helvetica',size=14)
SendButton["font"] = ft
SendButton["fg"] = "#000000"
SendButton["justify"] = "center"
SendButton["text"] = "Send"
SendButton.place(x=240,y=120,width=74,height=52)
SendButton["command"] = send_message

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

messageWindow.bind("<Return>", lambda event: send_message())

root.mainloop()
