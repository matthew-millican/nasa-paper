#! /usr/bin/env python3
import appscript
import requests
import os
import subprocess
import wget
import ast

# Fill with your own API key
NASA_API_KEY = "api-key"
NASA_PHOTO_OF_THE_DAY = "https://api.nasa.gov/planetary/apod?api_key=" + NASA_API_KEY

# https://stackoverflow.com/questions/431205/how-can-i-programmatically-change-the-background-in-mac-os-x
def set_wallpaper(filename):
    se = appscript.app('System Events')
    desktops = se.desktops.display_name.get()
    for d in desktops:
        desk = se.desktops[appscript.its.display_name == d]
        desk.picture.set(appscript.mactypes.File(filename))
        subprocess.call(['/usr/bin/killall', 'Dock'])

def nasa_photo_of_the_day():

    r = requests.get(NASA_PHOTO_OF_THE_DAY)
    # Make sure we got the data
    if r.ok:
        data = ast.literal_eval(r.content.decode('utf-8'))
        print(data['url'])
        filename = wget.download(data['url'])
        print()
        print("Title: " + data['title'])
        print("Explanation: " + data['explanation'])
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Only remove file if we have downloaded a picture. Sometimes nasa posts youtube links
            for file in os.listdir(os.getcwd()):
                if file.endswith('.jpg'):
                    os.remove(file)
                    set_wallpaper(filename)


nasa_photo_of_the_day()

    
