from cmu_graphics import *
from PIL import Image
from maze import maze
import time 
import copy
import os, pathlib
import random
from ghost import *
from win import *
from helper import *

# Draw pacman in different orientations depending on what direction it's moving in
def drawPacman(app):
    if app.direction == 'right':
        drawImage(app.spriteListR[app.spriteCounter], app.pacmanX, app.pacmanY, 
                align = 'center')
    elif app.direction == 'up':
        drawImage(app.spriteListU[app.spriteCounter], app.pacmanX, app.pacmanY, 
                align = 'center')
    elif app.direction == 'down':
        drawImage(app.spriteListD[app.spriteCounter], app.pacmanX, app.pacmanY, 
                align = 'center')
    elif app.direction == 'left':
        drawImage(app.spriteListL[app.spriteCounter], app.pacmanX, app.pacmanY, 
                align = 'center')

# Moves pacman in desired direction
def movePacman(app): 
    if app.startGame:
        if app.direction == 'right' and app.dirsDict['right']:
            app.pacmanX += app.pacmanSpeed
        elif app.direction == 'left' and app.dirsDict['left']:
            app.pacmanX -= app.pacmanSpeed
        elif app.direction == 'up' and app.dirsDict['up']:
            app.pacmanY -= app.pacmanSpeed
        elif app.direction == 'down' and app.dirsDict['down']:
            app.pacmanY += app.pacmanSpeed

# If pacman is at the 5th pixel of a tile and the speed changes to 10, its coordinate will
# alternate between 5 and 15, and the pacmanCanTurn will not be True and pacman will be unable to turn
# To account for this, this function will subtract 5 whenever it's at the 5th or 10th pixel in either the x or y direction.
def checkPacmanCenter(app):
    if app.pacmanSpeed == 10:
        if app.pacmanX % app.tileWidth == 5 or app.pacmanX % app.tileWidth == 15:
            app.pacmanX -= 5
        if app.pacmanY % app.tileHeight == 5 or app.pacmanY % app.tileHeight == 15:
            app.pacmanY -= 5

# Turns tiles with pellets to empty tiles when pacman "eats" the pellets.
# Keeps track of score involving pellets and power ups and number of pellets and power ups "eaten".
def pacmanEat(app):
    if app.pacmanX > 0 and app.pacmanX < 580:
        currRow, currCol = app.pacmanY//app.tileHeight, app.pacmanX//app.tileWidth
        if app.maze[currRow][currCol] == 'p':
            app.maze[currRow][currCol] = 'e'
            app.pelletsEaten += 1
            app.score += 10
        elif app.maze[currRow][currCol] == 'pUP':
            app.maze[currRow][currCol] = 'e'
            app.powerUp = True
            app.eatPowerUP.play()
            app.pelletsEaten += 1
            app.score += 50 
            app.powerUpStartTime = time.time()
        elif app.maze[currRow][currCol] == 'speedUp':
            app.maze[currRow][currCol] = 'e'
            app.speedUp = True
            app.pacmanSpeed = 10
            app.speedUpMP3.play()
            app.pelletsEaten += 1
            app.score += 20
            app.speedUpStartTime = time.time()
        elif app.maze[currRow][currCol] == 'freezeTime':
            app.maze[currRow][currCol] = 'e'
            app.freezeTime = True
            app.freezeTimeMP3.play()
            app.pelletsEaten += 1
            app.score += 20
            app.freezeTimeStartTime = time.time()

# Checks whether the player can make a specific turn in the maze
# Turning algorithm motivated by https://www.youtube.com/watch?v=9H27CimgPsQ&ab_channel=LeMasterTech
def pacmanCanTurn(app):
    # Can move if tile is empty, a pellet, or any power up
    canMove = {'e','p','pUP','speedUp','freezeTime'} 
    app.dirsDict = {'right':False, 'left':False, 'up':False, 'down':False}
    currRow, currCol = app.pacmanY // app.tileHeight, app.pacmanX // app.tileWidth 
    leftCol, rightCol = (app.pacmanX - app.edgeWidth) // app.tileWidth, (app.pacmanX + app.edgeWidth) // app.tileWidth
    upRow, downRow = (app.pacmanY - app.edgeWidth) // app.tileHeight, (app.pacmanY + app.edgeWidth) // app.tileHeight

    if app.pacmanX > 700 or app.pacmanX < -1:
        # If the player is in the tunnel, it can move in the right or left direction
        app.dirsDict['right'] = True
        app.dirsDict['left'] = True
    else:
        # Checks if the player is able to turn back and go the way it came from
        if app.direction == 'right':
            if app.maze[currRow][leftCol] in canMove:
                app.dirsDict['left'] = True
        if app.direction == 'left':
            if app.maze[currRow][rightCol] in canMove:
                app.dirsDict['right'] = True
        if app.direction == 'up':
            if app.maze[downRow][currCol] in canMove:
                app.dirsDict['down'] = True
        if app.direction == 'down':
            if app.maze[upRow][currCol] in canMove:
                app.dirsDict['up'] = True    
            
        # Checks if the player is able to turn when it's moving in the up or down direction
        if app.direction == 'up' or app.direction == 'down':
            # 30x30 board with 20x20 tiles
            # This allows the player to turn up or down only when its x coordinate is around the center of a tile
            if app.pacmanX % app.tileWidth - 10 % 20 == 0:
                # These numbers are so that the player can only turn up or down when its x coordinates are around the center of a tile
                if app.maze[upRow][currCol] in canMove:
                    app.dirsDict['up'] = True
                if app.maze[downRow][currCol] in canMove:
                    app.dirsDict['down'] = True
            # This allows the player to turn right or left only when its y coordinate is around the center of a tile
            if app.pacmanY % app.tileHeight - 10 % 20 == 0:
                if app.maze[currRow][currCol+1] in canMove:
                    app.dirsDict['right'] = True
                if app.maze[currRow][currCol-1] in canMove:
                    app.dirsDict['left'] = True 

        # Checks if the player is able to turn when it's moving in the right or left direction
        if app.direction == 'right' or app.direction == 'left':
            # This allows the ghost to turn right or left only when its y coordinate is around the center of a tile
            if app.pacmanY % app.tileHeight - 10 % 20 == 0:             
                if app.maze[currRow][rightCol] in canMove:
                    app.dirsDict['right'] = True
                if app.maze[currRow][leftCol] in canMove:
                    app.dirsDict['left'] = True 
            # This allows the ghost to turn up or down only when its x coordinate is around the center of a tile
            if app.pacmanX % app.tileWidth - 10 % 20 == 0:
                if app.maze[currRow-1][currCol] in canMove:
                    app.dirsDict['up'] = True
                if app.maze[currRow+1][currCol] in canMove:
                    app.dirsDict['down'] = True

# Checks the direction of the lasy key pressed and whether we can move in that direction
# If we can, set direction to the direction of the last key pressed (currDirection)
# If we cannot, keep going in the direction we are currently going 
def joystickMovement(app):
    if app.direction != app.currDirection and app.dirsDict[app.currDirection] == False:
        app.direction = app.direction
    else:
        app.direction = app.currDirection
    if app.currDirection == 'right' and app.dirsDict['right']:
        app.direction = 'right'
    if app.currDirection == 'left' and app.dirsDict['left']:
        app.direction = 'left'
    if app.currDirection == 'up' and app.dirsDict['up']:
        app.direction = 'up'
    if app.currDirection == 'down' and app.dirsDict['down']:
        app.direction = 'down' 