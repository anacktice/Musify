# Importing important libraries and files

# from signal import pause
from tkinter import *
import os
from threading import *
from PIL import ImageTk, Image
import Play_DLL
import Dwl_Manager
import url_extracter
import customtkinter
import pafy
from time import sleep
import time

# -------------------  Basic Variable Setup -------------------  #

music_dir = f"""{os.environ["USERPROFILE"]}\\Music"""
images_dir = f"""{os.getcwd()}\\Images"""
queue = []
activity = "Idle"
song_duration = 0
song_url = ""
sleeptime = 0
currently_playing = ""
SongName = ""
paused = False
close_app  = False
progress_value = 0.0
player_index = 0.0
length = 0
timeSliderLast = 0
timeSliderUpdate = time.time()

##################################################################



# -------------------  Basic GUI Setup -------------------  #

window = customtkinter.CTk()
window.title("Musify")
window.iconbitmap(f"{images_dir}/icon.ico")
window.configure(bg = "#25242C")
window.resizable(False, False)

## --- Function to close the app --- ##

def close_code():
    global close_app

    print("entered")

    close_app = True
    try:
        Play_DLL.player.stop()
    except:
        pass
    window.destroy()
    exit()

#######################################

window.protocol('WM_DELETE_WINDOW', close_code) # overriding the function of the X button in the title bar

# Set the geometry of Tkinter Frame
window.geometry("1095x600")

# creating  the Image File
bg = ImageTk.PhotoImage(file=f"{os.getcwd()}/Images/background.jpg")
search_imag = ImageTk.PhotoImage(file=f"{os.getcwd()}/Images/background.jpg")

# Create a Canvas
canvas = customtkinter.CTkCanvas(window, width=700, height=3500,
    bg = "#FFFFFF",
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")

canvas.pack(fill=BOTH, expand=True)

# Add Image inside the Canvas
canvas.create_image(0, 0, image=bg, anchor='nw')

# creating a search box widget
token_entry = Entry(bd = 0, bg = "#25242C", highlightthickness = 0, font=('callibri 20'))

#creating functions that will add the temporary text in the search box
def on_entry_click(event):
    """function that gets called whenever entry is clicked"""
    if token_entry.get() == 'Search':
       token_entry.delete(0, "end") # delete all the text in the entry
       token_entry.insert(0, '') #Insert blank for user input
def on_focusout(event):
    if token_entry.get() == '':
        token_entry.insert(0, 'Search')

# Inserting the temporary Search text in the search box
token_entry.insert(0, "Search")
token_entry.config(fg = '#DCCAFC')
token_entry.config(insertbackground = '#DCCAFC')

# packing that widget in the tkinter windows
token_entry.place(
    x = 225, y = 218,
    width = 600.0,
    height = 30)

#configuring the search box to add the functions
token_entry.bind('<FocusIn>', on_entry_click)
token_entry.bind('<FocusOut>', on_focusout)

play_photo = PhotoImage(file = f"{images_dir}/paused.png")
download_photo = PhotoImage(file = f"{images_dir}/download.png")
search_photo = PhotoImage(file = f"{images_dir}/search.png")
next_photo = PhotoImage(file = f"{images_dir}/next.png")
previous_photo = PhotoImage(file = f"{images_dir}/previous.png")

def threading_dwl():
    t1=Thread(target=song_downloader)
    t1.start()

# def seekto(pos):
#     print("entered")
#     try:
#         Play_DLL.seek(pos)
#     except:
#         pass

def song_downloader():  
    # seekto(0.5)
    print("started")
    Dwl_Manager.start_Download(f'''{url_extracter.Extract(token_entry.get()+"song lyrics")}''')

#function to add the names of the songs to the queue
def add_to_queue(song_name):

    global queue
    queue.append(song_name)

def threading_play():
    t1=Thread(target=get_input)
    t1.start()

def threading_progress():
    tp1 = Thread(target=ProgressBar)
    tp1.start()

def threading_pause():
    global play_photo, paused

    if Play_DLL.player != "":
        if Play_DLL.paused:
            Play_DLL.paused = False
            play_photo=PhotoImage(file = f"{images_dir}/paused.png")
            print("resumed")
        else:
            Play_DLL.paused = True
            play_photo=PhotoImage(file = f"{images_dir}/playing.png")
            print("paused")
    
    else:
        pass
    
    play_button.configure(image=play_photo)
    t3=Thread(target=Play_DLL.pause_song)
    t3.start()

def set_song_name_label(song_name):
    global song_name_label

    song_name_label.configure(text = f"{song_name}")

def Reverse(lst):
    return [ele for ele in reversed(lst)]

def previous_song():
    global queue, current_song
    print(queue)
    song_queue = Reverse(queue)
    print(song_queue)
    current_song = song_queue[song_queue.index(currently_playing) - 1]
    
    set_song_name_label(pafy.new(url_extracter.Extract(current_song)).title)

    Play_DLL.play_by_songName(current_song)
    threading_progress()
    
def next_song():
    pass

def next_thread():
    nextThread = Thread(target=next_song)
    nextThread.start()

def previous_thread():
    previousThread = Thread(target=previous_song)
    previousThread.start()

# def OnTick():
#         """Timer tick, update the time slider to the video time.
#         """
#     global paused, slider, timeSliderUpdate
#     if not paused:
#             # since the self.player.get_length may change while
#             # playing, re-set the timeSlider to the correct range
#         t = Play_DLL.player.get_position() * 1e-3  # to seconds
#         if t > 0:
#             slider.config(to=t)

#             t = Play_DLL.player.get_time() * 1e-3  # to seconds
#                 # don't change slider while user is messing with it
#             if t > 0 and time.time() > (timeSliderUpdate + 2):
#                 slider.set(t)
#                 timeSliderLast = int(timeVar.get())
#         # start the 1 second timer again
#     window.after(1000, OnTick)

def everySec():
    global timeSliderUpdate, paused, timeVar, slider, timeSliderLast, length
    if not paused:
        t = length
        if t > 0:
            slider.config(to=t)
            t = Play_DLL.player.get_time() * 1e-3  # to seconds

            if t > 0 and time.time() > (timeSliderUpdate + 2):
                slider.set(t)
                timeSliderLast = int(timeVar.get())
    
    window.after(1000, everySec)
    
def get_input():
    """
    Function to get the user input from the GUI Window and play it.

    """
    global url, activity, currently_playing , SongName, song_name_label,song_duration, current_song
    
    SongName = (pafy.new(url_extracter.Extract(token_entry.get()+ "song lyrics")).title)

    currently_playing = token_entry.get()+" song lyrics"
    current_song = currently_playing
    print(SongName)
    
    song_name_label["text"] = SongName
    add_to_queue(currently_playing)
    slider.set(0)
    Play_DLL.play_by_songName(currently_playing)
    threading_progress()
    


song_name_label = Label(text=SongName, background="#25242C", foreground="white",font=("Aerial", 20))
canvas.create_window(547,300, window=song_name_label)

play_button= Button(window, image=play_photo,borderwidth=0, border=0, 
    relief="flat",command=threading_pause,width=50, height=50)
canvas.create_window(547,420,window=play_button)


def ProgressBar():
    
    global paused, close_app, length, slider, timeVar, timeSliderUpdate, timeSliderLast

    length = pafy.new(url_extracter.Extract(token_entry.get())).length

    if not paused:
        t = timeVar.get()
        if timeSliderLast != int(t):
            # this is a hack. The timer updates the time slider.
            # This change causes this rtn (the 'slider has changed' rtn)
                # to be invoked.  I can't tell the difference between when
                # the user has manually moved the slider and when the timer
                # changed the slider.  But when the user moves the slider
                # tkinter only notifies this rtn about once per second and
                # when the slider has quit moving.
                # Also, the tkinter notification value has no fractional
                # seconds.  The timer update rtn saves off the last update
                # value (rounded to integer seconds) in timeSliderLast if
                # the notification time (sval) is the same as the last saved
                # time timeSliderLast then we know that this notification is
                # due to the timer changing the slider.  Otherwise the
                # notification is due to the user changing the slider.  If
                # the user is changing the slider then I have the timer
                # routine wait for at least 2 seconds before it starts
                # updating the slider again (so the timer doesn't start
                # fighting with the user).
            Play_DLL.player.set_position(int(t * 1e3))  # milliseconds
            timeSliderUpdate = time.time()
    
    

    # for i in range(length):

    #     if not paused:
    #         try:
    #             t = Play_DLL.player.get_position() * 1e-3
    #             # slider.set(Play_DLL.player.get_position())
    #             # print(length*Play_DLL.player.get_position())
    #             if t > 0:
                    
    #                 slider.config(to=t)

    #                 t = Play_DLL.player.get_position() * 1e-3  # to seconds
    #                     # don't change slider while user is messing with it
    #                 if t > 0 and time.time() > (timeSliderUpdate + 2):
    #                     slider.set(t)
    #                     timeSliderLast = int(timeVar.get())
    #             # start the 1 second timer again
    #             window.after(1000, ProgressBar)
    #         except:
    #             pass

    #         if close_app:
    #             try:
    #                 Play_DLL.player.stop()

    #             except:
    #                 exit()
    #             exit()
                
    #         # print(i)
    #         sleep(1)
        
    #     else:
    #         while paused:

    #             for x in range(1):
    #                 sleep(1)

    #             if close_app:
    #                 Play_DLL.player.stop()
    #                 exit()

    # slider.set(1)


slider_value = DoubleVar()
timeVar = DoubleVar()
window.after(1000, everySec)
slider = customtkinter.CTkSlider(master = window, orient=HORIZONTAL, bg_color="#25242D", width=600, progress_color = "#DCCAFC")
slider.set(0)

canvas.create_window(547, 350, window=slider)


download_button= Button(window, image=download_photo,borderwidth=0, border=0, 
    command= threading_dwl,width=38, height=37)

search_button= Button(window, image=search_photo,borderwidth=0, border=0, 
    command= threading_play,width= 38, height=37)

next_button= Button(window, image=next_photo,borderwidth=0, border=0, 
    command= next_thread,width= 50, height=50)

previous_button= Button(window, image=previous_photo,borderwidth=0, border=0, 
    command= previous_thread,width= 50, height=50)


canvas.create_window(920,234,window=download_button)
canvas.create_window(857,234,window=search_button)
canvas.create_window(647,420,window=next_button)
canvas.create_window(447,420,window=previous_button)


# --------------------------------------------------------- #


#############################################################

window.mainloop()