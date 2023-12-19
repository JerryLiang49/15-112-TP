# Drawing the maze piece by piece is too complicated, so we can represent each 
# piece of the maze with letters. Looking at Maze.png, we can see that the 
# entire maze can be recreated with several different piece, not including 
# Pacman or the ghosts. 
# 'e' represents an empty black square
# 'h' represents a horizontal blue line
# 'v' represents a vertical blue line
# 'tL' represents a top left corner
# 'tR' represents a top right corner
# 'bL' represents a bottom left corner
# 'bR' represents a bottom right corner
# 'p' represents a normal pellet
# 'pUP' represents a power up pellet
# 'gD' represents a horizontal white line (the ghost door)
# 'speedUp' represents the speed boost power-up
# 'freezeTime' represents the time freeze power-up
# I will now represent the maze with a 2D list:

maze = [
['tL', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 
'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'tR'],
['v', 'tL', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'tR', 
'tL', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'tR', 'v'],
['v', 'v', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'v', 
'v', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'v', 'v'],
['v', 'v', 'p', 'tL', 'h', 'h', 'tR', 'p', 'tL', 'h', 'h', 'h', 'tR', 'p', 'v', 
'v', 'p', 'tL', 'h', 'h', 'h', 'tR', 'p', 'tL', 'h', 'h', 'tR', 'p', 'v', 'v'],
['v', 'v', 'pUP', 'v', 'e', 'e', 'v', 'p', 'v', 'e', 'e', 'e', 'v', 'p', 'v', 
'v', 'p', 'v', 'e', 'e', 'e', 'v', 'p', 'v', 'e', 'e', 'v', 'pUP', 'v', 'v'],
['v', 'v', 'p', 'bL', 'h', 'h', 'bR', 'p', 'bL', 'h', 'h', 'h', 'bR', 'p', 'bL',
'bR', 'p', 'bL', 'h', 'h', 'h', 'bR', 'p', 'bL', 'h', 'h', 'bR', 'p', 'v', 'v'],
['v', 'v', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 
'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'v', 'v'],
['v', 'v', 'p', 'tL', 'h', 'h', 'tR', 'p', 'tL', 'tR', 'p', 'tL', 'h', 'h', 'h', 
'h', 'h', 'h', 'tR', 'p', 'tL', 'tR', 'p', 'tL', 'h', 'h', 'tR', 'p', 'v', 'v'],
['v', 'v', 'p', 'bL', 'h', 'h', 'bR', 'p', 'v', 'v', 'p', 'bL', 'h', 'h', 'tR', 
'tL', 'h', 'h', 'bR', 'p', 'v', 'v', 'p', 'bL', 'h', 'h', 'bR', 'p', 'v', 'v'],
['v', 'v', 'p', 'p', 'p', 'p', 'p', 'p', 'v', 'v', 'p', 'p', 'p', 'p', 'v', 
'v', 'p', 'p', 'p', 'p', 'v', 'v', 'p', 'p', 'p', 'p', 'p', 'p', 'v', 'v'],
['v', 'bL', 'h', 'h', 'h', 'h', 'tR', 'p', 'v', 'bL', 'h', 'h', 'tR', 'e', 'v', 
'v', 'e', 'tL', 'h', 'h', 'bR', 'v', 'p', 'tL', 'h', 'h', 'h', 'h', 'bR', 'v'],
['v', 'e', 'e', 'e', 'e', 'e', 'v', 'p', 'v', 'tL', 'h', 'h', 'bR', 'e', 'bL', 
'bR', 'e', 'bL', 'h', 'h', 'tR', 'v', 'p', 'v', 'e', 'e', 'e', 'e', 'e', 'v'],
['v', 'e', 'e', 'e', 'e', 'e', 'v', 'p', 'v', 'v', 'e', 'e', 'e', 'e', 'e', 
'e', 'e', 'e', 'e', 'e', 'v', 'v', 'p', 'v', 'e', 'e', 'e', 'e', 'e', 'v'],
['bR', 'e', 'e', 'e', 'e', 'e', 'v', 'p', 'v', 'v', 'e', 'tL', 'h', 'h', 'gD', 
'gD', 'h', 'h', 'tR', 'e', 'v', 'v', 'p', 'v', 'e', 'e', 'e', 'e', 'e', 'bL'],
['h', 'h', 'h', 'h', 'h', 'h', 'bR', 'e', 'bL', 'bR', 'e', 'v', 'e', 'e', 'e', 
'e', 'e', 'e', 'v', 'e', 'bL', 'bR', 'e', 'bL', 'h', 'h', 'h', 'h', 'h', 'h'],
['e', 'e', 'e', 'e', 'e', 'e', 'e', 'speedUp', 'e', 'e', 'e', 'v', 'e', 'e', 'e', 
'e', 'e', 'e', 'v', 'e', 'e', 'e', 'speedUp', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
['h', 'h', 'h', 'h', 'h', 'h', 'tR', 'p', 'tL', 'tR', 'e', 'v', 'e', 'e', 'e', 
'e', 'e', 'e', 'v', 'e', 'tL', 'tR', 'p', 'tL', 'h', 'h', 'h', 'h', 'h', 'h'],
['tR', 'e', 'e', 'e', 'e', 'e', 'v', 'p', 'v', 'v', 'e', 'bL', 'h', 'h', 'h', 
'h', 'h', 'h', 'bR', 'e', 'v', 'v', 'p', 'v', 'e', 'e', 'e', 'e', 'e', 'tL'],
['v', 'e', 'e', 'e', 'e', 'e', 'v', 'p', 'v', 'v', 'e', 'e', 'e', 'e', 'e', 
'e', 'e', 'e', 'e', 'e', 'v', 'v', 'p', 'v', 'e', 'e', 'e', 'e', 'e', 'v'],
['v', 'e', 'e', 'e', 'e', 'e', 'v', 'p', 'v', 'v', 'e', 'tL', 'h', 'h', 'h', 
'h', 'h', 'h', 'tR', 'e', 'v', 'v', 'p', 'v', 'e', 'e', 'e', 'e', 'e', 'v'],
['v', 'tL', 'h', 'h', 'h', 'h', 'bR', 'p', 'bL', 'bR', 'e', 'bL', 'h', 'h', 'tR', 
'tL', 'h', 'h', 'bR', 'e', 'bL', 'bR', 'p', 'bL', 'h', 'h', 'h', 'h', 'tR', 'v'],
['v', 'v', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'v', 
'v', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'v', 'v'],
['v', 'v', 'p', 'tL', 'h', 'h', 'tR', 'p', 'tL', 'h', 'h', 'h', 'tR', 'p', 'v', 
'v', 'p', 'tL', 'h', 'h', 'h', 'tR', 'p', 'tL', 'h', 'h', 'tR', 'p', 'v', 'v'],
['v', 'v', 'p', 'bL', 'h', 'tR', 'v', 'p', 'bL', 'h', 'h', 'h', 'bR', 'p', 'bL', 
'bR', 'p', 'bL', 'h', 'h', 'h', 'bR', 'p', 'v', 'tL', 'h', 'bR', 'p', 'v', 'v'],
['v', 'v', 'pUP', 'p', 'p', 'v', 'v', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 
'e', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'v', 'v', 'p', 'p', 'pUP', 'v', 'v'],
['v', 'bL', 'h', 'tR', 'p', 'v', 'v', 'p', 'tL', 'tR', 'p', 'tL', 'h', 'h', 'h', 
'h', 'h', 'h', 'tR', 'p', 'tL', 'tR', 'p', 'v', 'v', 'p', 'tL', 'h', 'bR', 'v'],
['v', 'tL', 'h', 'bR', 'p', 'bL', 'bR', 'p', 'v', 'v', 'p', 'bL', 'h', 'h', 'tR', 
'tL', 'h', 'h', 'bR', 'p', 'v', 'v', 'p', 'bL', 'bR', 'p', 'bL', 'h', 'tR', 'v'],
['v', 'v', 'p', 'p', 'p', 'p', 'p', 'p', 'v', 'v', 'p', 'p', 'p', 'p', 'v', 
'v', 'p', 'p', 'p', 'p', 'v', 'v', 'p', 'p', 'p', 'p', 'p', 'p', 'v', 'v'],
['v', 'v', 'p', 'tL', 'h', 'h', 'h', 'h', 'bR', 'bL', 'h', 'h', 'tR', 'p', 'v', 
'v', 'p', 'tL', 'h', 'h', 'bR', 'bL', 'h', 'h', 'h', 'h', 'tR', 'p', 'v', 'v'],
['v', 'v', 'p', 'bL', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'bR', 'p', 'bL', 
'bR', 'p', 'bL', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'bR', 'p', 'v', 'v'],
['v', 'v', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'e', 
'freezeTime', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'v', 'v'],
['v', 'bL', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 
'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'bR', 'v'],
['bL', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 
'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'bR']
]