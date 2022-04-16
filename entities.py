import random, string

class Entity(object):
    def __init__(self):
        self.direction = None
        self.location = (0,0)
        self.directions = {'u': (-1, 0), 'd': (1,0), 'l': (0, -1), 'r': (0, 1)}
        self.speed = 0
    
    def isValidStep(self, possNode, matrix):
        possRow, possCol = possNode[0], possNode[1]
        if possRow < 0 or possRow >= matrix.rows:
            return False
        if possCol < 0 or possCol >= matrix.cols:
            return False
        if matrix.isConnected(self.location, possNode) == False:
            return False
        return True
    
    def move(self, matrix):
        directionValue = self.directions[self.direction]
        dx, dy = directionValue[0], directionValue[1]

        currRow, currCol = self.location[0], self.location[1]
        possRow, possCol = currRow + dx, currCol + dy
        possNode = (possRow, possCol)
    
        if self.isValidStep(possNode, matrix):
            self.location = (possRow, possCol)
    
class Player(Entity):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.speed = 15
        self.breed = 'Player'

class Capybara(object):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.breed = 'Capybara'
        self.speed = random.randrange(9, 15)
        self.location = (0,0)
    
    def __repr__(self):
        return self.name

def generateCapybaras(capys):
    capySet = set()
    letters = string.ascii_uppercase
    for i in range(capys):
        identifier = letters[i]
        identifier = Capybara(identifier)
        capySet.add(identifier)
    return capySet



        
        

 
    