from cmu_cs3_graphics import *
import mazeGen, entities, random
from PIL import Image
#APP FILE: runs for visuals, stores entitiess and their interactions, as well as user interactions to the game.

def onAppStart(app):
    app.mode = 'start'
    #START SCREEN & ANIMATION
    app.startBack = CMUImage(Image.open('startBack.png'))
    app.titleFrame = CMUImage(Image.open('title.png'))
    app.instructionFrame = CMUImage(Image.open('instructions.png'))
    app.easyMode = CMUImage(Image.open('easy.png'))
    app.easynon = CMUImage(Image.open('easynon.png'))
    app.hardMode = CMUImage(Image.open('hard.png'))
    app.hardnon = CMUImage(Image.open('hardnon.png'))
    app.playFrame = CMUImage(Image.open('play.png'))
    app.winFrame = CMUImage(Image.open('win.png'))
    app.lossFrame = CMUImage(Image.open('loss.png'))
    app.homeInstructions = CMUImage(Image.open('homeInstruction.png'))
    app.gameInstructions = CMUImage(Image.open('gameInstruction.png'))
    app.stars = entities.getStars(300)
    app.texts = entities.getTexts()
    app.textCount = 1
    app.hard = False
    app.instructions = False #
    app.insideShip = CMUImage(Image.open('insideShip.png'))
    app.skipText = CMUImage(Image.open('skip.png'))
    app.textOpacity = 51
    app.textGoingUp = True

    #GAME SECTION
    app.gameBack = CMUImage(Image.open('gameBack.png'))
    app.level = 1
    app.gamePaused = False
    app.won = False
    app.gameOver = False

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

    if not app.hard: #EASYMODE (PRIMS)
        app.matrix = mazeGen.Graph(app.rows, app.cols) #matrix variable
        app.maze = mazeGen.Prims(app.matrix) #maze variable
        app.maze.generatePrims() #uses Prim's on maze to create a maze in matrix

    elif app.hard: #HARDMODE (KRUSKALS)
        app.matrix = mazeGen.Graph(app.rows, app.cols) #matrix variable
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
    app.shot = False
    #app.numbers = entities.getNumberPics()
    
    #BOMB
    app.bombisExploding = False
    app.bombRadius = 4
    app.bombLanded = False
    app.maxBombRadius = 30
    app.bombCoords = None
    app.bombDirection = None
    app.landingNode = None
    app.landingCoords = None
    app.totalCxDiff = None
    app.totalCyDiff = None

    #CAPYS
    app.capyCount = 3 * app.level + 1
    app.capybaras = entities.generateCapybaras(app.capyCount, app.matrix)

    #ENEMIES
    app.enemyCount = 2 ** app.level + 1
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
    app.mode = 'game'
    #GAME SECTION
    app.gameBack = CMUImage(Image.open('gameBack.png'))
    app.level = level
    app.gamePaused = False
    app.hard = difficulty
    app.won = False
    app.gameOver = False

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

    if app.hard == False: #EASYMODE (PRIMS)
        app.matrix = mazeGen.Graph(app.rows, app.cols) #matrix variable
        app.maze = mazeGen.Prims(app.matrix) #maze variable
        app.maze.generatePrims() #uses Prim's on maze to create a maze in matrix
    else: #HARDMODE (KRUSKALS)
        app.matrix = mazeGen.Graph(app.rows, app.cols) #matrix variable
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
    app.shot = False
    #app.capyNumbers = entities.getCapyNumberPics()
    
    #BOMB
    app.bombisExploding = False
    app.bombRadius = 4
    app.bombLanded = False
    app.maxBombRadius = 30
    app.bombCoords = None
    app.bombDirection = None
    app.landingNode = None
    app.landingCoords = None
    app.totalCxDiff = None
    app.totalCyDiff = None

    #CAPYS
    app.capyCount = 3 * level + 1
    app.capybaras = entities.generateCapybaras(app.capyCount, app.matrix)

    #ENEMIES
    app.enemyCount = 2 ** level + level
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
    if key ==  'p':
        level = app.level + 1
        startGame(app, level, app.hard)
    if key == 'r':
        onAppStart(app)
    elif key  == 'escape':
        app.gamePaused = not app.gamePaused
        if app.instructions == False:
            app.instructions = True
        else:
            app.instructions = False

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
    elif key  == 'up':
        if app.bombisExploding == False:
            app.bombDirection = ('u', (-1,0))
            throwBomb(app)
    elif key == 'down':
        if app.bombisExploding == False:
            app.bombDirection = ('d', (1,0))
            throwBomb(app)
    elif key == 'right':
        if app.bombisExploding == False:
            app.bombDirection = ('r', (0,1))
            throwBomb(app)
    elif key == 'left':
        if app.bombisExploding == False:
            app.bombDirection = ('l', (0,-1))
            throwBomb(app)

def punch(app):
    directionValue = app.player.directions[app.player.direction]
    punchNode = app.maze.moveinDirection(app.player.location, directionValue)
    for enemy in app.enemies:
            if enemy.location == punchNode:
                enemy.stunned = (True, app.ticks)
                enemy.locked = False
                enemy.biting = False

def findBombLanding(app):
    startNode = app.player.location
    direction = app.bombDirection[1]
    oneAway = app.maze.moveinDirection(startNode, direction)
    twoAway = app.maze.moveinDirection(oneAway, direction)
    #if 2 unit away is connected and in borders
    if app.hard == False:
        if app.matrix.hasPath(startNode, twoAway) and (
            app.maze.inBorders(twoAway)):
            return twoAway
    #if 1 unit away is connected and in borders
    if app.matrix.hasPath(startNode, oneAway) and (
        app.maze.inBorders(oneAway)):
        return oneAway
    else:
        return startNode

def throwBomb(app):
    if app.bombisExploding: return
    app.bombisExploding = True
    cx, cy = getCenter(app, app.player.location[0], app.player.location[1])
    app.bombCoords = [cx, cy]
    app.landingNode = findBombLanding(app)
    lCx, lCy = getCenter(app, app.landingNode[0], app.landingNode[1])
    app.landingCoords = [lCx, lCy]
    app.totalCxDiff, app.totalCyDiff = abs(lCx-cx), abs(lCy-cy)

def moveBomb(app):
    if app.bombisExploding == True and app.bombLanded == False:
        direction = app.bombDirection[0]
        if app.landingCoords != app.bombCoords:
            if direction == 'u':
                diff = abs(app.landingCoords[1] - app.bombCoords[1])
                if diff < 30:
                    app.bombCoords[1] -= diff
                else:
                    app.bombCoords[1] -= 30
            elif direction == 'd':
                diff = abs(app.landingCoords[1] - app.bombCoords[1])
                if diff < 30:
                    app.bombCoords[1] += diff
                else:
                    app.bombCoords[1] += 30
            elif direction == 'l':
                diff = abs(app.landingCoords[0] - app.bombCoords[0])
                if diff < 30:
                    app.bombCoords[0] -= diff
                else:
                    app.bombCoords[0] -= 30
            elif direction == 'r':
                diff = abs(app.landingCoords[0] - app.bombCoords[0])
                if diff < 30:
                    app.bombCoords[0] += diff
                else:
                    app.bombCoords[0] += 30
        else:
            app.bombLanded = True

def growBomb(app):
    if app.bombLanded == True:
        if app.bombRadius != app.maxBombRadius:
            diff = abs(app.maxBombRadius - app.bombRadius)
            if diff < 10:
                app.bombRadius += diff
            else:
                app.bombRadius += 10
        else:
            app.bombisExploding = False
            app.bombRadius = 5
            app.bombLanded = False
            app.maxBombRadius = 26
            app.bombCoords = None
            app.bombDirection = None
            app.landingNode = None
            app.landingCoords = None
            app.shot = False

def checkBombs(app):
    if app.bombLanded == True:
        if app.landingNode == app.player.location and app.shot == False:
            if app.playerHearts > 0:
                app.playerHearts -= 1
            app.shot = True
        for capybara in app.capybaras:
            if capybara.location == app.landingNode:
                app.gamePaused = True
                app.gameOver = True
        for enemy in app.enemies:
            if enemy.location == app.landingNode:
                enemy.stunned = (True, app.ticks)

def drawBomb(app):
    if app.bombisExploding == True and app.bombLanded == False:
        cx,cy = app.bombCoords[0], app.bombCoords[1]
        drawCircle(cx, cy, app.bombRadius+4, fill = 'brown')
        drawCircle(cx, cy, app.bombRadius+2, fill = 'chocolate')
    elif app.bombLanded == True:
        cx,cy = app.landingCoords[0], app.landingCoords[1]
        drawCircle(cx, cy, app.bombRadius, fill = 'darkRed')
        drawCircle(cx, cy, app.bombRadius-2, fill = 'crimson')
        drawCircle(cx, cy, app.bombRadius/2, fill = 'orangeRed')
        drawCircle(cx, cy, app.bombRadius/3, fill = 'darkOrange')
        drawCircle(cx, cy, app.bombRadius/4, fill = 'white')


def gameOnStep(app):
    checkBombs(app)
    if app.gamePaused == True:
        return
    checkLoss(app)
    app.spriteCounter = (1 + app.spriteCounter) % 8 #how
    checkCapys(app)
    lockEnemies(app)
    if app.ticks % (7) == 0:
        chaseEnemies(app)
    biteEnemies(app)
    checkWin(app)
    unstunEnemies(app)
    moveBomb(app)
    growBomb(app)
    app.ticks += 1

def checkWin(app):
    row, col = app.rows - 1, app.cols -1
    if app.player.location == (row, col) and app.savedCapys == app.capyCount:
        if app.level < 3:
            level = app.level + 1
            difficulty = app.hard 
            startGame(app, level, difficulty)
        elif app.level == 3:
            app.gamePaused = True
            app.won = True

def checkLoss(app):
    if app.playerHearts == 0:
        app.gamePaused = True
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
            if app.playerHearts > 0:
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
    if app.hard: color = 'darkGray'
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
    levelDict = app.statPics[app.level]
    statPic = levelDict[app.savedCapys]
    cx, cy = app.sideMargin, app.verticalMargin-88
    if app.level == 3:
        cy += 1
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

def drawBlind(app):
    if app.hard == False: return
    height = app.cellSize
    lastCol = app.cols - 1
    for row in range(app.rows):
        playerRow, playerCol = app.player.location[0], app.player.location[1]
        visibleRows = {playerRow - 1, playerRow + 1, playerRow}
        if row in visibleRows:
            if playerCol == 0 or playerCol == 1:
                cx, cy = getCellBounds(app, row, playerCol + 2)
                width = app.cellSize * (app.cols - playerCol - 2)
                drawRect(cx, cy, width, height, fill='black', opacity = 92)
            elif playerCol  == lastCol or playerCol == lastCol - 1:
                cx, cy = getCellBounds(app, row, 0)
                width = app.cellSize * (playerCol - 1)
                drawRect(cx, cy, width, height, fill='black', opacity = 92)

                
            else:
                #drawleftBlind
                leftEndCol = playerCol - 1
                cx, cy = getCellBounds(app, row, 0)
                width = app.cellSize * leftEndCol
                if playerCol == 2:
                    width = app.cellSize
                drawRect(cx, cy, width, height, fill='black', opacity = 92)

                #drawRightBlind
                rightStartCol = playerCol + 2
                cx, cy = getCellBounds(app, row, rightStartCol)
                width = app.cellSize * (app.cols - playerCol - 1)
                drawRect(cx, cy, width, height, fill='black', opacity = 92)

        else:
            cx, cy = getCellBounds(app, row, 0)
            width = app.cellSize * app.cols
            drawRect(cx, cy, width, height, fill='black', opacity = 92)

def drawWin(app):
    if app.won == True:
        drawRect(0,0, app.width, app.height, fill = 'black', opacity = 50)
        drawRect(318, 183, 996, 552, fill = 'darkSlateGray')
        drawImage(app.winFrame, 326, 191, width=980, height=536)

def drawLoss(app):
    if app.gameOver == True:
        drawRect(0,0, app.width, app.height, fill = 'black', opacity = 50)
        drawRect(318, 183, 996, 552, fill = 'darkSlateGray')
        drawImage(app.lossFrame, 326, 191, width=980, height=536)

def drawGameInstructions(app):
    if app.instructions == True:
        drawRect(0,0, app.width, app.height, opacity = 50)
        drawRect(51,62, 1529, 795, fill = 'slateGray')
        drawImage(app.gameInstructions, 55, 66)
    
def gameOnMousePress(app, mouseX, mouseY): 
    if app.instructions == True:
        #RESTART
        if mouseX in range(145,774) and mouseY in range(549,673):
            app.instructions = False
            startGame(app, 1, app.hard)
        elif mouseX in range(172,735) and mouseY in range(699,823):
            app.instructions = False
            app.mode = 'start'
        elif mouseX in range(1503,1558) and mouseY in range(86,138):
            app.instructions = False
            app.gamePaused = not app.gamePaused

    if app.won == True or app.gameOver == True:
        #PLAY AGAIN
        if mouseX in range(835,1127) and mouseY in range(425,556):
            startGame(app, 1, app.hard)
        #MENU
        elif mouseX in range(835,1127) and mouseY in range(576,659):
            app.mode = 'start'

def gameRedrawAll(app):
    drawBackground(app)
    drawGrid(app)
    drawPassages(app)
    drawPlayerSprite(app)
    drawCapys(app)
    drawEnemies(app)
    drawStats(app)
    drawBomb(app)
    drawBlind(app)
    drawWin(app)
    drawLoss(app)
    drawGameInstructions(app)


#START!!!
def startOnKeyPress(app, key):
    if key == 'escape':
        if app.instructions == True:
            app.instructions = False

def startOnMousePress(app, mouseX, mouseY):
    if app.instructions == True:
        if mouseX in range(1503,1558) and mouseY in range(86,138):
            app.instructions = False
    #PLAY
    if mouseX in range(302,1333) and mouseY in range(677,803):
        difficulty = app.hard
        playAnimation(app, difficulty)

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

def drawInstructions(app):
    if app.instructions == True:
        drawRect(51,62, 1529, 795, fill = 'slateGray')
        drawImage(app.homeInstructions, 55, 66)

def startRedrawAll(app):
    drawImage(app.startBack, 0, 0, width=1632, height=918)
    drawImage(app.titleFrame, 220,110,width =1194,height=125)
    drawOptions(app)
    drawInstructions(app)

def playAnimation(app, difficulty):
    app.hard = difficulty
    app.mode = 'animation'

def animationOnStep(app):
    if app.textOpacity == 30:
        app.textGoingUp = True
    elif app.textOpacity == 90:
        app.textGoingUp = False

    if app.textGoingUp:
        app.textOpacity += 1
    else:
        app.textOpacity -= 1

    for star in app.stars:
        if app.stars[star][2] > 90: 
            app.stars[star][3] == False
        elif app.stars[star][2] < 15:
            app.stars[star][3] == True

        if app.stars[star][3] == True:
            app.stars[star][2] = app.stars[star][2] + 1
        elif app.stars[star][3] == False:
            app.stars[star][2] -= app.stars[star][2] - 1
 
def drawStars(app):
    drawRect(550, 200, 600, 600, fill = 'black')
    for star in app.stars:
        image = app.stars[star][0]
        cx, cy = app.stars[star][1][0], app.stars[star][1][1]
        opacity = app.stars[star][2]
        if opacity > 100:
            opacity = 80
            app.stars[star][2] = 80
        elif opacity < 0:
            opacity = 30
            app.stars[star][2] = 30
        drawImage(image, cx, cy, opacity = abs(opacity))

def animationRedrawAll(app):
    drawStars(app)
    drawImage(app.insideShip, 0, 0, width=1632, height=918)
    drawImage(app.skipText, 1350, 880, width = 258, height=19, 
        opacity = app.textOpacity)
    drawImage(app.texts[app.textCount], 450, 650)

def animationOnKeyPress(app, key):
    if key == 'x':
        startGame(app, 1, app.hard)
    elif key == 'r':
        onAppStart(app)
    elif key == 'space':
        if app.textCount == 4:
            startGame(app, 1, app.hard)
        else:
            app.textCount += 1
    
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