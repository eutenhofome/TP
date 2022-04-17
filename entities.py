import random, string

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
    
class Player(Entity):
    def __init__(self, name, matrix):
        super().__init__(name, matrix)
        self.speed = 2
        self.breed = 'Player'
    
    def __repr__(self):
        return (self.name, self.location)

class Capybara(Entity):
    def __init__(self, name, matrix):
        super().__init__(name, matrix)
        self.breed = 'Capybara'
        self.speed = random.randrange(9, 15)
        self.location = random.choice(list(matrix.table))
    
    def __repr__(self):
        return (self.name, self.location)

def generateCapybaras(capys):
    capySet = set()
    letters = string.ascii_uppercase
    for i in range(capys):
        identifier = letters[i]
        identifier = Capybara(identifier)
        capySet.add(identifier)
    return capySet



        
        

 
    