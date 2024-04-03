from customtkinter import *
from datetime import datetime
from module import *
from subprocess import Popen

set_appearance_mode("dark")
SetView(0)
app = CTk()
app.title("SEAOS")
app.attributes("-fullscreen", True)
app.iconbitmap("./assets/images/michael.ico")
default_height = app.winfo_screenheight()
default_width = app.winfo_screenwidth()


# BOOT
boot_background = CTkLabel(app, text="", image=LoadImage("./assets/images/blackscreen.png", default_width, default_height))
bootlogo = CTkLabel(app, text="", image=LoadImage("./assets/images/SeaOS_bootscreen.png", 325, 200))
boot_progress = CTkProgressBar(app, width=200, mode="indeterminate", progress_color=accentcolor)
boot_progress.start()

# ASZTAL
desktop_background = CTkLabel(app, text="", image=LoadImage("./assets/images/SeaOS_background.png", default_width, default_height))

taskbar = CTkFrame(app, fg_color=taskbar_color, corner_radius=0)
taskbar_button = CTkButton(taskbar, text="", fg_color=taskbar_color, hover_color=accentcolor, width=50, image=LoadImage("./assets/images/SeaOS_taskbar.png", 40, 40), command=lambda: ShowOrHideStart())
time = CTkLabel(taskbar, bg_color=taskbar_color, text_color="black", text="Loading....", font=font)
date = CTkLabel(taskbar, bg_color=taskbar_color, text_color="black", text="Loading....", font=font)

michael_button = CTkButton(app, text="", width=50, height=50, corner_radius=0, border_width=0, fg_color="cyan", hover_color=accentcolor, image=LoadImage("./assets/images/michael.png", 50, 50), command=lambda: LoadMichaelApp())
micheal_text = CTkLabel(app, text="buvar.run", text_color="black", bg_color="white", font=font)

system_button = CTkButton(app, text="", width=50, height=50, corner_radius=0, border_width=0, fg_color="gray", hover_color=accentcolor, image=LoadImage("./assets/images/system.png", 50, 50), command=lambda: LoadSystemApp())
system_text = CTkLabel(app, text="sysfo.run", text_color="black", bg_color="white", font=font)

icons = [michael_button, system_button]
texts = [micheal_text, system_text]

# START
start_frame = CTkFrame(app, fg_color=taskbar_color, corner_radius=0)
start_label =  CTkLabel(start_frame, text="START MENÜ", text_color=accentcolor, bg_color="white", font=font).place(x=10, y=0)
shutdown_button = CTkButton(start_frame, text="Kikapcsolás", fg_color=taskbar_color, text_color="black", font=font, hover_color="red", command=lambda: app.quit()).place(x=10, rely=1, anchor="sw")


# ABLAKOK
michwin = CTkFrame(app, border_width=1, corner_radius=0, border_color=appbackgroundcolor, fg_color=appbackgroundcolor)
systemwin = CTkFrame(app, border_width=1, corner_radius=0, border_color=appbackgroundcolor, fg_color=appbackgroundcolor)


isstartshowing = False
def ShowOrHideStart():
    global isstartshowing 
    if isstartshowing :
        isstartshowing = False
        start_frame.place_forget()
    else:
        isstartshowing = True
        start_frame.place(x=0, y=default_height-taskbar_height*1, anchor="sw")


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
    app.after(20*timescale, lambda: taskbar_button.place(x=2, y=2))
    app.after(35*timescale, lambda: time.place(x=default_width-70, y=0))
    app.after(35*timescale, lambda: date.place(x=default_width-85, y=20))

    app.after(40*timescale, lambda: LoadDesktopIcons())
    app.after(50*timescale, lambda: UpdateTime())


def UpdateTime():
    time.configure(text=datetime.now().strftime('%H:%M:%S'))
    date.configure(text=datetime.now().strftime('%Y.%m.%d'))

    app.after(10*timescale, UpdateTime)


def UnloadDesktopIcons():
    UnloadAssets(icons)
    UnloadAssets(texts)


def LoadDesktopIcons():
    LoadIcons(icons)
    LoadIconText(texts)


def LoadSystemApp():
    win_title = CTkLabel(systemwin, text="rendszer infromáció.app".upper(), font=font, text_color=accentcolor, bg_color=appbackgroundcolor)
    quit_button = CTkButton(systemwin, font=font, text="Bezárás", fg_color=accentcolor, hover_color=hovercolor, command=lambda: CloseApp())
    inner_frame = CTkFrame(systemwin, fg_color=framecolor)

    inner_frame_title = CTkLabel(inner_frame, text="rendszer információk".upper(), font=title_font, text_color=accentcolor, bg_color=framecolor)
    display_image = CTkLabel(inner_frame, text="", image=LoadImage("./assets/images/display.png", 270, 220))

    team_attribute = CTkLabel(inner_frame, text="Csapat:  ")
    team_value = CTkLabel(inner_frame, text="undefined")

    ui_attribute = CTkLabel(inner_frame, text="Kezelőfelületet kódolta: ")
    ui_value = CTkLabel(inner_frame, text="Kovács Dániel Benedek")

    env_attribute = CTkLabel(inner_frame, text="3D-s környezetet fejlesztette: ")
    env_value = CTkLabel(inner_frame, text="Tóth Péter Sándor")

    algo_attribute = CTkLabel(inner_frame, text="Algoritmus(oka)t programozta: ")
    algo_value = CTkLabel(inner_frame, text="Borók Máté")

    if AnimateFrame(systemwin, app, 50, 0):
        UnloadDesktopIcons()
        SetFramesWidthAndHeight(systemwin, [inner_frame])
        win_title.place(x=frameoffset/2, y=10, anchor="w")
        inner_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        quit_button.place(relx=0.95, y=10, anchor=CENTER)

        inner_frame_title.place(relx=0.5, rely=0.15, anchor=CENTER)
        display_image.place(relx=0.5, rely=0.32, anchor=CENTER)

        PlaceRow([team_attribute, ui_attribute, env_attribute, algo_attribute], [team_value, ui_value, env_value, algo_value])

        def CloseApp():
            UnloadAssets([quit_button, inner_frame, win_title])
            if (AnimateFrame(systemwin, app, 50, 0, animtype="close")):
                LoadDesktopIcons()

def LoadMichaelApp():
    win_title = CTkLabel(michwin, text="michael remote shell UI.app".upper(), font=font, text_color=accentcolor, bg_color=appbackgroundcolor)
    quit_button = CTkButton(michwin, font=font, text="Bezárás", fg_color=accentcolor, hover_color=hovercolor, command=lambda: CloseApp())
    current_title = CTkLabel(app, text="betöltés...".upper(), font=title_font, text_color=accentcolor, bg_color=framecolor)
    video_label = CTkLabel(michwin, text="", bg_color=framecolor)
    skip_button = CTkButton(michwin, text="Átugrás", font=font, bg_color="black", text_color="black" , fg_color="#00FF51", hover_color="#009951", command=lambda: CloseApp())

    # <FÁJL KIVÁLASZTÁS>
    file_frame = CTkFrame(michwin, fg_color=framecolor)
    file_title = CTkLabel(file_frame, text="Út: Nincsen megadva", font=font, text_color=accentcolor, bg_color=framecolor, fg_color=framecolor)
    file_select_button = CTkButton(file_frame, text="Fájl kiválasztása", font=font, bg_color=framecolor, fg_color=accentcolor, hover_color=hovercolor)
    file_done_button = CTkButton(file_frame, text="Kész", font=font, bg_color=framecolor, fg_color=accentcolor, hover_color=hovercolor)

    file_delfirstrow_var = StringVar(value=False)
    file_delfirstrow_checkbox = CTkCheckBox(file_frame, font=font, text="Első sor törlése", fg_color=accentcolor, text_color=accentcolor, variable=file_delfirstrow_var, onvalue=True, offvalue=False)
    
    # <MEDENCE BEÁLLITÁS>
    medence_frame = CTkFrame(michwin, fg_color=framecolor)
    medence_x_label = CTkLabel(medence_frame, text="X", font=font, text_color=accentcolor, bg_color=framecolor, fg_color=framecolor)
    medence_y_label = CTkLabel(medence_frame, text="Y", font=font, text_color=accentcolor, bg_color=framecolor, fg_color=framecolor)
    medence_z_label = CTkLabel(medence_frame, text="Z", font=font, text_color=accentcolor, bg_color=framecolor, fg_color=framecolor)

    medence_x_slider = CTkSlider(medence_frame, progress_color=accentcolor, command=lambda value: SetSliderLabelValue(value, medence_x_label, "X:"))
    medence_y_slider = CTkSlider(medence_frame, progress_color=accentcolor, command=lambda value: SetSliderLabelValue(value, medence_y_label, "Y:"))
    medence_z_slider = CTkSlider(medence_frame, progress_color=accentcolor, command=lambda value: SetSliderLabelValue(value, medence_z_label, "Z:"))

    medence_done_button = CTkButton(medence_frame, text="Kész", font=font, bg_color=framecolor, fg_color=accentcolor, hover_color=hovercolor)

    # <IDÓ, SEBESSÉG, ALGO ÉS NÉZET>
    timeandspeed_frame = CTkFrame(michwin, fg_color=framecolor)
    speedtime_done_button = CTkButton(timeandspeed_frame, text="Kész", font=font, bg_color=framecolor, fg_color=accentcolor, hover_color=hovercolor)

    speed_input = CTkEntry(timeandspeed_frame, font=font, text_color=accentcolor, border_color=accentcolor, placeholder_text="Sebesség")
    speed_dropdown = CTkOptionMenu(timeandspeed_frame, font=font, fg_color=accentcolor, dropdown_font=font, dropdown_hover_color=accentcolor, values=["m/s", "km/h"])

    time_input = CTkEntry(timeandspeed_frame, font=font, border_color=accentcolor, text_color=accentcolor, placeholder_text="Idő")
    time_dropdown = CTkOptionMenu(timeandspeed_frame, font=font, fg_color=accentcolor, dropdown_font=font, dropdown_hover_color=accentcolor, values=["másodperc", "perc"])

    view_var = StringVar(value=0)
    view_checkbox = CTkCheckBox(timeandspeed_frame, font=font, text="Belsőnézet", fg_color=accentcolor, text_color=accentcolor, variable=view_var, onvalue=True, offvalue=False, command=lambda: SetView(int(view_var.get())))


    if AnimateFrame(michwin, app, 50, 0):
        SetFramesWidthAndHeight(michwin, [file_frame, medence_frame, timeandspeed_frame])
        UnloadDesktopIcons()
        win_title.place(x=frameoffset/2, y=10, anchor="w")
        quit_button.place(relx=0.95, y=10, anchor=CENTER)

        current_title.place(relx=0.5, rely=0.2, anchor=CENTER)
        file_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        

        def LoadOpenFileStage():
            UnloadAssets([medence_frame])
            current_title.configure(text="válassza ki a gyöngyöket tartalmazó fájlt".upper())

            file_select_button.configure(command=lambda: (SelectPath(file_title), file_done_button.configure(state=NORMAL)))
            file_done_button.configure(command=lambda: WaitForSuccesOrFailure(), state=DISABLED)

            def WaitForSuccesOrFailure():
                if LoadPositionsFromFile(file_delfirstrow_var):
                    LoadMedenceStage()

            file_title.place(relx=0.5, rely=0.45, anchor=CENTER)
            file_delfirstrow_checkbox.place(relx=0.5, rely=0.5, anchor=CENTER)
            file_select_button.place(relx=0.5, rely=0.55, anchor=CENTER)

            file_done_button.place(relx=0.5, rely=0.65, anchor=CENTER)



        def LoadMedenceStage():
            UnloadAssets([file_frame])
            current_title.configure(text="állítsa be a medencét".upper())
            medence_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

            medence = GetMedence()
            
            min_x, min_y, min_z = medence[0], medence[1], medence[2]

            medence_x_slider.configure(from_=min_x, to=min_x*medence_multiplier)
            medence_x_slider.set(min_x)
            medence_x_slider.place(relx=0.52, rely=0.45, anchor=CENTER)
            medence_x_label.place(relx=0.44, rely=0.45, anchor=CENTER)

            medence_y_slider.configure(from_=min_y, to=min_y*medence_multiplier)
            medence_y_slider.set(min_y)
            medence_y_slider.place(relx=0.52, rely=0.50, anchor=CENTER)
            medence_y_label.place(relx=0.44, rely=0.50, anchor=CENTER)

            medence_z_slider.configure(from_=min_z, to=min_z*medence_multiplier)
            medence_z_slider.set(min_z)
            medence_z_slider.place(relx=0.52, rely=0.55, anchor=CENTER)
            medence_z_label.place(relx=0.44, rely=0.55, anchor=CENTER)

            medence_done_button.configure(command=lambda: (OverwriteMedenceSize(medence_x_slider, medence_y_slider, medence_z_slider), LoadMichaelSettings()))
            medence_done_button.place(relx=0.5, rely=0.60, anchor=CENTER)
            

        def LoadMichaelSettings():
            UnloadAssets([medence_frame])
            current_title.configure(text="állítsa be a nézetet, időt és sebességet".upper())
            timeandspeed_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
            
            speed_input.place(relx=0.45, rely=0.45, anchor=CENTER)
            speed_dropdown.place(relx=0.55, rely=0.45, anchor=CENTER)

            time_input.place(relx=0.45, rely=0.50, anchor=CENTER)
            time_dropdown.place(relx=0.55, rely=0.50, anchor=CENTER)

            view_checkbox.place(relx=0.5, rely=0.55, anchor=CENTER)

            speedtime_done_button.configure(command=lambda: SetInfo())
            speedtime_done_button.place(relx=0.5, rely=0.65, anchor=CENTER)

            def SetInfo():
                if (SetSpeedAndTime(speed_input.get(), speed_dropdown.get(), time_input.get(), time_dropdown.get())):
                    LoadVideos()


        def LoadVideos():
            UnloadAssets([timeandspeed_frame, quit_button, win_title])
            michwin.configure(fg_color="black")

            skip_button.place(relx=0.5, rely=0.8, anchor=CENTER)
            def PlayFindVideo():
                app.after(500, lambda: current_title.configure(text_color="#00FF51", bg_color="black", text="michael (búvárhajó) megkeresése".upper()))
                video_label.place(relx=0.5, rely=0.5, anchor=CENTER)
                app.after(1500, lambda: PlayVideo(app, "./assets/anims/found/found.mp4", video_label, lambda: PlaySendVideo()))

            def PlaySendVideo():
                app.after(500, lambda: current_title.configure(text_color="#00FF51", bg_color="black", text="Konfigurációs fájl küldése".upper()))
                video_label.place(relx=0.5, rely=0.5, anchor=CENTER)
                app.after(1500, lambda: PlayVideo(app, "./assets/anims/send/send.mp4", video_label, lambda: CloseApp()))

            PlayFindVideo()


        def CloseApp():
            UnloadAssets([file_frame, medence_frame, timeandspeed_frame, timeandspeed_frame, current_title, quit_button, win_title, video_label, skip_button])
            if (AnimateFrame(michwin, app, 50, 0, animtype="close")):
                michwin.configure(fg_color=appbackgroundcolor)
                current_title.configure(text_color=accentcolor, bg_color=appbackgroundcolor)
                LoadDesktopIcons()
                Popen(["python", "scubabot.py"])

        
        LoadOpenFileStage()

if fastboot:
    LoadDesktop()
else:
    Boot()
app.mainloop()