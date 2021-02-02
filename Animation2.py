import os
import glob
from picamera import PiCamera
from time import sleep
from gpiozero import Button
from datetime import datetime
from signal import pause

global preview
global frame
preview = 0
frame = 1
button_cheese = Button(3)
button_stop = Button(27)
button_compile = Button(10)
camera = PiCamera()
global path
global path_search
timestamp = datetime.now().isoformat()
path = "/home/pi/Animation/" + timestamp
path_search = path + "/frame%03d.jpg"

def cheese():
    global frame
    global path
    timestamp = datetime.now().isoformat()
    camera.capture(path + "/frame%03d.jpg" % frame)
    frame += 1
    
def toggle_preview():
    global preview
    if preview == 0:
        camera.start_preview()
        preview = 1
    elif preview == 1:
        camera.stop_preview()
        preview = 0

def compile_movie():
    global path
    global path_search
    movie_name = path + "/movie.mp4"
    command = "ffmpeg -r 3 -i {ps} -c:v libx264 {movie_name:s}".format(ps=path_search, movie_name=movie_name)
    try:
        os.system(command)
    except OSError:
        print ("Failed to create movie file.")
    else:
        print ("Movie file created!")

try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s failed..." % path)
else:
    print ("Successfully created the directory %s " % path)

button_cheese.when_pressed = cheese
button_stop.when_pressed = toggle_preview
button_compile.when_pressed = compile_movie

pause()