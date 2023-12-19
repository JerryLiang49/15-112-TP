from cmu_graphics import *
from PIL import Image
from maze import maze
import time 
import copy
import os, pathlib
import random

# Check if win condition has been fulfilled
def checkGameWon(app):
    if app.pelletsEaten == 242:
        app.playChomp = False
        app.gameWon = True
        app.startGame = False
        app.pauseGame = True

# Win screen   
def winScreen(app):
    if app.gameWon:
        drawRect(0, 0, 700, 750, fill='black', opacity = 60)
        drawImage(app.pacmanWinPNG, 80, 330, align = 'center')
        drawLabel('GAME COMPLETED! :>', app.width//2, 200, size = 45, bold = True, 
                italic = True, fill='white', align='center')
        drawLabel(f'Score: ', app.width//2-50, 320, size = 55, bold = True, 
                italic = True, fill='white', align='center')
        drawLabel(str(app.score), app.width//2+50, 325, size = 55, bold = True, 
                italic = True, fill='yellow', align='left')
        drawLabel("Press space key to play", app.width//2, 440, size = 40, bold = True, 
                italic = True, fill='yellow', align='center')