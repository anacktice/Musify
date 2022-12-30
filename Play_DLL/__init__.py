"""
Plays the requested song without a console output
"""

# Importing some modules

import requests
import vlc
import pafy


# Creating some variables

player = ""
val = ""
song_names = []
currently_playing = ""
paused = False

# --------------------- All the main Functional stuff ---------------------#


# ========= All the webscraping stuff ===== #

def get_song_url(topic):

    """
    Function to find YouTube video URL of the Song requested....
    """

    url = 'https://www.youtube.com/results?q=' + topic + " song lyrics"
    print(url)
    count = 0
    cont = requests.get(url)
    data = cont.content
    data = str(data)
    lst = data.split('"')
    for i in lst:
        count += 1
        if i == 'WEB_PAGE_TYPE_WATCH':
            break
    if lst[count - 5] == "/results":
        raise Exception("No video found.")

    return "https://www.youtube.com" + lst[count - 5]


def url_extracter(song_name):
    '''
    Function to find the song url.
    '''
    global currently_playing, video, song_url

    currently_playing = song_name

    video = pafy.new(song_name).getbestaudio().url
    song_names.append(song_name)
    song_url = video
    
    return song_url



# ========= All the functions that play the song ===== #
def play_by_song_url(url):
    global player, val

    """
    Function to play song from video/song URL....
    """
    try:
       player.stop()
    except:
        pass
    
    player = vlc.MediaPlayer(url)  

    player.play()
    



def play_by_yt_url(yt_url):
    
    # Function to play song from youtube video URL

    
    play_by_song_url(url_extracter(yt_url))


def play_by_songName(song_name):

    """
    Function which will take song name as argument and then find the YouTube video url of that song;
    After that it find the video URL of the Song then plays it.....
    """

    url_of_song = get_song_url(song_name)
    play_by_yt_url(url_of_song)
 
def play_by_file(file_path):
    play_by_song_url(file_path)

# ========= All the pause, resume, rewind etc type of functions ===== #

def pause_song(): 
    '''
    Function to pause or resume the playing song.
    '''

    global player, paused
    if player != "":
        player.pause()


def next_():
    pass

def previous():
    seek(0.0)



def seek(pos):
    # here in the arguments we are supposed to give the seconds to which w have to seek. lIKE IF WE HAVE TO SEEK TO 20 SECONDS THEN WE HAVE TO GIVE 20 IN THE ARGUMENTS
    global player
    player.set_position(pos)
# ---------------------------------------------------------------------------#

# Testing Area


