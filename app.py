from cmu_cs3_graphics import *
import mazeGen, entities, random
from PIL import Image

def onAppStart(app):
    app.mode = 'start'
    #START SCREEN
    app.startBack = CMUImage(Image.open('startBack.png'))
    app.titleFrame = CMUImage(Image.open('title.png'))
    app.instructionFrame = CMUImage(Image.open('instructions.png'))
    app.easyMode = CMUImage(Image.open('easy.png'))
    app.easynon = CMUImage(Image.open('easynon.png'))
    app.hardMode = CMUImage(Image.open('hard.png'))
    app.hardnon = CMUImage(Image.open('hardnon.png'))
    app.playFrame = CMUImage(Image.open('play.png'))
    app.hard = False
    app.instructions = False # draw 30 opacity black screen infront of background

    #GAME SECTION
    app.gameBack = CMUImage(Image.open('gameBack.png'))
    app.level = 1
    app.gamePaused = False

    #MAZE
    app.rows, app.cols = 6 + (2 * app.level), 12 + (4 * app.level)
    app.cellSize = 66
    app.cellRadius = (app.cellSize // 2)
    app.edgeSize = 60
    app.sideMargin = (app.width - (app.cellSize * app.cols)) // 2
    app.verticalMargin = (app.height - (app.cellSize * app.rows)) // 2 + 40
    app.edgeMargin = (app.cellSize - app.edgeSize) // 2
    app.edgeWidth = 5
    app.menu = False

    app.matrix = mazeGen.Graph(app.rows, app.cols) #matrix variable

    if app.hard == False: #EASYMODE (PRIMS)
        app.maze = mazeGen.Prims(app.matrix) #maze variable
        app.maze.generatePrims() #uses Prim's on maze to create a maze in matrix
    else: #HARDMODE (KRUSKALS)
        print('kr')
        app.maze = mazeGen.Kruskals(app.matrix)
        app.maze.generateKruskals() #generates Kruskal's maze in matrix variable

    # PLAYER
    app.player = entities.Player('Andres', app.matrix) #matrix
    app.playerWidth, app.playerHeight = 40, 40
    app.prevDirection = 'r'
    app.savedCapys = 0
    app.playerHearts = 5
    app.statPics = entities.getStatPics()
    app.heartPics = entities.getHeartPics()
    app.numbers = entities.getNumberPics()
    
    #BOMB
    app.bombCoords = None
    app.bombisExploding = False
    app.bombCount = 10
    app.bombs = []
    app.bombRadius = 5
    app.expRadius = 10
    app.expLimit = 66

    #CAPYS
    app.capyCount = 3 * app.level + 1
    app.capybaras = entities.generateCapybaras(app.capyCount, app.matrix)

    #ENEMIES
    app.enemyCount = 2**app.level 
    app.enemies = entities.generateEnemies(app.enemyCount, app.matrix)

    #SPRITES
    app.playerSprites = entities.getPlayerSprites()
    app.capySprites = entities.getCapySprites()
    app.alienSprites = entities.getAlienSprites()

    #TIME
    app.spriteCounter = 0
    app.stepsPerSecond = 20
    app.ticks = 0

def startGame(app, level, difficulty):
    app.screen = 'game'
    #GAME SECTION
    app.gameBack = CMUImage(Image.open('gameBack.png'))
    app.level = 1
    app.gamePaused = False

    #MAZE
    app.rows, app.cols = 6 + (2 * app.level), 12 + (4 * app.level)
    app.cellSize = 66
    app.cellRadius = (app.cellSize // 2)
    app.edgeSize = 60
    app.sideMargin = (app.width - (app.cellSize * app.cols)) // 2
    app.verticalMargin = (app.height - (app.cellSize * app.rows)) // 2 + 40
    app.edgeMargin = (app.cellSize - app.edgeSize) // 2
    app.edgeWidth = 5
    app.menu = False

    app.matrix = mazeGen.Graph(app.rows, app.cols) #matrix variable

    if app.hard == False: #EASYMODE (PRIMS)
        app.maze = mazeGen.Prims(app.matrix) #maze variable
        app.maze.generatePrims() #uses Prim's on maze to create a maze in matrix
    else: #HARDMODE (KRUSKALS)
        app.maze = mazeGen.Kruskals(app.matrix)
        app.maze.generateKruskals() #generates Kruskal's maze in matrix variable

    # PLAYER
    app.player = entities.Player('Andres', app.matrix) #matrix
    app.playerWidth, app.playerHeight = 40, 40
    app.prevDirection = 'r'
    app.savedCapys = 0
    app.playerHearts = 5
    app.statPics = entities.getStatPics()
    app.heartPics = entities.getHeartPics()
    app.numbers = entities.getNumberPics()
    
    #BOMB
    app.bombCoords = None
    app.bombisExploding = False
    app.bombCount = 10
    app.bombs = []
    app.bombRadius = 5
    app.expRadius = 10
    app.expLimit = 66

    #CAPYS
    app.capyCount = 3 * app.level + 1
    app.capybaras = entities.generateCapybaras(app.capyCount, app.matrix)

    #ENEMIES
    app.enemyCount = 2**(app.level)
    app.enemies = entities.generateEnemies(app.enemyCount, app.matrix)

    #SPRITES
    app.playerSprites = entities.getPlayerSprites()
    app.capySprites = entities.getCapySprites()
    app.alienSprites = entities.getAlienSprites()

    #TIME
    app.spriteCounter = 0
    app.stepsPerSecond = 20
    app.ticks = 0

def gameOnKeyPress(app, key):
    if key == 'r':
        onAppStart(app)
    elif key  == 'escape':
        app.gamePaused = not app.gamePaused
        #app.mode = 'start'
    if app.player.hurt or app.gamePaused: return
    if key == 'd':
        app.player.direction = 'r'
        app.prevDirection = 'r'
        app.player.move()
    elif key == 'a':
        app.player.direction = 'l'
        app.prevDirection = 'l'
        app.player.move()
    elif key == 'w':
        app.player.direction = 'u'
        app.player.move()
    elif key == 's':
        app.player.direction = 'd'
        app.player.move()
    elif key == 'x':
        punch(app)
    elif key  == 'space':
        throwBomb(app)
    print(app.matrix[app.player.location])

def punch(app):
    directionValue = app.player.directions[app.player.direction]
    punchNode = app.maze.moveinDirection(app.player.location, directionValue)
    for enemy in app.enemies:
            if enemy.location == punchNode:
                enemy.stunned = (True, app.ticks)
                enemy.locked = False
                enemy.biting = False

def throwBomb(app):
    if app.bombCount < 1 or app.bombisExploding:
        return
    app.bombisExploding = True
    app.bombCount -= 1
    #direction
    #find landing point -> if no obstruction, 2cellSizes away, if edge, at edge:
    


def drawBomb(app):
    pass

def checkBombs(app):
    pass

def growBombs(app):
    pass

def gameOnStep(app):
    if app.gamePaused == True:
        return
    app.spriteCounter = (1 + app.spriteCounter) % 8 #how
    checkCapys(app)
    lockEnemies(app)
    if app.ticks % (8 - app.level) == 0:
        chaseEnemies(app)
    biteEnemies(app)
    checkPlayer(app)
    checkWin(app)
    checkDeath(app)
    unstunEnemies(app)
    checkBombs(app)
    growBombs(app)
    app.ticks += 1

def checkDeath(app):
    if app.playerHearts == 0:
        onAppStart(app)
def checkWin(app):
    row, col = app.rows - 1, app.cols -1
    if app.player.location == (row, col) and app.savedCapys == app.capyCount:
        if app.level < 3:
            app.level += 1
            difficulty = app.hard 
            startGame(app, app.level, difficulty)
        elif app.level == 3:
            onAppStart(app)

def checkPlayer(app):
    if app.playerHearts == 0:
        app.gameOver = True

def lockEnemies(app):
    if app.player.hurt == False: #if player is not getting bitten
        for enemy in app.enemies:
            if enemy.lock(app.player.location) == True:
                enemy.locked = True #lock possible enemies

    elif app.player.hurt == True: #if player getting bitten
        for enemy in app.enemies: 
            if enemy.locked == True: #unlock enemies
                enemy.locked = False
                enemy.direction = 'i'

def chaseEnemies(app):
    for enemy in app.enemies:
        if enemy.locked == True and enemy.stunned[0] == False:
            if enemy.location == app.player.location:
                app.player.hurt = True
                enemy.biting = True
                enemy.locked = False
            else:
                enemy.move(app.player.location)

def biteEnemies(app):
    for enemy in app.enemies:
        if enemy.biting == True:
            app.playerHearts -= 1
            enemy.stunned = (True, app.ticks)
            enemy.biting = False
            app.player.hurt = False

def unstunEnemies(app):
    for enemy in app.enemies:
        if enemy.stunned[0] == True:
            if app.ticks == enemy.stunned[1] + 30:
                enemy.stunned = (False, None)
                enemy.locked = False
                enemy.direction = 'i'

def checkCapys(app):
    savedCapys = set()
    for capybara in app.capybaras:
        if capybara.action != 'laying' and (len(capybara.getPath(app.player.location))) == 3:
            capybara.action = 'laying'
        if capybara.location == app.player.location:
            savedCapys.add(capybara)
            app.savedCapys += 1
    for capybara in savedCapys:
        app.capybaras.remove(capybara)

def drawPlayer(app):
    row, col = app.player.location[0], app.player.location[1]
    cx, cy = getCenter(app, row, col)
    drawRect(cx, cy, app.playerWidth, app.playerHeight, fill= 'red', align ='center')

def drawPlayerSprite(app):
    if app.player.direction == 'u' or app.player.direction == 'd':
        spriteStrip = app.playerSprites[app.prevDirection]
    else:
        spriteStrip = app.playerSprites[app.player.direction]
    sprite = spriteStrip[app.spriteCounter]
    width, height = 50, 58
    cx, cy = getEntityCoordsVert(app, app.player, width, height)
    app.player.coords = (cx, cy)
    drawImage(sprite, cx, cy, width=50, height=58)

def drawCapys(app):
    for capybara in app.capybaras:
        spriteStrip = app.capySprites[capybara.action]
        if capybara.action == 'laying':
            width, height = 52.2, 32.4
            cx, cy = getEntityCoordsVert(app, capybara, width, height)
            index =app.spriteCounter * -1
            sprite = spriteStrip[index]
            drawImage(sprite, cx, cy+10, width=52.2, height=32.4)
        else:
            width, height = 52.2, 23.1422
            cx, cy = getEntityCoordsVert(app, capybara, width, height)
            sprite = spriteStrip[0]
            drawImage(sprite, cx, cy+10, width=52.2, height=23.142)

def drawEnemies(app):
    for enemy in app.enemies:
        if enemy.stunned[0] == True:
            direction = random.choice(['lr','ll','lu','ld'])
            spriteStrip = app.alienSprites[direction]
            sprite = spriteStrip[app.spriteCounter]
            width, height = 31, 58
            cx, cy = getEntityCoordsVert(app, enemy, width, height)
            enemy.coords = (cx, cy)
            drawImage(sprite, cx, cy, width=31, height=58)

        elif enemy.locked == True:
            index = 'l'+enemy.direction
            spriteStrip = app.alienSprites[index]
            sprite = spriteStrip[app.spriteCounter]
            width, height = 31, 58
            cx, cy = getEntityCoordsVert(app, enemy, width, height)
            enemy.coords = (cx, cy)
            drawImage(sprite, cx, cy, width=31, height=58)
        
        elif enemy.biting == True:
            spriteStrip = app.alienSprites['lu']
            sprite = spriteStrip[app.spriteCounter]
            width, height = 31, 58
            cx, cy = getEntityCoordsVert(app, enemy, width, height)
            enemy.coords = (cx, cy)
            drawImage(sprite, cx, cy, width=31, height=58)


        elif enemy.stunned[0] == False and enemy.locked == False and (
            enemy.biting == False):
            spriteStrip = app.alienSprites[enemy.direction]
            sprite = spriteStrip[app.spriteCounter]
            width, height = 31, 58
            cx, cy = getEntityCoordsVert(app, enemy, width, height)
            enemy.coords = (cx, cy)
            drawImage(sprite, cx, cy, width=31, height=58)

def getEntityCoordsVert(app, entity, width, height):
    row, col = entity.location[0], entity.location[1]
    left, top = getCellBounds(app, row, col)
    cx = left + (app.cellSize - width)/2
    cy = top + (app.cellSize - height)/2
    entity.coords = (cx, cy)
    return cx, cy

def drawPassages(app):
    for node in app.maze.matrix.table:
        for connection in app.maze.matrix.table[node]:
            nodeRow, nodeCol = node[0], node[1]
            direction = app.matrix.edgeDirection(node, connection)
            cellX, cellY = getCellBounds(app, nodeRow, nodeCol)
            color = 'white'

            if nodeRow == app.rows - 1  and nodeCol == app.cols - 1:
                color = 'darkSeaGreen'

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
    color = 'lightSlateGray'
    for row in range(app.rows):
        for col in range(app.cols):
            #if row == app.rows-1 and col == app.cols-1:
                #color = 'green'
            left, top = getCellBounds(app, row, col)
            width, height = app.cellSize, app.cellSize
            drawRect(left, top, width, height, fill = color, opacity = 100)

def drawWalls(app):
    walls = app.maze.getWalls()

    for wall in walls:
        nodeX, nodeY = wall[0], wall[1]
        nodeXRow, nodeXCol = nodeX[0], nodeX[1]
        nodeYRow, nodeYCol = nodeY[0], nodeY[1]
        direction = app.matrix.edgeDirection(nodeX, nodeY)
        color = 'green'
        if direction == 'u':
            left, top = getCellBounds(app, nodeXRow, nodeXCol)
            width, height = app.cellSize, app.edgeWidth
            cx, cy = left, top - (height/2)
        elif direction == 'd':
            left, top = getCellBounds(app, nodeYRow, nodeYCol)
            width, height = app.cellSize, app.edgeWidth
            cx, cy = left, top - (height/2)

        elif direction == 'r':
            left,top = getCellBounds(app, nodeYRow, nodeYCol)
            width, height = app.edgeWidth, app.cellSize + (app.edgeWidth/2)
            cx, cy = left - (width/2), top - (width/2)
        elif direction == 'l':
            left,top = getCellBounds(app, nodeXRow, nodeXCol)
            width, height = app.edgeWidth, app.cellSize + (app.edgeWidth/2)
            cx, cy = left - (width/2), top - (width/2)
        drawRect(cx,cy,width, height, fill = color)

def drawBackground(app):
    drawImage(app.gameBack, 0, 0, width=1632, height=918)

def drawStats(app):
    #BOX
    statPic = app.statPics[app.level-1]
    cx, cy = app.sideMargin, app.verticalMargin-88
    drawImage(statPic,cx,cy)
    #HEARTS
    heartPic = app.heartPics[app.playerHearts]
    if app.level == 1:
        diff =  24
    elif app.level == 2:
        diff = 37
    else:
        diff = 50
    cx, cy = app.sideMargin + diff, app.verticalMargin-67
    drawImage(heartPic,cx,cy)
    #NUMBER

def gameRedrawAll(app):
    drawBackground(app)
    drawGrid(app)
    drawPassages(app)
    #drawEdges(app)
    drawPlayerSprite(app)
    drawCapys(app)
    drawEnemies(app)
    drawStats(app)
    #drawBomb(app)

#START!!!
def startOnKeyPress(app, key):
    print(app.instructions)
    if key == 'escape':
        app.instructions = False

def startOnMousePress(app, mouseX, mouseY):
    #PLAY
    if mouseX in range(302,1333) and mouseY in range(677,803):
        difficulty = app.hard
        startGame(app, 1, difficulty)
        app.mode = 'game'

    #INSTRUCTIONS
    elif mouseX in range(302,1333) and mouseY in range(325,479):
        app.instructions = True

    #EASY
    #w:507, h:153
    elif mouseX in range(302,810) and mouseY in range(507,661):
        app.hard = False
    #HARD
    elif mouseX in range(828, 1335) and mouseY in range(507,661):
        app.hard = True

def drawOptions(app):
    if app.hard == False:
        drawImage(app.easyMode, 302, 507)
        drawImage(app.hardnon, 828,507)
    else:
        drawImage(app.hardMode, 828, 507)
        drawImage(app.easynon, 302, 507)
    drawImage(app.instructionFrame, 302, 325)
    drawImage(app.playFrame, 302, 677)

def drawShips(app):
    pass

def startRedrawAll(app):
    drawImage(app.startBack, 0, 0, width=1632, height=918)
    drawImage(app.titleFrame, 220,110,width =1194,height=125)
    drawOptions(app)
    drawShips(app)
    
def main(): 
    runApp(width=1632, height=918)

def getCellBounds(app, row, col):
    cellX = app.sideMargin + (app.cellSize * col)
    cellY = app.verticalMargin + (app.cellSize * row)
    return cellX, cellY

def getCenter(app, row, col):
    cellX, cellY = getCellBounds(app, row, col)
    midpointX = cellX + app.cellRadius
    midpointY = cellY + app.cellRadius
    return midpointX, midpointY

main()