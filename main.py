from customtkinter import *
from window_anim import animate_window
from configparser import RawConfigParser
from datetime import datetime
from PIL import Image
from module import PlayVideo, LoadDesktopIcons, UnloadAssets, SelectPath, SetFramesWidthAndHeight, SetSliderLabelValue, OverwriteMedenceSize, CheckForSpeedAndTime
from ast import literal_eval

set_appearance_mode("dark")
app = CTk()
app.title = "SEAOS"
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
michael_framecolor = config.get("MICHAELAPP", "framebackgroundcolor")
medence_multiplier = config.getint("MICHAELAPP", "medencemultiplier")


font = (font_family, font_size)
title_font = (font_family ,title_font_size)


def LoadImage(file: str, width: int=app.winfo_screenwidth(), height: int=app.winfo_screenheight()):
    return CTkImage(Image.open(file), size=(width, height))

# BOOT
boot_background = CTkLabel(app, text="", image=LoadImage("./images/blackscreen.png"))
bootlogo = CTkLabel(app, text="", image=LoadImage("./images/SeaOS_bootscreen.png", 325, 200))
boot_progress = CTkProgressBar(app, width=200, mode="indeterminate", progress_color=michael_accentcolor)
boot_progress.start()

# ASZTAL
desktop_background = CTkLabel(app, text="", image=LoadImage("./images/SeaOS_background.png"))

taskbar = CTkFrame(app, fg_color=taskbar_color, corner_radius=0)
taskbar_logo = CTkLabel(app, text="", image=LoadImage("./images/SeaOS_taskbar.png", 40, 40))
time = CTkLabel(app, bg_color=taskbar_color, text_color="black", text="Loading....", font=font)
date = CTkLabel(app, bg_color=taskbar_color, text_color="black", text="Loading....", font=font)

michael_button = CTkButton(app, text="", width=50, height=50, corner_radius=0, border_width=0, fg_color="cyan", hover_color="cyan", image=LoadImage("./images/michael.png", 50, 50), command=lambda: LoadMichaelApp())
michael_button2 = CTkButton(app, text="", width=50, height=50, corner_radius=0, border_width=0, fg_color="cyan", hover_color="cyan", image=LoadImage("./images/michael.png", 50, 50), command=lambda: LoadMichaelApp())

# MICHAEL ABLAK
michwin = CTkFrame(app, border_width=1, corner_radius=0, border_color=michael_backgroundcolor, fg_color=michael_backgroundcolor)


def Boot():
    boot_background.place(x=0, y=0)
    bootlogo.place(relx=0.1, rely=0.1, anchor=CENTER)
    app.after(10*timescale, lambda: bootlogo.place_forget())
    app.after(15*timescale, lambda: boot_progress.place(relx=0.5, rely=0.7, anchor=CENTER))
    app.after(20*timescale, lambda: bootlogo.place_configure(relx=0.5, rely=0.5, anchor=CENTER))
    app.after(85*timescale, lambda: LoadDesktop())

def LoadDesktop():
    UnloadAssets([boot_background, bootlogo, boot_progress])
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
    michwin_title = CTkLabel(michwin, text="buvarrobot (michael) wireless shell.APP".upper(), font=font, text_color=michael_accentcolor, bg_color=michael_backgroundcolor)
    current_title = CTkLabel(app, text="betöltés...".upper(), font=title_font, text_color=michael_accentcolor, bg_color=michael_framecolor)
    quit_button = CTkButton(michwin, font=font, text="Bezárás", fg_color=michael_accentcolor, hover_color=michael_hovercolor, command=lambda: CloseApp())
    found_video_label = CTkLabel(michwin, text="", bg_color=michael_framecolor)

    # <FÁJL KIVÁLASZTÁS>
    file_frame = CTkFrame(michwin, fg_color=michael_framecolor)
    file_title = CTkLabel(file_frame, text="Út: Nincsen megadva", font=font, text_color=michael_accentcolor, bg_color=michael_framecolor, fg_color=michael_framecolor)
    file_select_button = CTkButton(file_frame, text="Fájl kiválasztása", font=font, bg_color=michael_framecolor, fg_color=michael_accentcolor, hover_color=michael_hovercolor)
    file_done_button = CTkButton(file_frame, text="Kész", font=font, bg_color=michael_framecolor, fg_color=michael_accentcolor, hover_color=michael_hovercolor)

    # <MEDENCE BEÁLLITÁS>
    medence_frame = CTkFrame(michwin, fg_color=michael_framecolor)
    medence_x_label = CTkLabel(medence_frame, text="X", font=font, text_color=michael_accentcolor, bg_color=michael_framecolor, fg_color=michael_framecolor)
    medence_y_label = CTkLabel(medence_frame, text="Y", font=font, text_color=michael_accentcolor, bg_color=michael_framecolor, fg_color=michael_framecolor)
    medence_z_label = CTkLabel(medence_frame, text="Z", font=font, text_color=michael_accentcolor, bg_color=michael_framecolor, fg_color=michael_framecolor)

    medence_x_slider = CTkSlider(medence_frame, progress_color=michael_accentcolor, command=lambda value: SetSliderLabelValue(value, medence_x_label, "X:"))
    medence_y_slider = CTkSlider(medence_frame, progress_color=michael_accentcolor, command=lambda value: SetSliderLabelValue(value, medence_y_label, "Y:"))
    medence_z_slider = CTkSlider(medence_frame, progress_color=michael_accentcolor, command=lambda value: SetSliderLabelValue(value, medence_z_label, "Z:"))

    medence_done_button = CTkButton(medence_frame, text="Kész", font=font, bg_color=michael_framecolor, fg_color=michael_accentcolor, hover_color=michael_hovercolor)


    # <IDÓ ÉS SEBESSÉG>
    timeandspeed_frame = CTkFrame(michwin, fg_color=michael_framecolor)
    speedtime_done_button = CTkButton(timeandspeed_frame, text="Kész", font=font, bg_color=michael_framecolor, fg_color=michael_accentcolor, hover_color=michael_hovercolor)

    speed_input = CTkEntry(timeandspeed_frame, font=font, text_color=michael_accentcolor, border_color=michael_accentcolor, placeholder_text="Sebesség")
    speed_dropdown = CTkOptionMenu(timeandspeed_frame, font=font, fg_color=michael_accentcolor, dropdown_font=font, dropdown_hover_color=michael_accentcolor, values=["m/s", "km/h"])

    time_input = CTkEntry(timeandspeed_frame, font=font, border_color=michael_accentcolor, text_color=michael_accentcolor, placeholder_text="Idő")
    time_dropdown = CTkOptionMenu(timeandspeed_frame, font=font, fg_color=michael_accentcolor, dropdown_font=font, dropdown_hover_color=michael_accentcolor, values=["másodperc", "perc"])


    UnloadAssets([michael_button, michael_button2])
    if animate_window(michwin, app, heightoffset=50, widthoffset=0):
        current_title.place(relx=0.5, rely=0.2, anchor=CENTER)
        SetFramesWidthAndHeight(michwin, [file_frame, medence_frame, timeandspeed_frame])

        michwin_title.place(relx=0.1, rely=0.01, anchor=CENTER)
        quit_button.place(relx=0.95, rely=0.01, anchor=CENTER)
        file_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        

        def LoadOpenFileStage():
            UnloadAssets([medence_frame])
            current_title.configure(text="adja meg a gyongyok.txt-t".upper())

            file_select_button.configure(command=lambda: (SelectPath(file_title), file_done_button.configure(state=NORMAL)))
            file_done_button.configure(command=lambda: LoadMedenceStage(), state=DISABLED)

            file_select_button.place(relx=0.5, rely=0.5, anchor=CENTER)
            file_done_button.place(relx=0.5, rely=0.55, anchor=CENTER)
            file_title.place(relx=0.5, rely=0.45, anchor=CENTER)


        def LoadMedenceStage():
            UnloadAssets([file_frame])
            config.read("config.conf")
            current_title.configure(text="állítsa be a medencét".upper())
            medence_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

            medence = literal_eval(config.get("3DSCENE", "medence"))
            min_x, min_y, min_z = medence[0], medence[1], medence[2]

            medence_x_slider.configure(from_=min_x, to=min_x*medence_multiplier)
            medence_x_slider.place(relx=0.52, rely=0.45, anchor=CENTER)
            medence_x_label.place(relx=0.44, rely=0.45, anchor=CENTER)

            medence_y_slider.configure(from_=min_y, to=min_y*medence_multiplier)
            medence_y_slider.place(relx=0.52, rely=0.50, anchor=CENTER)
            medence_y_label.place(relx=0.44, rely=0.50, anchor=CENTER)

            medence_z_slider.configure(from_=min_z, to=min_z*medence_multiplier)
            medence_z_slider.place(relx=0.52, rely=0.55, anchor=CENTER)
            medence_z_label.place(relx=0.44, rely=0.55, anchor=CENTER)

            medence_done_button.configure(command=lambda: (OverwriteMedenceSize(medence_x_slider, medence_y_slider, medence_z_slider), LoadMichaelSettings()))
            medence_done_button.place(relx=0.5, rely=0.60, anchor=CENTER)
            

        def LoadMichaelSettings():
            UnloadAssets([medence_frame])
            current_title.configure(text="állítsa be az időt és sebességet".upper())
            timeandspeed_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
            
            speed_input.place(relx=0.45, rely=0.45, anchor=CENTER)
            speed_dropdown.place(relx=0.55, rely=0.45, anchor=CENTER)

            time_input.place(relx=0.45, rely=0.50, anchor=CENTER)
            time_dropdown.place(relx=0.55, rely=0.50, anchor=CENTER)

            speedtime_done_button.configure(command=lambda: CheckForSpeedAndTime(speed_input.get(), speed_dropdown.get(), time_input.get(), time_dropdown.get(), LoadVideos())) #, LoadCloseStage
            speedtime_done_button.place(relx=0.5, rely=0.55, anchor=CENTER)


        def LoadVideos():
            UnloadAssets([timeandspeed_frame, quit_button, michwin_title])
            found_video_label.place(relx=0.5, rely=0.5, anchor=CENTER)
            michwin.configure(fg_color="black")
            app.after(500, lambda: current_title.configure(text_color="#00FF51", bg_color="black", text="michael (búvárhajó) megkeresése".upper()))
            app.after(1500, lambda: PlayVideo(app, "./anims/found/found.mp4", found_video_label, lambda: CloseApp()))


        def CloseApp():
            UnloadAssets([file_frame, medence_frame, timeandspeed_frame, timeandspeed_frame, current_title, quit_button, michwin_title])
            if (animate_window(michwin, app, heightoffset=50, widthoffset=0, animtype="close")):
                michwin.configure(fg_color=michael_backgroundcolor)
                current_title.configure(text_color=michael_accentcolor, bg_color=michael_backgroundcolor)
                LoadDesktopIcons([michael_button, michael_button2])

        LoadOpenFileStage()

if fastboot:
    LoadDesktop()
else:
    Boot()
app.mainloop()