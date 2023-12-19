from cmu_graphics import *
from PIL import Image
from maze import maze
import time 
import copy
import os, pathlib
import random
from ghost import *
from win import *
from pacmanHelper import *

# This makes the power ups flicker using another counter variable
def flicker(app):
    app.flickerCounter += 1
    if app.flickerCounter % 2 == 0:
        app.visible = not app.visible

# Set the player's coordinates to the other side of the tunnnel if it goes through one end of the tunnel
def tunnel(app):
    if app.pacmanX >= 580:
        app.pacmanX = 0
    elif app.pacmanX <= 1:
        app.pacmanX = 580

def distance(x, y, x1, y1):
    return ((x1-x)**2 + (y1-y)**2)**0.5

# From sound demo on piazza
def loadSound(relativePath):
    absolutePath = os.path.abspath(relativePath)
    url = pathlib.Path(absolutePath).as_uri()
    return Sound(url)

# Set the timers for the different power-ups
def powerUps(app):
    if app.powerUp == True:
        powerUpcurrentTime = time.time()
        powerUpelapsedTime = powerUpcurrentTime - app.powerUpStartTime
        if powerUpelapsedTime > 10:
            app.powerUp = False
    
    if app.speedUp == True:
        speedUpcurrentTime = time.time()
        speedUpelapsedTime = speedUpcurrentTime - app.speedUpStartTime
        if speedUpelapsedTime > 8:
            app.speedUp = False
            app.pacmanSpeed = 5
        
    if app.freezeTime == True:
        freezeTimecurrentTime = time.time()
        freezeTimelapsedTime = freezeTimecurrentTime - app.freezeTimeStartTime
        if freezeTimelapsedTime > 5:
            app.freezeTime = False