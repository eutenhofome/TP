import random, string
import astar
from cmu_cs3_graphics import *
from PIL import Image
#ENTITIES FILE: contains classes for all entities(player, capybara, enemy), generates their individual information and traits and calls for them to move, this file also has functions which return all sprites/images for the game, which are called onAppStart.

#Alien Sprites from body/child/darkelf_2.png: by kheftel, Stephen Challener (Redshrike), Nila122, Matthew Krohn (makrohn), Marcel van de Steeg (MadMarcel). License(s): CC-BY-SA, Capybara Sprite foundation from artist Christian PachecoPlayer Sprites by Mark Knight, accessible at https://marmoset.co/posts/sprite-sheet-creation-in-hexels/.

#Sprite usage inspired by https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html. #8:Spritesheets using Pillow/PIL methods.

class Entity(object):
    def __init__(self, name, matrix):
        self.location = (0,0)
        self.directions = {'u': (-1, 0), 'd': (1,0), 'l': (0, -1), 'r': (0, 1)}
        self.matrix = matrix
        self.name = name
        self.action = 'd'
    def isValidStep(self, possNode, matrix): #checks in borders and is connect
        possRow, possCol = possNode[0], possNode[1]
        if possRow < 0 or possRow >= matrix.rows:
            return False
        if possCol < 0 or possCol >= matrix.cols:
            return False
        if matrix.isConnected(self.location, possNode) == False:
            return False
        return True
        
    def move(self):
        directionValue = self.directions[self.direction]
        dx, dy = directionValue[0], directionValue[1]

        currRow, currCol = self.location[0], self.location[1]
        possRow, possCol = currRow + dx, currCol + dy
        possNode = (possRow, possCol)
    
        if self.isValidStep(possNode, self.matrix):
            self.location = (possRow, possCol)
    
    def getPath(self, endNode):
        path = astar.aStar(self.location, endNode, self.matrix)
        return path
    
    def __repr__(self):
        return f'{self.name} at {self.location}'

class Player(Entity):
    def __init__(self, name, matrix):
        super().__init__(name, matrix)
        self.breed = 'Player'
        self.coords = (57,136)
        self.hurt = False
        self.direction = 'd'
        self.punch = False

class Capybara(Entity):
    def __init__(self, name, matrix):
        super().__init__(name, matrix)
        self.breed = 'Capybara'
        self.speed = random.randrange(9, 15)
        self.location = findCorner(self.matrix)
        self.action = 'lied'
        self.coords = (0,0)
    
    def __repr__(self):
        return self.location

class Enemy(Entity):
    def __init__(self, name, matrix):
        super().__init__(name, matrix)
        self.breed = 'Enemy'
        self.speed = random.randrange(9, 15)
        self.startingPoint = findEnemySpot(self.matrix)
        self.location = self.startingPoint
        self.locked = False
        self.biting = False
        self.stunned = (False, None)
        self.returning = False
        self.direction = 'i'

    def lock(self, endNode):
        path = self.getPath(endNode)
        if len(path) < 4:
            self.locked = True
            return True
        return False
    
    def move(self, endNode):
        path = self.getPath(endNode)
        #nextNode = path[self.location]
        nextNode = path[0]
        direction = self.matrix.edgeDirection(self.location, nextNode)
        self.direction = direction
        #how to slow down walking
        self.location = nextNode

def findEnemySpot(matrix): #away from spawn, and prioritizes horizontal paths
    spots = set()
    for node in matrix:
        beginnerZone, endZone = 0, 0
        nodeRow, nodeCol = node[0], node[1]
        if nodeRow <= 3 and nodeCol <= 3:
            beginnerZone += 1
        if nodeRow == matrix.rows-1 and nodeCol == matrix.cols-1:
            endZone += 1
        verticalEdgeCount = 0
        for edge in matrix[node]:
            edgeRow = edge[0]
            if edgeRow != nodeRow:
                verticalEdgeCount += 1
        if endZone == 0 and beginnerZone == 0:
            spots.add(node)
        
    spot = random.choice(list(spots))
    return spot

def findCorner(matrix):
    corners = []
    for node in matrix:
        nodeRow, nodeCol = node[0], node[1]
        #if len(matrix[node]) == 1 and nodeRow > 2 and nodeCol > 2:
        if nodeRow > 2 and nodeCol > 2:
            corners.append(node)      
    index = random.randint(0, len(corners)-1)
    corner = corners[index]
    return corner

def generateCapybaras(capys, matrix):
    capySet = set()
    letters = string.ascii_uppercase
    for i in range(capys):
        identifier = letters[i]
        identifier = Capybara(identifier, matrix)
        capySet.add(identifier)
    return capySet

def generateEnemies(enemies, matrix):
    enemySet = set()
    count = 0
    for i in range(enemies):
        identifier = 'E'+str(i)
        identifier = Enemy(identifier, matrix)
        enemySet.add(identifier)
    return enemySet

def getPlayerSprites():
    #left = first gap + width(leftshould -> nextleftshould)
    #right = start to rightshould + (lleftshould->leftshould)`
    sprites = dict()
    rightStrip = Image.open('astronaut.png')
    rightSprites = []
    for i in range(2):
        for j in range(5):
            left, top, right, bot = 39+196*j, 14+193*i, 162+196*j, 172+196*i
            sprite = CMUImage(rightStrip.crop((left,top,right,bot)))
            rightSprites.append(sprite)
    sprites['r'] = rightSprites

    leftStrip = Image.open('astronautLeft.png')
    leftSprites = []
    for i in range(2):
        for j in range(5):
            left, top, right, bot = 39+196*j, 14+193*i, 162+196*j, 172+196*i
            sprite = CMUImage(leftStrip.crop((left,top,right,bot)))
            leftSprites.append(sprite)
    sprites['l'] = leftSprites
    return sprites

#CAPY SPRITES
def getCapySprites():
    sprites = dict()
    layingStrip = Image.open('capyLaying.png')
    layingSprites = []
    for i in range(9):
        left,top,right,bot = 20 +145*i, 98, 146+145*i, 180
        sprite = CMUImage(layingStrip.crop((left, top, right, bot)))
        layingSprites.append(sprite)
    sprites['laying'] = layingSprites

    liedStrip = Image.open('capyLaying.png')
    liedSprites = []
    left,top,right,bot = 10, 0, 136, 56
    sprite = CMUImage(liedStrip.crop((left, top, right, bot)))
    liedSprites.append(sprite)
    sprites['lied'] = liedSprites
    return sprites

#ALIENSPRITES
def getAlienSprites():
    sprites = dict()
    upStrip = Image.open('aliengoUp.png')
    upSprites = []
    for i in range(9):
        left,top,right,bot = 56 +179*i, 0, 120+179*i, 113
        sprite = CMUImage(upStrip.crop((left, top, right, bot)))
        upSprites.append(sprite)
    sprites['u'] = upSprites

    downStrip = Image.open('alienDown.png')
    downSprites = []
    for i in range(9):
        left,top,right,bot = 20 +64*i, 0, 43+64*i, 42
        sprite = CMUImage(downStrip.crop((left, top, right, bot)))
        downSprites.append(sprite)
    sprites['d'] = downSprites

    leftStrip = Image.open('alienLeft.png')
    leftSprites = []
    for i in range(9):
        left,top,right,bot = 21 +64*i, 0, 44+64*i, 41
        sprite = CMUImage(leftStrip.crop((left, top, right, bot)))
        leftSprites.append(sprite)
    sprites['l'] = leftSprites

    rightStrip = Image.open('alienRight.png')
    rightSprites = []
    for i in range(9):
        left,top,right,bot = 20 +64*i, 0, 43+64*i, 41
        sprite = CMUImage(rightStrip.crop((left, top, right, bot)))
        rightSprites.append(sprite)
    sprites['r'] = rightSprites
    
    idleStrip = Image.open('alienIdle.png')
    idleSprites = []
    for i in range(9):
        left,top,right,bot = 20 +64*i, 0, 43+64*i, 42
        sprite = CMUImage(idleStrip.crop((left, top, right, bot)))
        idleSprites.append(sprite)
    sprites['i'] = idleSprites

    upStrip = Image.open('lockedUp.png')
    upSprites = []
    for i in range(9):
        left,top,right,bot = 56 +179*i, 0, 120+179*i, 113
        sprite = CMUImage(upStrip.crop((left, top, right, bot)))
        upSprites.append(sprite)
    sprites['lu'] = upSprites

    downStrip = Image.open('lockedDown.png')
    downSprites = []
    for i in range(9):
        left,top,right,bot = 20 +64*i, 0, 43+64*i, 42
        sprite = CMUImage(downStrip.crop((left, top, right, bot)))
        downSprites.append(sprite)
    sprites['ld'] = downSprites

    leftStrip = Image.open('lockedLeft.png')
    leftSprites = []
    for i in range(9):
        left,top,right,bot = 21 +64*i, 0, 44+64*i, 41
        sprite = CMUImage(leftStrip.crop((left, top, right, bot)))
        leftSprites.append(sprite)
    sprites['ll'] = leftSprites

    rightStrip = Image.open('lockedRight.png')
    rightSprites = []
    for i in range(9):
        left,top,right,bot = 20 +64*i, 0, 43+64*i, 41
        sprite = CMUImage(rightStrip.crop((left, top, right, bot)))
        rightSprites.append(sprite)
    sprites['lr'] = rightSprites

    idleStrip = Image.open('lockedIdle.png')
    idleSprites = []
    for i in range(9):
        left,top,right,bot = 20 +64*i, 0, 43+64*i, 42
        sprite = CMUImage(idleStrip.crop((left, top, right, bot)))
        idleSprites.append(sprite)
    sprites['li'] = idleSprites

    return sprites
    
def getHeartPics():
    pics = []
    for i in range(6):
        title = str(i)+'heart.png'
        pic = CMUImage(Image.open(title))
        pics.append(pic)
    return pics

def getStatPics():
    pics = dict()
    #level1
    level1 = dict()
    for i in range(0,5):
        title = '1stat'+str(i)+'.png'
        pic = CMUImage(Image.open(title))
        level1[i] = pic
    pics[1] = level1

    level2 = dict()
    for i in range(0,8):
        title = '2stat'+str(i)+'.png'
        pic = CMUImage(Image.open(title))
        level2[i] = pic
    pics[2] = level2

    level3 = dict()
    for i in range(0,11):
        title = '3stat'+str(i)+'.png'
        pic = CMUImage(Image.open(title))
        level3[i] = pic
    pics[3] = level3
    return pics

def getStarPics():
    pics = []
    #level1
    for i in range(1,4):
        title = 'stat'+str(i)+'.png'
        pic = CMUImage(Image.open(title))
        pics.append(pic)
    return pics
    #level2
    #level3

def getStars(count):
    stars = dict()
    for i in range(count):
        number = random.randint(1,5)
        opacity = random.randint(16,94)
        title = 'star'+str(number)+'.png'

        if opacity < 50:
            goingUp = True
        elif opacity > 50:
            goingUp = False
    
        pic = CMUImage(Image.open(title))
        cx, cy = random.randint(580, 1067), random.randint(200, 650)
        stars[i] = [pic, [cx,cy], opacity, goingUp]
    return stars

def getTexts():
    texts = dict()
    for i in range(1,5):
        title = 'text'+str(i)+'.png'
        pic = CMUImage(Image.open(title))
        texts[i] = pic
    return texts
    
def getNumberPics():
    numbers = dict()
    for i in range(0,10):
        title = i
        pic = CMUImage(Image.open(title))
        numbers[i] = pic
    return numbers
