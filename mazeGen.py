from cmu_cs3_graphics import *
import random

#Graph class inspired from TA-led mini lecture: Graph Algorithms.

class mazeGenerator(object): #used class to store sets in self. & cleanliness
    def __init__(self, matrix):
        self.unvisited = set() #unvisited nodes (not in maze)
        for row in range(matrix.rows):
            for col in range(matrix.cols):
                self.unvisited.add((row, col))
        self.frontiers = set() #current available frontiers
        self.mazedNodes = set() #nodes which have been converted, in maze now
        self.directions = ([-1, 0], [1, 0], [0, -1], [0, 1]) #easier 4 neighbors
        self.matrix = matrix #the adjacency list from the Graph class object
    
    def mazedNeighbors(self, node):#return frontier input's mazed neighbors
        neighbors = set()
        for direction in self.directions: #check in each direction
            possibleNeighbor = self.moveinDirection(node, direction)
            if self.inBorders(possibleNeighbor) and ( #checks if in borders
                possibleNeighbor in self.mazedNodes): #and within the maze
                neighbors.add(possibleNeighbor) 
        return neighbors
    
    def inBorders(self, node): #checks if a node is within the maze dimensions
        row, col = node[0], node[1] #each node is a tuple with (row,col)
        if 0 <= row < self.matrix.rows and 0 <= col < self.matrix.cols: 
            return True
        return False
    
    def moveinDirection(self, node, direction): #quick helper to clean code
        nodeRow, nodeCol = node[0], node[1]
        rowInc, colInc = direction[0], direction[1]
        newNode = (nodeRow + rowInc, nodeCol + colInc) #pos of node w/ dir move
        return newNode
    
    def addFrontiers(self, node): #adds frontiers of mazednode to frontier set
        for direction in self.directions: #checks neighbor in each direction
            possibleFrontier = self.moveinDirection(node, direction)
            if self.inBorders(possibleFrontier) and possibleFrontier in (
                self.unvisited): #must be inborders and unvisited(notm in maze)
                self.frontiers.add(possibleFrontier)
    
    def convert(self, node): #converts a frontier node to a maze node
        self.mazedNodes.add(node) #adds node to mazedNodes
        self.addFrontiers(node) #updates frontierset to accomodate change
        self.unvisited.remove(node) #removes node from unvisited
        if node in self.frontiers:
            self.frontiers.remove(node)
    
    def generatePrims(self): #uses helpers to generate Prim's maze
        randRow = random.randrange(self.matrix.rows)
        randCol = random.randrange(self.matrix.cols)
        self.convert((randRow, randCol)) #starts maze w/ random node
        while self.frontiers != set(): #while there are frontiers left
            frontier = random.choice(list(self.frontiers)) #list(for .choice)
            allMazedNeighbors = self.mazedNeighbors(frontier)
            index = random.randrange(len(allMazedNeighbors))
            mazedNeighbor = list(allMazedNeighbors)[index] #same here
            self.matrix.connect(mazedNeighbor, frontier)#passage(mazed->frontie)
            self.convert(frontier) #converts frontier after matrix.table update
    
    def getPlatform(self):
        for key in self.table:
            keyRow, keyCol = key[0], key[1]
            for value in self.table[key]:
                valRow, valCol = value[0], value[1]
                direction = self.edgeDirection(key, value)
                if self.grid[keyRow][keyCol] == None:
                    self.grid[keyRow][keyCol] = (direction)
                else:
                    self.grid[keyRow][keyCol].add(direction)
        return self.grid
    
    def __getitem__(self, item):
        return self.matrix[item]

class Graph(object): #class to manipulate an MST
    def __init__(self, rows, cols):
        self.table = {} #dictionary for adjacency list
        self.rows, self.cols = rows, cols #for maze dimensions
        self.grid = [cols * [None] for i in range(rows)] #initialize empty grid

    def connect(self, nodeX, nodeY): #nodeY added to NodeX key (mazed->frontier)
        self.table[nodeX] = self.table.get(nodeX, [])
        self.table[nodeX].append(nodeY)
        self.table[nodeY] = self.table.get(nodeY, [])
        self.table[nodeY].append(nodeX)

        nodeXRow, nodeXCol = nodeX[0], nodeX[1]
        direction = self.edgeDirection(nodeX, nodeY)
        if self.grid[nodeXRow][nodeXCol] == None:
            self.grid[nodeXRow][nodeXCol] = set()
        self.grid[nodeXRow][nodeXCol].add(direction)

        nodeYRow, nodeYCol = nodeY[0], nodeY[1]
        direction = self.edgeDirection(nodeY, nodeX)
        if self.grid[nodeYRow][nodeYCol] == None:
            self.grid[nodeYRow][nodeYCol] = set()
        self.grid[nodeYRow][nodeYCol].add(direction)
    
    def disconnect(self, nodeX, nodeY):#removes in all direction which it exists
        #not sure if I need it yet (may change for use) but wrote in case
        if nodeX in self.table and nodeY in self.table[nodeX]:
            self.table[nodeX].remove[nodeY]
        if nodeY in self.table and nodeX in self.table[nodeY]:
            self.table[nodeY].remove[nodeX]

    def isConnected(self, nodeX, nodeY): #checks if there is an edge btw 2 nodes
        #if either node is in other's key -> True
        if nodeX in self.table and nodeY in self.table[nodeX]:
            return True
        if nodeY in self.table and nodeX in self.table[nodeY]:
            return True
        return False
    
    def getConnections(self, node): #return a node's connections list
        connections = set() 
        if node in self.table: #all edges stored within precise node
            connections.add(self.table[node]) #adds those in node's key
        for key in self.table: #other nodes with unreciprocated connections
            if key == node or key in connections: #skip node itself and repeats
                pass
            if node in self.table[key]: #if in other node & unreciprocated
                connections.add(key)
        return connections
    
    def edgeDirection(self, nodeX, nodeY):#returns passage dir ('r','l','d','u')
        nodeXRow, nodeXCol = nodeX[0], nodeX[1]
        nodeYRow, nodeYCol = nodeY[0], nodeY[1]
        rowDiff, colDiff = nodeYRow - nodeXRow, nodeYCol - nodeXCol
        directionValue = (rowDiff, colDiff)
        if directionValue == (0, 1):
            return 'r'
        elif directionValue == (0, -1):
            return 'l'
        elif directionValue == (-1, 0):
            return 'u'
        elif directionValue == (1, 0):
            return 'd'
        
        return None #planning strings for visualization, not sure yet

    def getPlatform(self):
        for key in self.table:
            keyRow, keyCol = key[0], key[1]
            for value in self.table[key]:
                valRow, valCol = value[0], value[1]
                direction = self.edgeDirection(key, value)
                if self.grid[keyRow][keyCol] == None:
                    self.grid[keyRow][keyCol] = (direction)
                else:
                    self.grid[keyRow][keyCol].add(direction)
        return self.grid


    def __getitem__(self, item):
        return self.table[item]

    def __repr__(self):
        return str(self.table) #prints adjacency list

matrix = Graph(100, 100)
maze = mazeGenerator(matrix) 
maze.generatePrims()
newgrid = matrix.getPlatform
