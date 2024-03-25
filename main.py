from customtkinter import *
from window_anim import animate_window
from configparser import RawConfigParser
from datetime import datetime
from PIL import Image
from module import PlayVideo, LoadDesktopIcons, UnloadDesktopIcons, SelectPath

set_appearance_mode("dark")
app = CTk()
app.geometry("1200x800")
app.attributes("-fullscreen", True)

default_height = app.winfo_screenheight()
default_width = app.winfo_screenwidth()

config = RawConfigParser()
config.read("./config.conf")

timescale = config.getint("LOADING", "timescale")
fastboot = config.getboolean("LOADING", "fastboot")
font_family = config.get("GLOBAL", "font")
font_size = config.getint("GLOBAL", "size")
title_font_size = config.getint("GLOBAL", "titlefontsize")
taskbar_height = config.getint("TASKBAR", "height")
taskbar_color = config.get("TASKBAR", "color")
michael_backgroundcolor= config.get("MICHAELAPP", "backgroundcolor")
michael_accentcolor = config.get("MICHAELAPP", "accentcolor")
michael_hovercolor = config.get("MICHAELAPP", "hovercolor")

font = (font_family, font_size)
title_font = (font_family ,title_font_size)

def LoadImage(file: str, width: int=app.winfo_screenwidth(), height: int=app.winfo_screenheight()):
    return CTkImage(Image.open(file), size=(width, height))

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
michael_button = CTkButton(app, text="", width=50, height=50, corner_radius=0, border_width=0, fg_color="cyan", hover_color="cyan", image=LoadImage("./images/michael.png", 50, 50), command=lambda: LoadMichaelApp())
michael_button2 = CTkButton(app, text="", width=50, height=50, corner_radius=0, border_width=0, fg_color="cyan", hover_color="cyan", image=LoadImage("./images/michael.png", 50, 50), command=lambda: LoadMichaelApp())

# MICHAEL ABLAK
michwin = CTkFrame(app, border_width=1, corner_radius=0, border_color=michael_backgroundcolor, fg_color=michael_backgroundcolor)
michwin_title = CTkLabel(michwin, text="buvarrobot (michael) wireless shell".upper(), font=font, text_color=michael_accentcolor, bg_color=michael_backgroundcolor).place(relx=0.08, rely=0.01, anchor=CENTER)

found_video_label = CTkLabel(michwin, text="")

current_title = CTkLabel(michwin, text="", font=title_font, text_color=michael_accentcolor, bg_color=michael_backgroundcolor)

file_title = CTkLabel(app, text="Út: Nincsen megadva", font=font, text_color=michael_accentcolor, bg_color=michael_backgroundcolor)
file_select_button = CTkButton(app, text="Fájl kiválasztása", font=font, fg_color=michael_accentcolor, hover_color=michael_hovercolor, command=lambda: SelectPath(file_title))

def UnloadBootAssets():
    boot_background.place_forget()
    bootlogo.place_forget()
    boot_progress.place_forget()

def Boot():
    boot_background.place(x=0, y=0)
    bootlogo.place(relx=0.1, rely=0.1, anchor=CENTER)
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

    app.after(40*timescale, lambda: LoadDesktopIcons([michael_button, michael_button2]))
    app.after(50*timescale, lambda: UpdateTime())

def UpdateTime():
    time.configure(text=datetime.now().strftime('%H:%M:%S'))
    date.configure(text=datetime.now().strftime('%Y.%m.%d'))

    app.after(10*timescale, UpdateTime)

def LoadMichaelApp():
    UnloadDesktopIcons([michael_button, michael_button2])

    if animate_window(michwin, app, heightoffset=50, widthoffset=0):
        current_title.place(relx=0.5, rely=0.1, anchor=CENTER)
        found_video_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        current_title.configure(text="michael (búvárhajó) megkeresése".upper())
        PlayVideo(app, "./anims/found/found.mp4", found_video_label, lambda: LoadOpenFileStage())
        
        def LoadOpenFileStage():
            current_title.configure(text="adja meg a gyongyok.txt-t".upper())
            file_select_button.place(relx=0.5, rely=0.5, anchor=CENTER)
            file_title.place(relx=0.5, rely=0.45, anchor=CENTER)

        def LoadCloseStage():
            quit_button = CTkButton(michwin, font=font, text="Exit", fg_color=michael_accentcolor, hover_color=michael_hovercolor, command=lambda: (animate_window(michwin, app, heightoffset=50, widthoffset=0, animtype="close"), quitwin()))
            quit_button.place(relx=0.95, rely=0.02, anchor=CENTER)

        def quitwin():
            LoadDesktopIcons([michael_button, michael_button2])

if fastboot:
    LoadDesktop()
else:
    Boot()
app.mainloop()