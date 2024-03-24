def animate_window(frame, app, heightoffset: int, widthoffset: int, animtype="open"):
    frame.place(x=0, y=0)
    step=10
     
    width = app.winfo_screenwidth()-widthoffset
    height = app.winfo_screenheight()-heightoffset
    
    # if animtype == "open":
    #     while True:
    #         if currwidth != width:
    #             frame.update()
    #             frame.configure(width=currwidth+step)
    #         elif currwidth != width:
    #             frame.update()
    #             frame.configure(height=currheight+step)


    #     while currwidth != width:
    #         frame.update()
    #         frame.configure(width=currwidth+step)

    #     while currheight != height:
    #         frame.update()
    #         frame.configure(height=currheight+step)

        
    #     return True
    # else:
    #     while currwidth > 20:
    #         frame.update()
    #         frame.configure(width=currwidth+step)

    #     while currheight > 0:
    #         frame.update()
    #         frame.configure(height=currheight+step)
    #     return True

        
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
            if currwidth-step != 20:
                frame.configure(width=currwidth-step)
            elif currheight != 1:
                frame.configure(height=currheight-step)
            elif currheight == 1:
                frame.place_forget()
                return True
        
        frame.update()