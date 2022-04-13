from cmu_cs3_graphics import *
import prims, mazeGen

#Graph class inspired from TA-led mini lecture: Graph Algorithms.
#Maze drawing functions inspired from previous Tetris assignment.

def onAppStart(app):
    app.rows, app.cols = 11, 20
    app.grid = makePlatform(app) #initial platform
    app.maze = Graph(app.grid)
    #BoardFeatures
    app.margin = 25
    app.cellSize = 68
    app.name = 'Andres' #will be updated by user input

def makePlatform(app):
    platform = [app.cols * [0] for i in range(app.rows)]
    # code for the upper-left corner boundaries in notes: BORDER CODE
    return platform

def getCellBounds(app, row, col):
    sideMargin = (app.width - (app.cellSize * app.cols)) / 2
    left = sideMargin + (app.cellSize * col)
    verticalMargin = (app.height - (app.cellSize * app.rows)) / 2
    top = verticalMargin + (app.cellSize * row)
    return left, top

def drawCell(app, row, col):
    left, top = getCellBounds(app, row, col)
    width = app.cellSize
    height = app.cellSize
    maze = app.maze.getPlatform()
    if maze[row][col] == 1:
        drawRect(left, top, width, height, fill = 'white')
    elif maze[row][col] == 0:
        drawRect(left, top, width, height, fill = 'black')

def drawMaze(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawBackground(app):
    drawRect(0, 0, app.width, app.height, fill = 'lightblue')

def redrawAll(app):
    drawBackground(app)
    drawMaze(app)
 
def main():
    runApp(width=1440, height=810)

main()