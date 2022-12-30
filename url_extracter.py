import subprocess
import requests

# ------------------- EXTRACT URL FUNCTION ------------------- #

def Extract(topic):
    """Will play video on following topic, might takes about 10 to 15 seconds to load"""

    url = 'https://www.youtube.com/results?q=' + topic
    count = 0
    cont = ''
    try:
        cont = requests.get(url)
    except:
        print('Error','Cannot Connect.. Internet not connected or invalid URL or id.')
        cont = ''
    data = cont.content
    data = str(data)
    lst = data.split('"')
    for i in lst:
        count+=1
        if i == 'WEB_PAGE_TYPE_WATCH':
            break
    if lst[count-5] == "/results":
        print("Error","No video found.")
    return "https://www.youtube.com"+lst[count-5]

# ------------------------------------------------------------ #

def url_extracter(song_name):  
    """Accepts song name as input argument and returns the URL for that song"""

    song_url = str(subprocess.check_output(f'yt-dlp.exe -q -g {Extract(song_name)}')).split("\\n")
    return song_url[1]

