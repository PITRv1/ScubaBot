import customtkinter
from customtkinter import *
from window_anim import animate_window
from PIL import Image
from configparser import RawConfigParser
from datetime import datetime
from tkvideo import tkvideo
from moviepy.editor import VideoFileClip
import math

config = RawConfigParser()
config.read("./seaos.conf")

taskbar_height = int(config.get("TASKBAR", "height"))
taskbar_color = config.get("TASKBAR", "color")
timescale = int(config.get("LOADING", "timescale"))
font = (config.get("GLOBAL", "font"), int(config.get("GLOBAL", "size")))

app = CTk()
app.geometry("1200x800")
app.attributes("-fullscreen", True)

def LoadImage(file: str, width=app.winfo_screenwidth(), height=app.winfo_screenheight()):
    return CTkImage(Image.open(file), size=(width, height))

default_height = app.winfo_screenheight()
default_width = app.winfo_screenwidth()

# BOOT
boot_background = CTkLabel(app, text="", image=LoadImage("./images/blackscreen.png"))

bootlogo = CTkLabel(app, text="", image=LoadImage("./images/SeaOS_bootscreen.png", 325, 200))

boot_progress = CTkProgressBar(app, width=200, mode="indeterminate", progress_color="#0099CA")
boot_progress.start()

# ASZTAL
desktop_background = CTkLabel(app, text="", image=LoadImage("./images/SeaOS_background.png"))

taskbar = CTkFrame(app, fg_color=taskbar_color, corner_radius=0)
taskbar_logo = CTkLabel(app, text="", image=LoadImage("./images/SeaOS_taskbar.png", 40, 40))
time = CTkLabel(app, bg_color=taskbar_color, text_color="black", text="Loading....", font=font)
date = CTkLabel(app, bg_color=taskbar_color, text_color="black", text="Loading....", font=font)

# IKONOK
michael_button = CTkButton(app, text="", width=50, height=50, corner_radius=0, border_width=0, fg_color="cyan", hover_color="cyan", image=LoadImage("./images/michael.png", 50, 50), command=lambda: LoadTestApp())

# TESZT ABLAK
testwindow = CTkFrame(app, border_width=1, corner_radius=0, border_color="black", fg_color="black")
found_video_label = CTkLabel(testwindow, text="")

def PlayVideo(file, label, function):
    video = tkvideo(file, label, loop=0, size=(600, 338))
    video.play()
    
    duration = math.ceil(VideoFileClip(file).duration*1.65)
    app.after(duration*1000, lambda: (label.place_forget(), function()))


def UnloadBootAssets():
    boot_background.place_forget()
    bootlogo.place_forget()
    boot_progress.place_forget()

def Boot():
    boot_background.place(x=0, y=0)
    bootlogo.place(relx=0.05, rely=0.05, anchor=CENTER)
    app.after(10*timescale, lambda: bootlogo.place_forget())
    app.after(15*timescale, lambda: boot_progress.place(relx=0.5, rely=0.7, anchor=CENTER))
    app.after(20*timescale, lambda: bootlogo.place_configure(relx=0.5, rely=0.5, anchor=CENTER))
    app.after(85*timescale, lambda: LoadDesktop())

def LoadDesktop():
    UnloadBootAssets()
    app.after(6*timescale, lambda: desktop_background.place(x=0, y=0, relwidth=1, relheight=1))

    app.after(13*timescale, lambda: taskbar.place(x=0, y=default_height-taskbar_height, relwidth=1))
    app.after(20*timescale, lambda: taskbar_logo.place(x=5, y=default_height-taskbar_height+5))

    app.after(35*timescale, lambda: time.place(x=default_width-70, y=default_height-taskbar_height))
    app.after(35*timescale, lambda: date.place(x=default_width-85, y=default_height-taskbar_height+20))

    app.after(40*timescale, lambda: LoadDesktopIcons())

    app.after(50*timescale, lambda: UpdateTime())

def LoadDesktopIcons():
    michael_button.place(x=25, y=25)

def UpdateTime():
    time.configure(text=datetime.now().strftime('%H:%M:%S'))
    date.configure(text=datetime.now().strftime('%Y.%m.%d'))

    app.after(10*timescale, UpdateTime)

def test():
    print("heloeore")

def LoadTestApp():
    michael_button.place_forget()

    if animate_window(testwindow, app, heightoffset=50, widthoffset=0):
        buttontest = CTkButton(testwindow, font=font, text="Exit", fg_color="green", hover_color="green", command=lambda: animate_window(testwindow, app, heightoffset=50, widthoffset=0, animtype="close"))

        found_video_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        PlayVideo("./anims/found/found.mp4", found_video_label, lambda: LoadCloseStage())

        def LoadCloseStage():
            buttontest.place(relx=0.5, rely=0.5, anchor=CENTER)

Boot()
app.mainloop()