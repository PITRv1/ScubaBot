from tkvideo import tkvideo
from moviepy.editor import VideoFileClip
import math
from customtkinter import *
from configparser import RawConfigParser
config = RawConfigParser()
config.read("config.conf")
def PlayVideo(app: CTk, file: str, label: CTkLabel, function):
    video = tkvideo(file, label, loop=0, size=(600, 338))
    video.play()
    
    duration = math.ceil(VideoFileClip(file).duration*2)
    app.after(duration*1000, lambda: (label.place_forget(), function()))

def LoadDesktopIcons(icons: list):
    for i in range(len(icons)):
        icons[i].place(x=25, y=25+i*100)

def UnloadDesktopIcons(icons: list):
    for i in range(len(icons)):
        icons[i].place_forget()

def SelectPath(label: CTkLabel):
    file = filedialog.askopenfilename(initialdir="/", title="Pontok megadása", filetypes=(("Szöveges fájl", "*.txt"),))
    
    if file:
        label.configure(text=str(file))
        config.set("3DSCENE", "pointpath", file)
        SaveConfig()
    else:
        label.configure(text="Hiba: Kérem adjon meg egy fájlt!")

def SaveConfig():
    with open("config.conf", 'w') as configfile:
        config.write(configfile)