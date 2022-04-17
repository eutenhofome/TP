from cmu_cs3_graphics import *
import mazeGen, entities, astar, string

def onAppStart(app):
    #MAZE
    app.rows, app.cols = 12, 24
    app.matrix = mazeGen.Graph(app.rows, app.cols)
    app.maze = mazeGen.mazeGenerator(app.matrix)
    app.maze.generatePrims()
    app.cellSize = 66
    app.cellRadius = (app.cellSize // 2)
    app.edgeSize = 58
    app.sideMargin = (app.width - (app.cellSize * app.cols)) // 2
    app.verticalMargin = (app.height - (app.cellSize * app.rows)) // 2 + 40
    app.edgeMargin = (app.cellSize - app.edgeSize) // 2

    # PLAYER
    app.player = entities.Player('Andres', app.matrix) #matrix
    print(app.player)

    #CAPYS
    app.capyCount = 10
    app.capybaras = generateCapys(app)
    #print(app.capybaras)

    #TIME
    app.ticks = 0
    app.stepsPerSecond = 15

def generateCapys(app):
    capySet = set()
    for i in range(app.capyCount):
        identifier = entities.Capybara(string.ascii_uppercase[i], app.matrix)
        capySet.add(identifier)
    return capySet

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
    elif key == 'right':
        app.player.direction = 'r'
        app.player.move()
    elif key == 'left':
        app.player.direction = 'l'
        app.player.move()
    elif key == 'up':
        app.player.direction = 'u'
        app.player.move()
    elif key == 'down':
        app.player.direction = 'd'
        app.player.move()

def drawPlayer(app):
    row, col = app.player.location[0], app.player.location[1]
    cx, cy = getCenter(app, row, col)
    drawRect(cx, cy, 40, 40, fill= 'red', align ='center')

def drawCapys(app):
    for capybara in app.capybaras:
        row, col = capybara.location[0], capybara.location[1]
        cx, cy = getCenter(app, row, col)
        drawOval(cx, cy, 20, 20, fill = 'brown', align = 'center')

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

def drawGrid(app):
    for row in range(app.rows):
        for col in range(app.cols):
            left, top = getCellBounds(app, row, col)
            width, height = app.cellSize, app.cellSize
            color = 'black'
            drawRect(left, top, width, height, fill = color, border = 'black',  borderWidth = 0, opacity = 50)

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