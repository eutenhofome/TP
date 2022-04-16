from cmu_cs3_graphics import *
import mazeGen, entities

#TO - DO:
# Find Difficult Path for start/end
# Capy Pathfinding:

def onAppStart(app):
    #MAZE
    app.rows, app.cols = 15, 30
    app.matrix = mazeGen.Graph(app.rows, app.cols)
    app.maze = mazeGen.mazeGenerator(app.matrix)
    app.maze.generatePrims()
    app.cellSize = 50
    app.cellRadius = (app.cellSize // 2)
    app.edgeSize = 40
    app.sideMargin = (app.width - (app.cellSize * app.cols)) // 2
    app.verticalMargin = (app.height - (app.cellSize * app.rows)) // 2 + 40
    app.edgeMargin = (app.cellSize - app.edgeSize) // 2

    # PLAYER
    app.player = entities.Player('Andres')

    app.capyCount = 4
    app.capybaras = entities.generateCapybaras(app.capyCount)

def getCellBounds(app, row, col):
    cellX = app.sideMargin + (app.cellSize * col)
    cellY = app.verticalMargin + (app.cellSize * row)
    return cellX, cellY

def getCenter(app, row, col):
    cellX, cellY = getCellBounds(app, row, col)
    midpointX = cellX + app.cellRadius
    midpointY = cellY + app.cellRadius
    return midpointX, midpointY

def onKeyPress(app, key): 
    if key == 'r':
        onAppStart(app)
    elif key == 'a':
        app.player.direction = 'l'
        app.player.move(app.matrix)
    elif key == 'w':
        app.player.direction = 'u'
        app.player.move(app.matrix)
    elif key == 'd':
        app.player.direction = 'r'
        app.player.move(app.matrix)
    elif key == 's':
        app.player.direction = 'd'
        app.player.move(app.matrix)

def drawPlayer(app):
    row, col = app.player.location[0], app.player.location[1]
    cx, cy = getCenter(app, row, col)
    drawRect(cx, cy, 20, 20, fill = 'red', align = 'center')

def drawCapys(app):
    for capybara in app.capybaras:
        row, col = capybara.location[0], capybara.location[1]
        cx, cy = getCenter(app, row, col)
        drawOval(cx, cy, 20, 20, fill = 'brown', align = 'center')

def drawGrid(app):
    for row in range(app.rows):
        for col in range(app.cols):
            left, top = getCellBounds(app, row, col)
            width, height = app.cellSize, app.cellSize
            color = 'black'
            drawRect(left, top, width, height, fill = color, border = 'black',  borderWidth = 1, opacity = 50)

def drawPassages(app):
    for node in app.maze.matrix.table:
        for connection in app.maze.matrix.table[node]:
            nodeRow, nodeCol = node[0], node[1]
            direction = app.matrix.edgeDirection(node, connection)
            cellX, cellY = getCellBounds(app, nodeRow, nodeCol)
            color = 'white'
            
            if direction == 'r':
                left = cellX + app.edgeMargin
                top = cellY + app.edgeMargin
                width = app.cellSize - app.edgeMargin
                height = app.edgeSize
                drawRect(left, top, width, height, fill = color)

            elif direction == 'l':
                left = cellX
                top = cellY + app.edgeMargin
                width = app.cellSize - app.edgeMargin
                height = app.edgeSize
                drawRect(left, top, width, height, fill = color)

            elif direction == 'u':
                left = cellX + app.edgeMargin
                top = cellY
                width = app.edgeSize
                height = app.cellSize - app.edgeMargin
                drawRect(left, top, width, height, fill = color)

            elif direction == 'd':
                left = cellX + app.edgeMargin
                top = cellY + app.edgeMargin
                width  = app.edgeSize
                height = app.cellSize - app.edgeMargin
                drawRect(left, top, width, height, fill = color)   

def drawBackground(app):
    drawRect(0, 0, app.width, app.height, fill = 'lightblue')

def redrawAll(app):
    drawBackground(app)
    drawGrid(app)
    drawPassages(app)
    drawPlayer(app)
    drawCapys(app)

def main(): 
    runApp(width=1632, height=918)

main()