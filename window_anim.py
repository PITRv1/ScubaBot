def animate_window(frame, app, heightoffset: int, widthoffset: int, animtype="open"):
    frame.place(x=0, y=0)
    step=10
     
    width = app.winfo_screenwidth()-widthoffset
    height = app.winfo_screenheight()-heightoffset
    
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