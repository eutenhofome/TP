import astar, random, string

class Entity(object):
    def __init__(self, name, matrix):
        self.direction = None
        self.location = (0,0)
        self.directions = {'u': (-1, 0), 'd': (1,0), 'l': (0, -1), 'r': (0, 1)}
        self.matrix = matrix
        self.name = name
    
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
    
    def findPath(self, startNode, endNode):
        path = astar.aStar(startNode, endNode, self.matrix)
    
    def __repr__(self):
        return f'{self.name} at {self.location}'

class Player(Entity):
    def __init__(self, name, matrix):
        super().__init__(name, matrix)
        self.speed = 2
        self.breed = 'Player'

class Capybara(Entity):
    def __init__(self, name, matrix):
        super().__init__(name, matrix)
        self.breed = 'Capybara'
        self.speed = random.randrange(9, 15)
        self.location = findCorner(self.matrix)
    

class Enemy(Entity):
    def __init__(self, name, matrix):
        super().__init__(name, matrix)
        self.breed = 'Enemy'
        self.speed = random.randrange(9, 15)
        self.location = findEnemySpot(self.matrix)

def findEnemySpot(matrix):
    spots = set()
    for node in matrix:
        beginnerZone = 0
        nodeRow, nodeCol = node[0], node[1]
        if nodeRow <= 3 and nodeCol <= 3:
            beginnerZone += 1
        verticalEdgeCount = 0
        for edge in matrix[node]:
            edgeRow = edge[0]
            if edgeRow != nodeRow:
                verticalEdgeCount += 1
        if verticalEdgeCount == 0 and beginnerZone == 0:
            spots.add(node)
            
    spot = random.choice(list(spots))
    return spot

def findCorner(matrix):
    corners = set()
    for node in matrix:
        nodeRow, nodeCol = node[0], node[1]
        if len(matrix[node]) == 1 and nodeRow > 3 and nodeCol >3:
            corners.add(node)
    corner = random.choice(list(corners))
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



        
        

 
    