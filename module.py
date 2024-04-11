from assets.lib.tkvideo import tkvideo
from moviepy.editor import VideoFileClip
import math
from PIL import Image
from customtkinter import *
from configparser import RawConfigParser
from tkinter import messagebox
from typing import Callable
from ast import literal_eval

config = RawConfigParser()
config.read("config.conf", encoding="utf8")

timescale = config.getint("LOADING", "timescale")
fastboot = config.getboolean("LOADING", "fastboot")
font_family = config.get("GLOBAL", "font")
font_size = config.getint("GLOBAL", "size")
title_font_size = config.getint("GLOBAL", "titlefontsize")
taskbar_height = config.getint("TASKBAR", "height")
taskbar_color = config.get("TASKBAR", "color")
appbackgroundcolor= config.get("GLOBAL", "appbackgroundcolor")
accentcolor = config.get("GLOBAL", "accentcolor")
hovercolor = config.get("GLOBAL", "hovercolor")
framecolor = config.get("GLOBAL", "framebackgroundcolor")
medence_multiplier = config.getint("MICHAELAPP", "medencemultiplier")
frameoffset = config.getint("MICHAELAPP", "innerframeoffset")

font = (font_family, font_size)
title_font = (font_family ,title_font_size)

def LoadImage(file: str, width: int, height: int) -> CTkImage:
    return CTkImage(Image.open(file), size=(width, height))


def PlayVideo(app: CTk, file: str, label: CTkLabel, Function: Callable):
    video = tkvideo(file, label, loop=0, size=(600, 338))
    video.play()
    
    duration = math.ceil(VideoFileClip(file).duration*2)
    app.after(duration*1000, lambda: (label.place_forget(), Function()))


def SetView(value: int):
    value = bool(value)
    config.set("3DSCENE", "fps", value)
    SaveConfig()


def LoadIconText(texts: list):
    for i in range(len(texts)):
        texts[i].place(x=25, y=90+i*100)

def LoadIcons(icons: list):
    for i in range(len(icons)):
        icons[i].place(x=25, y=25+i*100)


def UnloadAssets(elements: list):
    for i in range(len(elements)):
        elements[i].place_forget()


def SetSliderLabelValue(value, label: CTkLabel, text: str):
    label.configure(text=f"{text} {int(value)}")


def OverwriteMedenceSize(x_slider: CTkSlider, y_slider: CTkSlider, z_slider: CTkSlider):
    x, y, z = int(x_slider.get()), int(y_slider.get()), int(z_slider.get())

    config.set("3DSCENE", "medence", [x, y, z])
    SaveConfig()


def SetFramesWidthAndHeight(parentframe: CTkFrame, frames: list):
    width = parentframe._current_width-frameoffset
    height = parentframe._current_height-frameoffset

    for i in range(len(frames)):
        frames[i].configure(width=width, height=height)


def PlaceRow(attributes: list, values:list):
    for i in range(len(attributes)):

        offset = 20*i
        ypos = 500+offset

        attribute = attributes[i]
        value = values[i]

        attribute.configure(font=font, text_color="white", bg_color=framecolor, fg_color=framecolor)
        value.configure(font=font, text_color=accentcolor, bg_color=framecolor, fg_color=framecolor)

        attribute.place(x=720, y=ypos, anchor="w")
        value.place(x=1170, y=ypos, anchor="e")


def SetSpeedAndTime(speed: str, speedtype: str, time: str, timetype: str):
    try:
        if speed and time:
            speed, time = float(speed), int(time)

            if(speedtype == "km/h"):
                speed = speed * 3.6
            else:
                speed = speed

            if(timetype == "perc"):
                time = time*60
            else:
                time = round(time)

            config.set("3DSCENE", "speed", speed)
            config.set("3DSCENE", "time", time)
            SaveConfig()
            return True
    except:
        return False


def GetMedence() -> list:
    config.read("config.conf",  encoding="utf8")

    medence = config.get("3DSCENE", "medence")
    medence = literal_eval(medence)

    return medence


def SelectPath(label: CTkLabel):
    global positionsfilepath
    file = filedialog.askopenfilename(initialdir="/", title="Pontok megadása", filetypes=(("Szöveges fájl", "*.txt"),))
    filepathtext = file
    positionsfilepath = file

    if len(file) > 100:
        filepathtext = file[:100]+"..."
    else:
        filepathtext = file
    if file:
        label.configure(text=filepathtext)
    else:
        label.configure(text="Hiba: Kérem adja meg a fájlt!")


def LoadPositionsFromFile(delfirstrow: StringVar):

    if len(positionsfilepath) == 0:
        return

    gyongyok = open(positionsfilepath)
    sorok = gyongyok.readlines()
    gyongyok.close()

    delfirstrow = bool(int(delfirstrow.get()))

    if (delfirstrow):
        sorok.pop(0)

    positions = {}
    x, y, z = 0, 0, 0
    
    try:
        for i in range(len(sorok)):
            sor = sorok[i].split(";")
            sor = sor[:-1]

            current_x = int(sor[0])
            current_y = int(sor[1])
            current_z = int(sor[2])
            current_e = int(sor[3])

            if current_x > x: 
                x = current_x

            if current_y > y: 
                y = current_y

            if current_z > z: 
                z = current_z

            positions[i] = {"x": current_x, "y": current_y, "z": current_z, "e": current_e}

            config.set("3DSCENE", "points", positions)
            config.set("3DSCENE", "medence", [x, y, z])
            SaveConfig()
    except IndexError and ValueError:
            messagebox.showerror("Betöltés sikertelen", "Hiba lépett fel a fájl betöltése során.")
            return False
    return True
    


def SaveConfig():
    with open("config.conf", 'w', encoding="utf8") as configfile:
        config.write(configfile)


def AnimateFrame(frame: CTkFrame, app: CTk, heightoffset: int, widthoffset: int, animtype: str="open") -> bool:
    try:
        frame.place(x=0, y=0)
        step=10
        
        width = app.winfo_screenwidth()-widthoffset
        height = app.winfo_screenheight()-heightoffset

        if animtype == "open":
            frame.configure(height=200)

        while True:
            currwidth = frame.winfo_width()
            currheight = frame.winfo_height()

            if animtype == "open":
                

                if currwidth < width:
                    frame.configure(width=currwidth+step)
                elif currheight < height:
                    frame.configure(height=currheight+step)
                elif currheight == height or currheight > height:
                    return True
                
            else:
                if currwidth-step != 1:
                    frame.configure(width=currwidth-step)
                elif currheight != 1:
                    frame.configure(height=currheight-step)
                elif currheight == 1:
                    frame.place_forget()
                    return True
            
            frame.update()
    except:
        return False