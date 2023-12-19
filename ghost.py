from cmu_graphics import *
from PIL import Image
from maze import maze
import time 
import copy
import os, pathlib
import random
from win import *
from helper import *
from pacmanHelper import *

# Implemented OOP 
class Ghost:    

    def __init__(self, app, x, y, speed, picture, direction, dead, cage, targetList):
        self.x = x
        self.y = y
        self.app = app
        self.speed = speed
        self.picture = picture
        self.direction = direction
        self.dead = dead
        self.inCage = cage
        self.targetList = targetList
        self.dirsDict = {'right':False, 'left':False, 'up':False, 'down':False}

    # Draw the ghost in different states depending on the conditions of the game
    # The three states are: Normal, vulnerable, and dead
    def drawGhostState(self):
        if self.app.powerUp and self.dead == False and self.inCage == False:
            drawImage(self.app.vulnerableGhostIMG, self.x, self.y, align='center')
        elif self.dead and self.inCage == False:
            drawImage(self.app.ghostEyesIMG, self.x, self.y, align='center')
        else:
            drawImage(self.picture, self.x, self.y, align='center')

    # Check whether the ghost can make a specific turn in the maze
    # Similar to the player's canTurn algorithm
    # Turning algorithm motivated by https://www.youtube.com/watch?v=9H27CimgPsQ&ab_channel=LeMasterTech
    def ghostCanTurn(self, app): 
        canMove = {'e','p','pUP','speedUp','freezeTime'} # The ghost can move if tile is empty, a pellet, or any power
        self.dirsDict = {'right':False, 'left':False, 'up':False, 'down':False}
        currRow, currCol = self.y // self.app.tileHeight, self.x // self.app.tileWidth 
        leftCol, rightCol = (self.x - self.app.edgeWidth) // self.app.tileWidth, (self.x + self.app.edgeWidth) // self.app.tileWidth
        upRow, downRow = (self.y - self.app.edgeWidth) // self.app.tileHeight, (self.y + self.app.edgeWidth) // self.app.tileHeight
        
        if self.x > 700 or self.x < -1:
            # If the ghost is in the tunnel, it can move in the right or left direction
            self.dirsDict['right'] = True
            self.dirsDict['left'] = True
        else:
            # For ghosts trying to get out of the ghost cage, they can move in the up direction
            if maze[upRow][currCol] == 'gD':
                self.dirsDict['up'] = True
            # Check if ghost is able to turn back and go the way it came from
            if self.direction == 'right':
                if app.maze[currRow][leftCol] in canMove or (app.maze[currRow][leftCol] == 'gD' and (self.inCage or self.dead)):
                    self.dirsDict['left'] = True
            if self.direction == 'left':
                if app.maze[currRow][rightCol] in canMove or (app.maze[currRow][rightCol] == 'gD' and (self.inCage or self.dead)):
                    self.dirsDict['right'] = True
            if self.direction == 'up':
                if app.maze[downRow][currCol] in canMove or (app.maze[downRow][currCol] == 'gD' and (self.inCage or self.dead)):
                    self.dirsDict['down'] = True
            if self.direction == 'down':
                if app.maze[upRow][currCol] in canMove or (app.maze[upRow][currCol] == 'gD' and (self.inCage or self.dead)):
                    self.dirsDict['up'] = True
                
            # Check if ghost is able to turn when it's moving in the up or down direction
            if self.direction == 'up' or self.direction == 'down':
                # 30x30 board with 20x20 tiles
                # This allows the ghost to turn up or down only when its x coordinate is around the center of a tile
                if (self.x % self.app.tileWidth - 10 % 20 == 0 or 
                    (abs(self.x-300) <= 5 and abs(self.y - 300)<=5) or
                    (abs(self.x-260) <= 5 and abs(self.y - 300)<=5) or
                    (abs(self.x-340) <= 5 and abs(self.y - 300)<=5)):
                    if app.maze[upRow][currCol] in canMove or (app.maze[upRow][currCol] == 'gD' and (self.inCage or self.dead)):
                        self.dirsDict['up'] = True
                    if app.maze[downRow][currCol] in canMove or (app.maze[downRow][currCol] == 'gD' and (self.inCage or self.dead)):
                        self.dirsDict['down'] = True
                # This allows the ghost to turn right or left only when its y coordinate is around the center of a tile
                if self.y % self.app.tileHeight - 10 % 20 == 0:
                    if app.maze[currRow][currCol+1] in canMove or (app.maze[currRow][currCol+1] == 'gD' and (self.inCage or self.dead)):
                        self.dirsDict['right'] = True
                    if app.maze[currRow][currCol-1] in canMove or (app.maze[currRow][currCol-1] == 'gD' and (self.inCage or self.dead)):
                        self.dirsDict['left'] = True 

            # Checks if ghost is able to turn when it's moving in the right or left direction
            if self.direction == 'right' or self.direction == 'left':
                if self.y % self.app.tileHeight - 10 % 20 == 0:
                # This allows the ghost to turn right or left only when its y coordinate is around the center of a tile
                    if app.maze[currRow][rightCol] in canMove or (app.maze[currRow][rightCol] == 'gD' and (self.inCage or self.dead)):
                        self.dirsDict['right'] = True
                    if app.maze[currRow][leftCol] in canMove or (app.maze[currRow][leftCol] == 'gD' and (self.inCage or self.dead)):
                        self.dirsDict['left'] = True
                if self.x % self.app.tileWidth - 10 % 20 == 0:
                # This allows the ghost to turn up or down only when its x coordinate is around the center of a tile
                    if app.maze[currRow-1][currCol] in canMove or (app.maze[currRow-1][currCol] == 'gD' and (self.inCage or self.dead)):
                        self.dirsDict['up'] = True
                    if app.maze[currRow+1][currCol] in canMove or (app.maze[currRow+1][currCol] == 'gD' and (self.inCage or self.dead)):
                        self.dirsDict['down'] = True

        # The ghost is in the cage if it's within the following coordinates
        if self.x > 240 and self.x < 360 and self.y > 265 and self.y < 340:
            self.inCage = True
        else:
            self.inCage = False

    # If the ghost is at the 5th pixel of a tile and the speed changes to 10, its coordinate will
    # alternate between 5 and 15, and the ghostCanTurn function will not be True and the ghost will be unable to turn.
    # To account for this, I subtract 5 whenever it's at the 5th or 10th pixel in either the x or y direction.
    def checkGhostCenter(self):
        if self.speed == 10:
            if self.x % self.app.tileWidth == 5 or self.x % self.app.tileWidth == 15:
                self.x -= 5
            if self.y % self.app.tileHeight == 5 or self.y % self.app.tileHeight == 15:
                self.y -= 5

    # Ghosts can have different targets: (cage, player, away from the player, ...)
    # This function updates the target for the ghost
    def getTargetList(self):
        self.targetList = [self.app.pacmanX, self.app.pacmanY]
        cageCoors = [300, 300]
        fleeCoors = [300, 220]
        if self.app.powerUp:
            if self.dead:
                self.targetList = cageCoors
            else:
                self.targetList = fleeCoors
        else:
            if self.dead:
                self.targetList = cageCoors
            elif self.dead == False and self.inCage:
                self.targetList = [300,100]
            elif self.dead == False and self.inCage == False:
                self.targetList = [self.app.pacmanX, self.app.pacmanY]

    # The pathfinding algorithm for the red ghost tries to get itself closer to pacman
    def redGhostPathfinding(self):
        if self.app.startGame:
            # This prevents the ghost from going through the tunnel over and over again if the 
            # player is to the right or to the left of the ghost.
            if self.x == 450 and self.y == 310:
                self.dirsDict['right'] = False
            if self.x == 150 and self.y == 310:
                self.dirsDict['left'] = False

            # The best move is to move right when pacman is to the right and the ghost is allowed to move right
            if self.direction == 'right':
                if self.dirsDict['right'] and self.targetList[0] > self.x:
                    self.x += self.speed
                    self.direction = 'right'
                # Ghost cannot make the best case move, so it makes logical moves that will get the ghost closer to pacman
                elif self.dirsDict['right'] == False:
                    if self.dirsDict['down'] and self.targetList[1] > self.y:
                        self.direction = 'down'
                        self.y += self.speed
                    elif self.dirsDict['up'] and self.targetList[1] < self.y:
                        self.direction = 'up'
                        self.y -= self.speed
                    elif self.dirsDict['left'] and self.targetList[0] < self.x:
                        self.direction = 'left'
                        self.x -= self.speed
                    # Ghost cannot make moves that's advantangeous, so it moves in any other possible direction
                    elif self.dirsDict['down']:
                        self.direction = 'down'
                        self.y += self.speed
                    elif self.dirsDict['up']:
                        self.direction = 'up'
                        self.y -= self.speed
                    elif self.dirsDict['left']:
                        self.direction = 'left'
                        self.x -= self.speed
                # Ghost can move right, but pacman is not to the right, so it moves up or down
                elif self.dirsDict['right']:
                    if self.dirsDict['down'] and self.targetList[1] > self.y:
                        self.direction = 'down'
                        self.y += self.speed
                    elif self.dirsDict['up'] and self.targetList[1] < self.y:
                        self.direction = 'up'
                        self.y -= self.speed
                    else:
                        self.x += self.speed

            # The best move is to move left when pacman is to the left and the ghost is allowed to move left
            elif self.direction == 'left':
                # We try the down direction first so the ghost doesn't get stuck in a loop
                if self.dirsDict['down'] and self.targetList[1] > self.y:
                    self.direction = 'down'
                elif self.dirsDict['left'] and self.targetList[0] < self.x:
                    self.x -= self.speed
                    self.direction = 'left'
                # Ghost cannot make the best case moves, so it makes logical moves that will get the ghost closer to pacman
                elif self.dirsDict['left'] == False:
                    if self.dirsDict['down'] and self.targetList[1] > self.y:
                        self.direction = 'down'
                        self.y += self.speed
                    elif self.dirsDict['up'] and self.targetList[1] < self.y:
                        self.direction = 'up'
                        self.y -= self.speed
                    elif self.dirsDict['right'] and self.targetList[0] > self.x:
                        self.direction = 'right'
                        self.x += self.speed
                    # Ghost cannot make moves that's advantangeous, so it moves in any other possible direction
                    elif self.dirsDict['down']:
                        self.direction = 'down'
                        self.y += self.speed
                    elif self.dirsDict['up']:
                        self.direction = 'up'
                        self.y -= self.speed
                    elif self.dirsDict['right']:
                        self.direction = 'right'
                        self.x += self.speed
                # Ghost can move left, but pacman is not to the left, so it moves up or down
                elif self.dirsDict['left']:
                    if self.dirsDict['down'] and self.targetList[1] > self.y:
                        self.direction = 'down'
                        self.y += self.speed
                    elif self.dirsDict['up'] and self.targetList[1] < self.y:
                        self.direction = 'up'
                        self.y -= self.speed
                    else:
                        self.x -= self.speed

            # The best move is to move up when pacman is above the ghost and the ghost is allowed to move up
            elif self.direction == 'up':
                # We try the left direction first so the ghost doesn't get stuck in a loop
                if self.dirsDict['left'] and self.targetList[0] < self.x:
                    self.direction = 'left'
                    self.x -= self.speed        
                elif self.dirsDict['up'] and self.targetList[1] < self.y:
                    self.direction = 'up'
                    self.y -= self.speed
                # Ghost cannot make the best case moves, so it makes logical moves that will get the ghost closer to pacman
                elif self.dirsDict['up'] == False:
                    if self.dirsDict['right'] and self.targetList[0] > self.x:
                        self.direction = 'right'
                        self.x += self.speed
                    elif self.dirsDict['left'] and self.targetList[0] < self.x:
                        self.direction = 'left'
                        self.x -= self.speed 
                    elif self.dirsDict['down'] and self.targetList[1] > self.y:
                        self.direction = 'down'
                        self.y += self.speed
                    # Ghost cannot make moves that's advantangeous, so it moves in any other possible direction
                    elif self.dirsDict['left']:
                        self.direction = 'left'
                        self.x -= self.speed
                    elif self.dirsDict['down']:
                        self.direction = 'down'
                        self.y += self.speed
                    elif self.dirsDict['right']:
                        self.direction = 'right'
                        self.x += self.speed
                # Ghost can move up, but pacman is not above the ghost, so it moves right or left
                elif self.dirsDict['up']:
                    if self.dirsDict['right'] and self.targetList[0] > self.x:
                        self.direction = 'right'
                        self.x += self.speed      
                    elif self.dirsDict['left'] and self.targetList[0] < self.x:
                        self.direction = 'left'
                        self.x -= self.speed
                    else:
                        self.y -= self.speed

            # The best move is to move down when pacman is below the ghost and the ghost is allowed to move down
            elif self.direction == 'down':
                if self.dirsDict['down'] and self.targetList[1] > self.y:
                    self.y += self.speed
                # Ghost cannot make the best case moves, so it makes logical moves that will get the ghost closer to pacman
                elif self.dirsDict['down'] == False:
                    if self.dirsDict['right'] and self.targetList[0] > self.x:
                        self.direction = 'right'
                        self.x += self.speed
                    elif self.dirsDict['left'] and self.targetList[0] < self.x:
                        self.direction = 'left'
                        self.x -= self.speed
                    elif self.dirsDict['up'] and self.targetList[1] < self.y:
                        self.direction = 'up'
                        self.y -= self.speed
                    # Ghost cannot make moves that's advantangeous, so it moves in any other possible direction
                    elif self.dirsDict['up']:
                        self.direction = 'up'
                        self.y -= self.speed
                    elif self.dirsDict['left']:
                        self.direction = 'left'
                        self.x -= self.speed
                    elif self.dirsDict['right']:
                        self.direction = 'right'
                        self.x += self.speed
                # Ghost can move down, but pacman is not below the ghost, so it moves right or left
                elif self.dirsDict['down']:
                    if self.dirsDict['right'] and self.targetList[0] > self.x:
                        self.direction = 'right'
                        self.x += self.speed 
                    elif self.dirsDict['left'] and self.targetList[0] < self.x:
                        self.direction = 'left'
                        self.x -= self.speed
                    else:
                        self.y += self.speed    

        # Handles ghost position if it goes though the tunnel    
        if self.x >= 580:
            self.x = 0
        elif self.x <= 1:
            self.x = 580 

    # The pathfinding algorithm for the blue ghost is different from the red ghost's in that
    # it involves some randomness. It doesn't always move in the most optimal direction
    def blueGhostPathfinding(self):
        if self.app.startGame:
            if self.x == 450 and self.y == 310:
                self.dirsDict['right'] = False
            if self.x == 150 and self.y == 310:
                self.dirsDict['left'] = False
            
            # When the ghost is trying to go back to the cage get out of the cage,
            # we will still use the red ghost's pathfinding algorithm.
            if self.inCage or self.dead:
                self.redGhostPathfinding()
            # Now we implement the randomness
            else:
                randomN = random.randint(0,10)
                # The best move is to move right when pacman is to the right and the ghost is allowed to move right
                if self.direction == 'right':
                    if self.dirsDict['right'] and self.targetList[0] > self.x:
                        self.x += self.speed
                        self.direction = 'right'
                    # Ghost cannot make the best case move, so it makes logical moves that will get the ghost closer to pacman
                    elif self.dirsDict['right'] == False:
                        if self.dirsDict['down'] and self.targetList[1] > self.y:
                            self.direction = 'down'
                            self.y += self.speed
                        elif self.dirsDict['up'] and self.targetList[1] < self.y:
                            self.direction = 'up'
                            self.y -= self.speed
                        elif self.dirsDict['left'] and self.targetList[0] < self.x:
                            self.direction = 'left'
                            self.x -= self.speed
                        # Ghost cannot make moves that's advantangeous, so it moves in a direction depending on the random number
                        elif self.dirsDict['down'] and randomN > 2:
                            self.direction = 'down'
                            self.y += self.speed
                        elif self.dirsDict['up'] and randomN < 2:
                            self.direction = 'up'
                            self.y -= self.speed
                        else:
                            self.direction = 'left'
                            self.x -= self.speed
                    # Ghost can move right, but pacman is not to the right, so it moves in a direction depending on the random number
                    elif self.dirsDict['right']:
                        if self.dirsDict['down'] and randomN < 2:
                            self.direction = 'down'
                            self.y += self.speed
                        elif self.dirsDict['up'] and randomN > 3:
                            self.direction = 'up'
                            self.y -= self.speed
                        else:
                            self.x += self.speed

                # The best move is to move left when pacman is to the left and the ghost is allowed to move left
                elif self.direction == 'left':
                    if self.dirsDict['left'] and self.targetList[0] < self.x:
                        self.x -= self.speed
                        self.direction = 'left'
                    # Ghost cannot make the best case move, so it makes logical moves that will get the ghost closer to pacman
                    elif self.dirsDict['left'] == False:
                        if self.dirsDict['down'] and self.targetList[1] > self.y:
                            self.direction = 'down'
                            self.y += self.speed
                        elif self.dirsDict['up'] and self.targetList[1] < self.y:
                            self.direction = 'up'
                            self.y -= self.speed
                        elif self.dirsDict['right'] and self.targetList[0] > self.x:
                            self.direction = 'right'
                            self.x += self.speed
                        # Ghost cannot make moves that's advantangeous, so it moves in a direction depending on the random number
                        elif self.dirsDict['down'] and randomN < 3:
                            self.direction = 'down'
                            self.y += self.speed
                        elif self.dirsDict['up'] and randomN > 5:
                            self.direction = 'up'
                            self.y -= self.speed
                        else:
                            self.direction = 'right'
                            self.x += self.speed
                    # Ghost can move left, but pacman is not to the left, so it moves in a direction depending on the random number
                    elif self.dirsDict['left']:
                        if self.dirsDict['down'] and randomN > 6:
                            self.direction = 'down'
                            self.y += self.speed
                        elif self.dirsDict['up'] and randomN < 3:
                            self.direction = 'up'
                            self.y -= self.speed
                        else:
                            self.x -= self.speed

                # The best move is to move up when pacman is above the ghost and the ghost is allowed to move up
                elif self.direction == 'up':     
                    if self.dirsDict['up'] and self.targetList[1] < self.y:
                        self.direction = 'up'
                        self.y -= self.speed
                    # Ghost cannot make the best case move, so it makes logical moves that will get the ghost closer to pacman
                    elif self.dirsDict['up'] == False:
                        if self.dirsDict['right'] and self.targetList[0] > self.x:
                            self.direction = 'right'
                            self.x += self.speed
                        elif self.dirsDict['left'] and self.targetList[0] < self.x:
                            self.direction = 'left'
                            self.x -= self.speed 
                        elif self.dirsDict['down'] and self.targetList[1] > self.y:
                            self.direction = 'down'
                            self.y += self.speed
                        # Ghost cannot make moves that's advantangeous, so it moves in a direction depending on the random number
                        elif self.dirsDict['left'] and randomN < 2:
                            self.direction = 'left'
                            self.x -= self.speed
                        elif self.dirsDict['down'] and randomN > 2:
                            self.direction = 'down'
                            self.y += self.speed
                        else:
                            self.direction = 'right'
                            self.x += self.speed     
                    # Ghost can move up, but pacman is not above the ghost, so it moves in a direction depending on the random number    
                    elif self.dirsDict['up']:
                        if self.dirsDict['right'] and randomN < 2:
                            self.direction = 'right'
                            self.x += self.speed      
                        elif self.dirsDict['left'] and randomN > 4:
                            self.direction = 'left'
                            self.x -= self.speed
                        else:
                            self.y -= self.speed

                # The best move is to move down when pacman is below the ghost and the ghost is allowed to move down                    
                elif self.direction == 'down':
                    if self.dirsDict['down'] and self.targetList[1] > self.y:
                        self.y += self.speed
                    # Ghost cannot make the best case move, so it makes logical moves that will get the ghost closer to pacman
                    elif self.dirsDict['down'] == False:
                        if self.dirsDict['right'] and self.targetList[0] > self.x:
                            self.direction = 'right'
                            self.x += self.speed
                        elif self.dirsDict['left'] and self.targetList[0] < self.x:
                            self.direction = 'left'
                            self.x -= self.speed
                        elif self.dirsDict['up'] and self.targetList[1] < self.y:
                            self.direction = 'up'
                            self.y -= self.speed
                        # Ghost cannot make moves that's advantangeous, so it moves in a direction depending on the random number
                        elif self.dirsDict['up'] and randomN > 8:
                            self.direction = 'up'
                            self.y -= self.speed
                        elif self.dirsDict['left'] and randomN < 8:
                            self.direction = 'left'
                            self.x -= self.speed
                        else:
                            self.direction = 'right'
                            self.x += self.speed
                    # Ghost can move down, but pacman is not below the ghost, so it moves in a direction depending on the random number
                    elif self.dirsDict['down']:
                        if self.dirsDict['right'] and randomN > 5:
                            self.direction = 'right'
                            self.x += self.speed 
                        elif self.dirsDict['left'] and randomN < 5:
                            self.direction = 'left'
                            self.x -= self.speed
                        else:
                            self.y += self.speed       
        
        # Handles ghost position if it goes though the tunnel    
        if self.x >= 580:
            self.x = 0
        elif self.x <= 1:
            self.x = 580 

    # The pathfinding algorithm for the pink ghost is different in that it doesn't search for pacman's position.
    # Instead, it searches a few tiles infront of Pacman depending on what direction Pacman is heading
    def pinkGhostPathfinding(self, app):
        predictedTarget = [self.targetList[0], self.targetList[1]]
        if self.app.startGame:
            if self.x == 450 and self.y == 310:
                self.dirsDict['right'] = False
            if self.x == 150 and self.y == 310:
                self.dirsDict['left'] = False

            # When the ghost is trying to go back to the cage get out of the cage or flee from the player,
            # we will still use the red ghost's pathfinding algorithm.
            if self.inCage or self.dead or app.powerUp:
                self.redGhostPathfinding()
            else:
                # This changes the target for the pink ghost depending on Pacman's direction
                if self.targetList[0] != None and self.targetList[1] != None:
                    if app.direction == 'right':
                        predictedTarget[0] = self.targetList[0] + 150
                    if app.direction == 'left':
                        predictedTarget[0] = self.targetList[0] - 150
                    if app.direction == 'up':
                        predictedTarget[1] = self.targetList[1] - 150
                    if app.direction == 'down':
                        predictedTarget[1] = self.targetList[1] + 150
                # Below is similar to the red ghost's pathfinding algorithm except that its target is now different
                if self.direction == 'right':
                    if self.dirsDict['right'] and predictedTarget[0] > self.x:
                        self.x += self.speed
                        self.direction = 'right'
                    elif self.dirsDict['right'] == False:
                        if self.dirsDict['down'] and predictedTarget[1] > self.y:
                            self.direction = 'down'
                            self.y += self.speed
                        elif self.dirsDict['up'] and predictedTarget[1] < self.y:
                            self.direction = 'up'
                            self.y -= self.speed
                        elif self.dirsDict['left'] and predictedTarget[0] < self.x:
                            self.direction = 'left'
                            self.x -= self.speed
                        elif self.dirsDict['down']:
                            self.direction = 'down'
                            self.y += self.speed
                        elif self.dirsDict['up']:
                            self.direction = 'up'
                            self.y -= self.speed
                        elif self.dirsDict['left']:
                            self.direction = 'left'
                            self.x -= self.speed
                    elif self.dirsDict['right']:
                        if self.dirsDict['down'] and predictedTarget[1] > self.y:
                            self.direction = 'down'
                            self.y += self.speed
                        elif self.dirsDict['up'] and predictedTarget[1] < self.y:
                            self.direction = 'up'
                            self.y -= self.speed
                        else:
                            self.x += self.speed

                elif self.direction == 'left':
                    if self.dirsDict['down'] and predictedTarget[1] > self.y:
                        self.direction = 'down'
                    elif self.dirsDict['left'] and predictedTarget[0] < self.x:
                        self.x -= self.speed
                        self.direction = 'left'
                    elif self.dirsDict['left'] == False:
                        if self.dirsDict['down'] and predictedTarget[1] > self.y:
                            self.direction = 'down'
                            self.y += self.speed
                        elif self.dirsDict['up'] and predictedTarget[1] < self.y:
                            self.direction = 'up'
                            self.y -= self.speed
                        elif self.dirsDict['right'] and predictedTarget[0] > self.x:
                            self.direction = 'right'
                            self.x += self.speed
                        elif self.dirsDict['down']:
                            self.direction = 'down'
                            self.y += self.speed
                        elif self.dirsDict['up']:
                            self.direction = 'up'
                            self.y -= self.speed
                        elif self.dirsDict['right']:
                            self.direction = 'right'
                            self.x += self.speed
                    elif self.dirsDict['left']:
                        if self.dirsDict['down'] and predictedTarget[1] > self.y:
                            self.direction = 'down'
                            self.y += self.speed
                        elif self.dirsDict['up'] and predictedTarget[1] < self.y:
                            self.direction = 'up'
                            self.y -= self.speed
                        else:
                            self.x -= self.speed

                elif self.direction == 'up':
                    if self.dirsDict['left'] and predictedTarget[0] < self.x:
                        self.direction = 'left'
                        self.x -= self.speed        
                    elif self.dirsDict['up'] and predictedTarget[1] < self.y:
                        self.direction = 'up'
                        self.y -= self.speed
                    elif self.dirsDict['up'] == False:
                        if self.dirsDict['right'] and predictedTarget[0] > self.x:
                            self.direction = 'right'
                            self.x += self.speed
                        elif self.dirsDict['left'] and predictedTarget[0] < self.x:
                            self.direction = 'left'
                            self.x -= self.speed 
                        elif self.dirsDict['down'] and predictedTarget[1] > self.y:
                            self.direction = 'down'
                            self.y += self.speed
                        elif self.dirsDict['left']:
                            self.direction = 'left'
                            self.x -= self.speed
                        elif self.dirsDict['down']:
                            self.direction = 'down'
                            self.y += self.speed
                        elif self.dirsDict['right']:
                            self.direction = 'right'
                            self.x += self.speed                            
                    elif self.dirsDict['up']:
                        if self.dirsDict['right'] and predictedTarget[0] > self.x:
                            self.direction = 'right'
                            self.x += self.speed      
                        elif self.dirsDict['left'] and predictedTarget[0] < self.x:
                            self.direction = 'left'
                            self.x -= self.speed
                        else:
                            self.y -= self.speed

                elif self.direction == 'down':
                    if self.dirsDict['right'] and predictedTarget[0] > self.x:
                            self.direction = 'right'
                            self.x += self.speed
                    elif self.dirsDict['down'] and predictedTarget[1] > self.y:
                        self.y += self.speed
                    elif self.dirsDict['down'] == False:
                        if self.dirsDict['right'] and predictedTarget[0] > self.x:
                            self.direction = 'right'
                            self.x += self.speed
                        elif self.dirsDict['left'] and predictedTarget[0] < self.x:
                            self.direction = 'left'
                            self.x -= self.speed
                        elif self.dirsDict['up'] and predictedTarget[1] < self.y:
                            self.direction = 'up'
                            self.y -= self.speed
                        elif self.dirsDict['up']:
                            self.direction = 'up'
                            self.y -= self.speed
                        elif self.dirsDict['left']:
                            self.direction = 'left'
                            self.x -= self.speed
                        elif self.dirsDict['right']:
                            self.direction = 'right'
                            self.x += self.speed
                    elif self.dirsDict['down']:
                        if self.dirsDict['right'] and predictedTarget[0] > self.x:
                            self.direction = 'right'
                            self.x += self.speed 
                        elif self.dirsDict['left'] and predictedTarget[0] < self.x:
                            self.direction = 'left'
                            self.x -= self.speed
                        else:
                            self.y += self.speed    

        #Handles ghost position if it goes though the tunnel    
        if self.x >= 580:
            self.x = 0
        elif self.x <= 1:
            self.x = 580 

    # The pathfinding algorithm for the orange ghost is similar to the red ghost's, with the only difference
    # being which direction it prioritizes depending on which direction it currently is heading. 
    def orangeGhostPathfinding(self, app):
        if self.app.startGame:
            if self.x == 450 and self.y == 310:
                self.dirsDict['right'] = False
            if self.x == 150 and self.y == 310:
                self.dirsDict['left'] = False
            if self.direction == 'right':
                if self.dirsDict['right'] and self.targetList[0] > self.x:
                    self.x += self.speed
                    self.direction = 'right'
                elif self.dirsDict['right'] == False:
                    if self.dirsDict['up'] and self.targetList[1] < self.y:
                        self.direction = 'up'
                        self.y -= self.speed
                    elif self.dirsDict['down'] and self.targetList[1] > self.y:
                        self.direction = 'down'
                        self.y += self.speed
                    elif self.dirsDict['left'] and self.targetList[0] < self.x:
                        self.direction = 'left'
                        self.x -= self.speed
                    elif self.dirsDict['down']:
                        self.direction = 'down'
                        self.y += self.speed
                    elif self.dirsDict['up']:
                        self.direction = 'up'
                        self.y -= self.speed
                    elif self.dirsDict['left']:
                        self.direction = 'left'
                        self.x -= self.speed
                elif self.dirsDict['right']:
                    if self.dirsDict['up'] and self.targetList[1] < self.y:
                        self.direction = 'up'
                        self.y -= self.speed
                    elif self.dirsDict['down'] and self.targetList[1] > self.y:
                        self.direction = 'down'
                        self.y += self.speed 
                    else:
                        self.x += self.speed

            elif self.direction == 'left':
                if self.dirsDict['down'] and self.targetList[1] > self.y:
                    self.direction = 'down'
                elif self.dirsDict['left'] and self.targetList[0] < self.x:
                    self.x -= self.speed
                    self.direction = 'left'
                elif self.dirsDict['left'] == False:
                    if self.dirsDict['down'] and self.targetList[1] > self.y:
                        self.direction = 'down'
                        self.y += self.speed
                    elif self.dirsDict['up'] and self.targetList[1] < self.y:
                        self.direction = 'up'
                        self.y -= self.speed
                    elif self.dirsDict['right'] and self.targetList[0] > self.x:
                        self.direction = 'right'
                        self.x += self.speed
                    elif self.dirsDict['up']:
                        self.direction = 'up'
                        self.y -= self.speed
                    elif self.dirsDict['down']:
                        self.direction = 'down'
                        self.y += self.speed
                    elif self.dirsDict['right']:
                        self.direction = 'right'
                        self.x += self.speed
                elif self.dirsDict['left']:
                    if self.dirsDict['down'] and self.targetList[1] > self.y:
                        self.direction = 'down'
                        self.y += self.speed
                    elif self.dirsDict['up'] and self.targetList[1] < self.y:
                        self.direction = 'up'
                        self.y -= self.speed
                    else:
                        self.x -= self.speed

            elif self.direction == 'up':
                if self.dirsDict['left'] and self.targetList[0] < self.x:
                    self.direction = 'left'
                    self.x -= self.speed
                elif self.dirsDict['right'] and self.targetList[0] > self.x:
                    self.x += self.speed
                    self.direction = 'right'        
                elif self.dirsDict['up'] and self.targetList[1] < self.y:
                    self.direction = 'up'
                    self.y -= self.speed
                elif self.dirsDict['up'] == False:
                    if self.dirsDict['right'] and self.targetList[0] > self.x:
                        self.direction = 'right'
                        self.x += self.speed
                    elif self.dirsDict['left'] and self.targetList[0] < self.x:
                        self.direction = 'left'
                        self.x -= self.speed 
                    elif self.dirsDict['down'] and self.targetList[1] > self.y:
                        self.direction = 'down'
                        self.y += self.speed
                    elif self.dirsDict['left']:
                        self.direction = 'left'
                        self.x -= self.speed
                    elif self.dirsDict['down']:
                        self.direction = 'down'
                        self.y += self.speed
                    elif self.dirsDict['right']:
                        self.direction = 'right'
                        self.x += self.speed                            
                elif self.dirsDict['up']:
                    if self.dirsDict['right'] and self.targetList[0] > self.x:
                        self.direction = 'right'
                        self.x += self.speed      
                    elif self.dirsDict['left'] and self.targetList[0] < self.x:
                        self.direction = 'left'
                        self.x -= self.speed
                    else:
                        self.y -= self.speed

            elif self.direction == 'down':
                if self.dirsDict['left'] and self.targetList[0] < self.x:
                    self.direction = 'left'
                    self.x -= self.speed
                elif self.dirsDict['right'] and self.targetList[0] > self.x:
                    self.x += self.speed
                    self.direction = 'right'
                elif self.dirsDict['down'] and self.targetList[1] > self.y:
                    self.y += self.speed
                elif self.dirsDict['down'] == False:
                    if self.dirsDict['right'] and self.targetList[0] > self.x:
                        self.direction = 'right'
                        self.x += self.speed
                    elif self.dirsDict['left'] and self.targetList[0] < self.x:
                        self.direction = 'left'
                        self.x -= self.speed
                    elif self.dirsDict['up'] and self.targetList[1] < self.y:
                        self.direction = 'up'
                        self.y -= self.speed
                    elif self.dirsDict['up']:
                        self.direction = 'up'
                        self.y -= self.speed
                    elif self.dirsDict['left']:
                        self.direction = 'left'
                        self.x -= self.speed
                    elif self.dirsDict['right']:
                        self.direction = 'right'
                        self.x += self.speed
                elif self.dirsDict['down']:
                    if self.dirsDict['right'] and self.targetList[0] > self.x:
                        self.direction = 'right'
                        self.x += self.speed 
                    elif self.dirsDict['left'] and self.targetList[0] < self.x:
                        self.direction = 'left'
                        self.x -= self.speed
                    else:
                        self.y += self.speed    

        #Handles ghost position if it goes though the tunnel    
        if self.x >= 580:
            self.x = 0
        elif self.x <= 1:
            self.x = 580 

    # Changes the speed of the ghost depending on the conditions of the game            
    def setGhostSpeed(self):
        if self.dead:
            self.speed = 10
        elif self.app.powerUp and self.dead == False:
            self.speed = 5
        if self.app.freezeTime and self.dead == False:
            self.speed = 0
        elif self.app.freezeTime == False and self.dead == False:
            self.speed = 5