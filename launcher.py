import customtkinter
from customtkinter import *
from readfile import LoadPositionsFromFile
import subprocess as sub
customtkinter.set_appearance_mode("system")

app = CTk()
app.title("ScubaBot Launcher")
app.geometry("600x400")
app.resizable(False, False)
app.grid_columnconfigure(0, weight=1)

Lightblue = "#24b9f9"
Blue = "#0099CA"
Darkblue = "#337be6"
padx = 10
pady = 10

def CreatePopoutWindow(message):
    win = CTkToplevel(app)
    win.title("ScubaBot Launcher Popout")
    win.geometry("300x100")
    win.resizable(True, True)
    win.grid_columnconfigure(0, weight=1)
    win.grab_set()
        
    def Exit():
        win.destroy()
        win.update()

    error = CTkLabel(win, text_color=Blue, text=message, font=("Arial", 20))
    error.focus()

    button_ok = CTkButton(win, fg_color=Blue, hover_color=Darkblue, text="Ok", command=Exit)

    error.grid(row=0, column=0, padx=padx, pady=pady)
    button_ok.grid(row=1, column=0, padx=padx, pady=pady)
    win.mainloop()

def Start():
    file = str(file_name_input.get())+".txt"

    speedtype = speed_dropdown.get()
    speed = speed_input.get()

    timetype = time_dropdown.get()
    time = time_input.get()

    if(file and speed and time):
        if(speedtype == "km/h"):
            speed = int(float(speed) * 3.6)
        
        if(timetype == "perc"):
            time = int(float(time)*60)

        positions = LoadPositionsFromFile(file)

        sub.Popen(["python", "opp_sub.py", f"{positions}", f"{speed}", f"{time}"])
        exit()
    else:
        CreatePopoutWindow("Kérem töltsön ki minden mezőt!")


mainframe = CTkFrame(app)

title_label = CTkLabel(app, text_color=Blue, text="ScubaBot Launcher", font=("Arial", 50))
team_label = CTkLabel(app, text_color=Blue, text="Csapat: undefined", font=("Arial", 15))

file_name_text = CTkLabel(mainframe, text_color=Blue, text="Gyöngyök poziciói (fájlnév):")
file_name_input = CTkEntry(mainframe, border_color=Blue)
file_type_label = CTkLabel(mainframe, text_color=Blue, text=".txt")

speed_text = CTkLabel(mainframe, text_color=Blue, text="Sebesség:")
speed_input = CTkEntry(mainframe, border_color=Blue)
speed_dropdown = CTkOptionMenu(mainframe, fg_color=Blue, dropdown_hover_color=Blue, button_hover_color=Darkblue, button_color=Lightblue, values=["m/s", "km/h"])

time_text = CTkLabel(mainframe, text_color=Blue, text="Idő:")
time_input = CTkEntry(mainframe, border_color=Blue)
time_dropdown = CTkOptionMenu(mainframe, fg_color=Blue, dropdown_hover_color=Blue, button_hover_color=Darkblue, button_color=Lightblue, values=["másodperc", "perc"])

button_start = CTkButton(app, width=300, fg_color=Blue, hover_color=Darkblue, text="Start", command=Start)

#Elemek elheleyzése
title_label.grid(row=0, column=0, padx=padx, pady=pady)
team_label.grid(row=1, column=0, padx=padx, pady=pady)

mainframe.grid(row=2, column=0, padx=padx, pady=pady)
button_start.grid(row=3, column=0, padx=padx, pady=pady)

file_name_text.grid(row=0, column=0, padx=padx, pady=pady)
file_name_input.grid(row=0, column=1, padx=padx, pady=pady)
file_type_label.grid(row=0, column=2, padx=padx, pady=pady)

speed_text.grid(row=1, column=0, padx=padx, pady=pady)
speed_input.grid(row=1, column=1, padx=padx, pady=pady)
speed_dropdown.grid(row=1, column=2, padx=padx, pady=pady)

time_text.grid(row=2, column=0, padx=padx, pady=pady)
time_input.grid(row=2, column=1, padx=padx, pady=pady)
time_dropdown.grid(row=2, column=2, padx=padx, pady=pady)


file_name_input.insert(0, "gyongyok")
app.mainloop()