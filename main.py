from cmu_graphics import *
from PIL import Image
import time 
import copy
import os, pathlib
import random
from maze import maze
from ghost import *
from win import *
from helper import *
from pacmanHelper import *

def onAppStart(app):
    app.maze = copy.deepcopy(maze)
    app.startTime = time.time()
    app.width, app.height = 600, 720
    app.tileWidth, app.tileHeight = app.width // 30, (app.height - 120) // 30
    app.edgeWidth = 14
    app.pacmanX, app.pacmanY = app.width//2, 490
    app.pacmanSpeed = 5
    app.pacmanRadius = 16
    app.direction = 'right'
    app.currDirection = 'right' 
    app.score = 0
    app.lives = 3
    app.visible = True
    app.powerUp = False
    app.speedUp = False
    app.freezeTime = False
    app.startGame = False
    app.pauseGame = False
    app.gameOver = False
    app.gameWon = False
    app.dirsDict = {'right':False, 'left':False, 'up':False, 'down':False}
    app.ghostState = {'red':False, 'blue':False, 'pink':False, 'orange':False}
    app.ghostSpeed = 5
    app.ghostRadius = 17
    app.stepsPerSecond = 10
    app.flickerCounter = 1
    app.pelletsEaten = 0
    app.waitTime = 7

    app.intro = loadSound("sounds/intro.wav")
    app.playIntro = True

    app.chomp = loadSound("sounds/chomp.mp3")
    app.playChomp = False

    app.dead = loadSound("sounds/death.wav")
    app.playDeath = False

    app.eatGhost = loadSound("sounds/eatGhost.wav")

    app.eatPowerUP = loadSound("sounds/eatPowerUP.wav")

    app.speedUpMP3 = loadSound("sounds/speedUp.mp3")

    app.freezeTimeMP3 = loadSound("sounds/freezeTime.mp3")

    pacmanGif = Image.open('images/pacman.gif') # Animated pacman
    pacmanPNG = Image.open('images/sprites.png') # Pacman picture for # of lives drawing on bottom right
    app.pacmanPNG = CMUImage(pacmanPNG.crop((240, 285, 440, 480)))
    app.pacmanImageWidth, app.pacmanImageHeight = getImageSize(app.pacmanPNG)

    pacmanWin = Image.open('images/pacmanWin.png')
    app.pacmanWinPNG = CMUImage(pacmanWin.resize((200,200)))

    pacmanLose = Image.open('images/pacmanLose.png')
    app.pacmanLosePNG = CMUImage(pacmanLose.resize((200,200)))

    vulnerableGhost = Image.open('images/sprites1.png')
    app.vulnerableGhostIMG = CMUImage(vulnerableGhost.crop((0,400,100,500)).resize((30,30)))

    redGhost = Image.open('images/sprites1.png')
    app.redGhostIMG = CMUImage(redGhost.crop((0,0,100,100)).resize((30,30)))
    blueGhost = Image.open('images/sprites1.png')
    app.blueGhostIMG = CMUImage(blueGhost.crop((410,0,510,100)).resize((30,30)))
    pinkGhost = Image.open('images/sprites1.png')
    app.pinkGhostIMG = CMUImage(pinkGhost.crop((205,0,305,100)).resize((30,30)))
    orangeGhost = Image.open('images/sprites1.png')
    app.orangeGhostIMG = CMUImage(orangeGhost.crop((620,0,720,100)).resize((30,30)))

    ghostEyes = Image.open('images/ghostEyes.png')
    app.ghostEyesIMG = CMUImage(ghostEyes.resize((30,30)))

    speedUp = Image.open('images/speedUp.png')
    app.speedUpIMG = CMUImage((speedUp.resize((25,25))).rotate(45))

    freezeTime = Image.open('images/freezeTime.png')
    app.freezeTimeIMG = CMUImage(freezeTime.resize((30,30)))

    app.redGhostX, app.redGhostY, app.redGhostDirection = app.width//2, 250, 'right'
    app.blueGhostX, app.blueGhostY, app.blueGhostDirection = 260, 300, 'up'
    app.pinkGhostX, app.pinkGhostY, app.pinkGhostDirection = 300, 300, 'up'
    app.orangeGhostX, app.orangeGhostY, app.orangeGhostDirection = 340, 300, 'up'
    app.redGhostDead = app.blueGhostDead = app.pinkGhostDead = app.orangeGhostDead = False
    app.redGhostInCage, app.blueGhostInCage, app.pinkGhostInCage, app.orangeGhostInCage = False, True, True, True
    app.redGhostTargetList = app.blueGhostTargetList = app.pinkGhostTargetList = app.orangeGhostTargetList = [None, None]

    app.redGhost = Ghost(app, app.redGhostX, app.redGhostY, app.ghostSpeed, app.redGhostIMG, 
                         app.redGhostDirection, app.redGhostDead, app.redGhostInCage, app.redGhostTargetList)
    app.blueGhost = Ghost(app, app.blueGhostX, app.blueGhostY, app.ghostSpeed, app.blueGhostIMG, 
                          app.blueGhostDirection, app.blueGhostDead, app.blueGhostInCage, app.blueGhostTargetList)
    app.pinkGhost = Ghost(app, app.pinkGhostX, app.pinkGhostY, app.ghostSpeed, app.pinkGhostIMG, 
                          app.pinkGhostDirection, app.pinkGhostDead, app.pinkGhostInCage, app.pinkGhostTargetList)
    app.orangeGhost = Ghost(app, app.orangeGhostX, app.orangeGhostY, app.ghostSpeed, app.orangeGhostIMG, 
                            app.orangeGhostDirection, app.orangeGhostDead, app.orangeGhostInCage, app.orangeGhostTargetList)

    app.spriteListR = []
    app.spriteListL = []
    app.spriteListU = []
    app.spriteListD = []

    for frame in range(pacmanGif.n_frames):
        pacmanGif.seek(frame)
        fr = pacmanGif.resize((pacmanGif.size[0]//75, pacmanGif.size[1]//75))
        Rfr = CMUImage(fr)
        Ufr = CMUImage(fr.rotate(90))
        Dfr = CMUImage(fr.rotate(-90))
        Lfr = CMUImage(fr.rotate(-180))
        app.spriteListR.append(Rfr)
        app.spriteListL.append(Lfr)
        app.spriteListU.append(Ufr)
        app.spriteListD.append(Dfr)

    app.spriteListR.pop(0)
    app.spriteListL.pop(0)
    app.spriteListU.pop(0)
    app.spriteListD.pop(0)
    app.spriteCounter = 0

# Starts a new game if the player loses or wins
def newGame(app):
    app.maze = copy.deepcopy(maze)
    app.startTime = time.time()
    app.pacmanX, app.pacmanY = app.width//2, 490
    app.pacmanSpeed = 5
    app.pacmanRadius = 16
    app.direction = 'right'
    app.currDirection = 'right'
    app.score = 0
    app.lives = 3
    app.visible = True
    app.powerUp = False
    app.speedUp = False
    app.freezeTime = False
    app.startGame = False
    app.pauseGame = False
    app.gameOver = False
    app.gameWon = False
    app.dirsDict = {'right':False, 'left':False, 'up':False, 'down':False}
    app.ghostState = {'red':False, 'blue':False, 'pink':False, 'orange':False}
    app.ghostSpeed = 5
    app.ghostRadius = 17
    app.pelletsEaten = 0
    app.waitTime = 5

    app.playIntro = True
    app.playChomp = False
    app.playDeath = False

    app.redGhostX, app.redGhostY, app.redGhostDirection = app.width//2, 250, 'right'
    app.blueGhostX, app.blueGhostY, app.blueGhostDirection = 260, 300, 'up'
    app.pinkGhostX, app.pinkGhostY, app.pinkGhostDirection = 300, 300, 'up'
    app.orangeGhostX, app.orangeGhostY, app.orangeGhostDirection = 340, 300, 'up'
    app.redGhostDead = app.blueGhostDead = app.pinkGhostDead = app.orangeGhostDead = False
    app.redGhostInCage, app.blueGhostInCage, app.pinkGhostInCage, app.orangeGhostInCage = False, True, True, True
    app.redGhostTargetList = app.blueGhostTargetList = app.pinkGhostTargetList = app.orangeGhostTargetList = [None, None]

    app.redGhost = Ghost(app, app.redGhostX, app.redGhostY, app.ghostSpeed, app.redGhostIMG, 
                         app.redGhostDirection, app.redGhostDead, app.redGhostInCage, app.redGhostTargetList)
    app.blueGhost = Ghost(app, app.blueGhostX, app.blueGhostY, app.ghostSpeed, app.blueGhostIMG, 
                          app.blueGhostDirection, app.blueGhostDead, app.blueGhostInCage, app.blueGhostTargetList)
    app.pinkGhost = Ghost(app, app.pinkGhostX, app.pinkGhostY, app.ghostSpeed, app.pinkGhostIMG, 
                          app.pinkGhostDirection, app.pinkGhostDead, app.pinkGhostInCage, app.pinkGhostTargetList)
    app.orangeGhost = Ghost(app, app.orangeGhostX, app.orangeGhostY, app.ghostSpeed, app.orangeGhostIMG, 
                            app.orangeGhostDirection, app.orangeGhostDead, app.orangeGhostInCage, app.orangeGhostTargetList)

# Resets the game when the player loses a life
def resetGame(app):
    app.startTime = time.time()
    app.visible = True
    app.powerUp = False
    app.speedUp = False
    app.freezeTime = False
    app.startGame = False
    app.pauseGame = False
    app.gameOver = False
    app.gameWon = False
    app.waitTime = 3
    app.pacmanX, app.pacmanY = app.width//2, 490
    app.direction = 'right'
    app.currDirection = 'right'
    app.redGhostX, app.redGhostY, app.redGhostDirection = app.width//2, 250, 'right'
    app.blueGhostX, app.blueGhostY, app.blueGhostDirection = 260, 300, 'up'
    app.pinkGhostX, app.pinkGhostY, app.pinkGhostDirection = 300, 300, 'up'
    app.orangeGhostX, app.orangeGhostY, app.orangeGhostDirection = 340, 300, 'up'
    app.redGhostDead = app.blueGhostDead = app.pinkGhostDead = app.orangeGhostDead = False
    app.redGhostInCage, app.blueGhostInCage, app.pinkGhostInCage, app.orangeGhostInCage = False, True, True, True

    app.redGhost = Ghost(app, app.redGhostX, app.redGhostY, app.ghostSpeed, app.redGhostIMG, 
                    app.redGhostDirection, app.redGhostDead, app.redGhostInCage, app.redGhostTargetList)
    app.blueGhost = Ghost(app, app.blueGhostX, app.blueGhostY, app.ghostSpeed, app.blueGhostIMG, 
                    app.blueGhostDirection, app.blueGhostDead, app.blueGhostInCage, app.blueGhostTargetList)
    app.pinkGhost = Ghost(app, app.pinkGhostX, app.pinkGhostY, app.ghostSpeed, app.pinkGhostIMG, 
                    app.pinkGhostDirection, app.pinkGhostDead, app.pinkGhostInCage, app.pinkGhostTargetList)
    app.orangeGhost = Ghost(app, app.orangeGhostX, app.orangeGhostY, app.ghostSpeed, app.orangeGhostIMG, 
                    app.orangeGhostDirection, app.orangeGhostDead, app.orangeGhostInCage, app.orangeGhostTargetList)

    app.playChomp = False

    app.dead.play()

# Lose screen
def gameOver(app):
    if app.gameOver:
        drawRect(0, 0, 700, 750, fill='black', opacity = 60)
        drawImage(app.pacmanLosePNG, 80, 330, align = 'center')
        drawLabel('GAME OVER :<', app.width//2, 200, size = 55, bold = True, 
                italic = True, fill='white', align='center')
        drawLabel(f'Score: ', app.width//2-50, 320, size = 55, bold = True, 
                italic = True, fill='white', align='center')
        drawLabel(str(app.score), app.width//2+50, 325, size = 55, bold = True, 
                italic = True, fill='yellow', align='left')
        drawLabel("Press space key to play", app.width//2, 440, size = 40, bold = True, 
                italic = True, fill='yellow', align='center')

# Sets current direction to the key press
def onKeyPress(app, key):
    if app.startGame:
        if key == 'right':
            app.currDirection = 'right'
        elif key == 'left':
            app.currDirection = 'left'
        elif key == 'up':
            app.currDirection = 'up'
        elif key == 'down':
            app.currDirection = 'down'
    if key == 'space':
        if app.gameOver or app.gameWon:
            newGame(app)

# Change the game conditions based on what the ghost collides with
def checkGhostCollision(app, ghost):
    if app.powerUp == False:
        if ghost.dead == False:
            if distance(ghost.x, ghost.y, app.pacmanX, app.pacmanY) <= app.ghostRadius + app.pacmanRadius:
                if app.lives > 0:
                    app.lives -= 1
                    resetGame(app)
                else:
                    app.gameOver = True
                    app.startGame = False
    elif app.powerUp:
        if ghost.dead == False:
            if distance(ghost.x, ghost.y, app.pacmanX, app.pacmanY) <= app.ghostRadius + app.pacmanRadius:
                app.score += 200
                ghost.dead = True
                app.eatGhost.play()
    if ghost.inCage and ghost.dead:
        ghost.dead = False

def onStep(app):
    pacmanCanTurn(app)

    #give the user around 4 seconds to look at the game
    if app.pauseGame == False:
        currentTime = time.time()
        elapsedTime = currentTime - app.startTime
        if elapsedTime > app.waitTime:
            app.startGame = True

    currentTime = time.time()
    elapsedTime = currentTime - app.startTime

    if elapsedTime > 3:
        app.playIntro = False

    if app.waitTime >= 5:
        if elapsedTime > app.waitTime:
            app.playChomp = True
    elif app.waitTime == 3:
        if elapsedTime > app.waitTime:
            app.playChomp = True
            
    if app.playIntro == True:
        app.intro.play()
    if app.playChomp == True:
        app.chomp.play(loop = True)
    if app.playChomp == False:
        app.chomp.pause()
            
    #change the speed of pacman's biting animation
    app.spriteCounter = (app.spriteCounter + 3) % len(app.spriteListR)

    flicker(app)
    
    powerUps(app)

    Ghost.setGhostSpeed(app.redGhost)
    Ghost.getTargetList(app.redGhost)
    Ghost.ghostCanTurn(app.redGhost, app)
    Ghost.checkGhostCenter(app.redGhost)
    checkGhostCollision(app, app.redGhost)
    Ghost.redGhostPathfinding(app.redGhost)

    Ghost.setGhostSpeed(app.blueGhost)
    Ghost.getTargetList(app.blueGhost)
    Ghost.ghostCanTurn(app.blueGhost, app)
    Ghost.checkGhostCenter(app.blueGhost)
    checkGhostCollision(app, app.blueGhost)
    Ghost.blueGhostPathfinding(app.blueGhost)

    Ghost.setGhostSpeed(app.pinkGhost)
    Ghost.getTargetList(app.pinkGhost)
    Ghost.ghostCanTurn(app.pinkGhost, app)
    Ghost.checkGhostCenter(app.pinkGhost)
    checkGhostCollision(app, app.pinkGhost)
    Ghost.pinkGhostPathfinding(app.pinkGhost, app)

    Ghost.setGhostSpeed(app.orangeGhost)
    Ghost.getTargetList(app.orangeGhost)
    Ghost.ghostCanTurn(app.orangeGhost, app)
    Ghost.checkGhostCenter(app.orangeGhost)
    checkGhostCollision(app, app.orangeGhost)
    Ghost.orangeGhostPathfinding(app.orangeGhost,app)

    checkPacmanCenter(app)
    joystickMovement(app)
    movePacman(app)
    pacmanEat(app)
    tunnel(app)
    checkGameWon(app)

# Draws the maze based on the 2D list in maze.py
def drawMaze(app, maze): 
    for tileRow in range(len(maze)):
        for tileCol in range(len(maze[tileRow])):
            tile = maze[tileRow][tileCol]
            tileCenterX = app.tileWidth*tileCol + app.tileWidth//2
            tileCenterY = app.tileHeight*tileRow + app.tileHeight//2
            if tile == 'h':
                drawLine(app.tileWidth*tileCol,tileCenterY,app.tileWidth*tileCol+app.tileWidth,tileCenterY,fill='blue')
            elif tile == 'v':
                drawLine(tileCenterX,app.tileHeight*tileRow,tileCenterX,app.tileHeight*tileRow+app.tileHeight,fill='blue')
            elif tile == 'tL':
                drawArc(tileCenterX+app.tileWidth/2,tileCenterY+app.tileHeight//2+0.8,app.tileWidth+2,app.tileHeight+2,85,100,fill=None,border='blue')
                drawLine(tileCenterX+app.tileWidth//2,tileCenterY+1.7,tileCenterX+app.tileWidth//2,tileCenterY+app.tileHeight//2+1,lineWidth=4,fill='black')
                drawLine(tileCenterX+1,tileCenterY+app.tileHeight//2,tileCenterX+app.tileWidth//2,tileCenterY+app.tileHeight//2,lineWidth=4,fill='black')
            elif tile == 'tR':
                drawArc(tileCenterX-app.tileWidth/2,tileCenterY+app.tileHeight//2+0.8,app.tileWidth+2,app.tileHeight+2,-5,100,fill=None,border='blue')
                drawLine(tileCenterX-app.tileWidth//2,tileCenterY+1.6,tileCenterX-app.tileWidth//2,tileCenterY+app.tileHeight//2+1,lineWidth=4,fill='black')
                drawLine(tileCenterX-app.tileWidth//2,tileCenterY+app.tileHeight//2,tileCenterX-1,tileCenterY+app.tileHeight//2,lineWidth=4,fill='black')
            elif tile == 'bL':
                drawArc(tileCenterX+app.tileWidth//2,tileCenterY-app.tileHeight//2,app.tileWidth+1,app.tileHeight+1,175,100,fill=None,border='blue')
                drawLine(tileCenterX+app.tileWidth//2,tileCenterY-app.tileHeight//2-1,tileCenterX+app.tileWidth//2,tileCenterY-1,lineWidth=4,fill='black')
                drawLine(tileCenterX+1,tileCenterY-app.tileHeight//2,tileCenterX+app.tileWidth//2,tileCenterY-app.tileHeight//2,lineWidth=4,fill='black')
            elif tile == 'bR':
                drawArc(tileCenterX-app.tileWidth//2,tileCenterY-app.tileHeight//2,app.tileWidth+1,app.tileHeight+1,265,100,fill=None,border='blue')
                drawLine(tileCenterX-app.tileWidth//2,tileCenterY-app.tileHeight//2-1,tileCenterX-app.tileWidth//2,tileCenterY-1,lineWidth=4,fill='black')
                drawLine(tileCenterX-app.tileWidth//2-1,tileCenterY-app.tileHeight//2,tileCenterX-1,tileCenterY-app.tileHeight//2,lineWidth=4,fill='black')
            elif tile == 'p':
                drawCircle(tileCenterX,tileCenterY,3,fill='white')
            elif tile == 'pUP' and app.visible:
                drawCircle(tileCenterX,tileCenterY,8,fill='white')
            elif tile == 'gD':
                drawLine(app.tileWidth*tileCol,tileCenterY,app.tileWidth*tileCol+app.tileWidth,tileCenterY,fill='white')
            elif tile == 'speedUp' and app.visible:
                drawImage(app.speedUpIMG, tileCenterX, tileCenterY-10, align = 'center')
            elif tile == 'freezeTime' and app.visible:
                drawImage(app.freezeTimeIMG, tileCenterX-10, tileCenterY, align = 'center')

def redrawAll(app):
    drawRect(0, 0, 700, 750, fill='black')
    drawMaze(app, app.maze)
    drawPacman(app)
    Ghost.drawGhostState(app.redGhost)
    Ghost.drawGhostState(app.blueGhost)
    Ghost.drawGhostState(app.pinkGhost)
    Ghost.drawGhostState(app.orangeGhost)
    drawLabel(f'Score: {app.score}', 90, 680, size = 16, bold = True, 
                italic = True, fill='white', align='center')
    for i in range(app.lives):
        drawImage(app.pacmanPNG, 390+30*i, 680, align = 'center', 
                width = app.pacmanImageWidth//8, height = app.pacmanImageHeight//8)
    gameOver(app)
    winScreen(app)

runApp()

# Citations: 
# Code structure adapted from: https://pacmancode.com/
# Adapted & modified from: https://www.youtube.com/watch?v=5IMXpp3rohQ&ab_channel=ChrisCourses and https://www.youtube.com/watch?v=9H27CimgPsQ&ab_channel=LeMasterTech
# Maze inspired by the Pacman Game
# Maze.png: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.dailymail.co.uk%2Fsciencetech%2Farticle-3677136%2FThe-world-s-smallest-Pac-Man-maze-Scientists-recreate-1980s-computer-game-using-microscopic-organisms.html&psig=AOvVaw0rSX5thj24hfshcguqlJqn&ust=1700985406760000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCLj3rsnW3oIDFQAAAAAdAAAAABAK
# pacman4.gif: https://www.google.com/url?sa=i&url=https%3A%2F%2Flhongtortai.com%2Fcollection%2Fpac-man-gif&psig=AOvVaw2U0ynlZ7BTf8vR0TzSefC4&ust=1700985684930000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCNjw8NDX3oIDFQAAAAAdAAAAABAI
# sprites.png: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.vhv.rs%2Fviewpic%2FwRJmmT_pixel-art-pac-man-png-download-pacman-sprite%2F&psig=AOvVaw38wNMcZRVt7UVtAH0HZAq3&ust=1700985633818000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCPj28LfX3oIDFQAAAAAdAAAAABAD
# sprites1.png: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.deviantart.com%2Fammarzakwan-md%2Fart%2FPac-Man-LED-Pixel-Panel-Costume-Sprite-910004395&psig=AOvVaw1TV-bvRYRuT9A_3ZtGfN0b&ust=1701033839957000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCNDV24SL4IIDFQAAAAAdAAAAABAD
# ghostEyes.png: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.nintendo.co.uk%2FGames%2FNintendo-Switch-download-software%2FPAC-MAN-99-1950590.html&psig=AOvVaw0pzAiHwEM4aHj1yZ3S1wlO&ust=1701033765000000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCPjelN2K4IIDFQAAAAAdAAAAABAJ
# pacmanLose.png: https://www.google.com/url?sa=i&url=https%3A%2F%2Ffavpng.com%2Fpng_view%2Fms-pac-man-mario-kart-arcade-gp-2-png%2FZFwAPurv&psig=AOvVaw1q34KExlNfRU_qVXeFOLTo&ust=1701415266061000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCLip1rCa64IDFQAAAAAdAAAAABAD
# pacmanWin.png: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pngegg.com%2Fes%2Fpng-wpkmq&psig=AOvVaw1q34KExlNfRU_qVXeFOLTo&ust=1701415266061000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCLip1rCa64IDFQAAAAAdAAAAABAI
# intro.wav: https://www.classicgaming.cc/classics/pac-man/sounds
# chomp.mp3: https://creatorset.com/products/pacman-eating-sound-effect
# death.wav: https://www.classicgaming.cc/classics/pac-man/sounds
# eatGhost.wav: https://www.classicgaming.cc/classics/pac-man/sounds
# eatPowerUP.wav: https://www.classicgaming.cc/classics/pac-man/sounds
# speedUp.png: https://www.google.com/url?sa=i&url=https%3A%2F%2Ficon-library.com%2Ficon%2Fmaybe-icon-8.html&psig=AOvVaw1bThHaRJANd3_d9r84pyeX&ust=1701741323462000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCKjU_dDW9IIDFQAAAAAdAAAAABA4
# freezeTime.png: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.flaticon.com%2Ffree-icon%2Fstopwatch_3877525&psig=AOvVaw3A9gEmAoqjIAkdzKl9jzBq&ust=1701742559772000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCMDplZvb9IIDFQAAAAAdAAAAABAs
# speedUp.mp3: https://www.pond5.com/search?kw=speed-boost&media=sfx
# freezeTime.mp3: https://orangefreesounds.com/time-stop-sound-effect/#google_vignette

# Attempt at writing a BFS pathfinding algorithm:
def ghostBFS(self, app):
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    rows, cols = len(maze), len(maze[0])
    canMove = {'e', 'p', 'pUP', 'speedUp', 'freezeTime'}
    path = []
    queue = []
    visited = []
    currRow = self.x // self.app.tileWidth
    currCol = self.y // self.app.tileHeight
    targetRow = self.app.pacmanX // self.app.tileWidth
    targetCol = self.app.pacmanY // self.app.tileHeight
    queue.append((currRow, currCol, path))
    while queue:
        currRow, currCol, path = queue.pop(0)
        if (currRow, currCol) == (targetRow, targetCol):
            return path
        for direction in moves:
            newRow, newCol = currRow + direction[0], currCol + direction[1]
            if (maze[newRow][newCol] in canMove and (newRow, newCol) not in visited
                and 0 < newRow < rows and 0 < newCol < cols):
                newPath = path + [direction]
                visited.append((newRow,newCol))
                queue.append((newRow,newCol,newPath))
    return []
