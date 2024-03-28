from tkvideo import tkvideo
from moviepy.editor import VideoFileClip
import math
from customtkinter import *
from configparser import RawConfigParser
from tkinter import messagebox
config = RawConfigParser()
config.read("config.conf")
frameoffset = config.getint("MICHAELAPP", "innerframeoffset")

def PlayVideo(app: CTk, file: str, label: CTkLabel, function):
    video = tkvideo(file, label, loop=0, size=(600, 338))
    video.play()
    
    duration = math.ceil(VideoFileClip(file).duration*2)
    app.after(duration*1000, lambda: (label.place_forget(), function()))


def LoadDesktopIcons(icons: list):
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


def CheckForSpeedAndTime(speed, speedtype, time, timetype, function):
    try:
        speed, time = float(speed), float(time)

        if (speed == 0 or time == 0):
            return

        if(speedtype == "km/h"):
            speed = round(speed * 3.6)
        else:
            speed = round(speed)

        if(timetype == "perc"):
            time = int(time*60)
        else:
            time = round(time)

        config.set("3DSCENE", "speed", speed)
        config.set("3DSCENE", "time", time)
        SaveConfig()
        function()
    except:
        return



def SelectPath(label: CTkLabel):
    file = filedialog.askopenfilename(initialdir="/", title="Pontok megadása", filetypes=(("Szöveges fájl", "*.txt"),))
    filepathtext = file

    if len(file) > 100:
        filepathtext = file[:100]+"..."
    else:
        filepathtext = file

    if file:
        label.configure(text=filepathtext)
        LoadPositionsFromFile(file)
    else:
        label.configure(text="Hiba: Kérem adja meg a fájlt!")


def LoadPositionsFromFile(fajl):
    gyongyok = open(fajl)
    sorok = gyongyok.readlines()
    gyongyok.close()
    sorok.pop(0)

    positions = {}

    x, y, z = 0, 0, 0

    for i in range(len(sorok)):
        sor = sorok[i].split(";")
        sor = sor[:-1]

        try:
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
        except IndexError:
            messagebox.showerror("Betöltés sikertelen", "Hiba lépett fel a fájlok betöltése során.")


def SaveConfig():
    with open("config.conf", 'w') as configfile:
        config.write(configfile)