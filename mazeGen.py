from cmu_cs3_graphics import *
import random
#MAZEGEN FILE: has a Graph class, Prim's class, and Kruskal's class. Adjacency dictionary/matrix is stored in the graph class, with functions to manipulate the MST within it. The graph class object is either inputted in Prim's class, if game difficulty is easy, or Kruskal's class, if difficulty is hard. Both Prim's and Kruskal's classes contain functions which compose the algorithm, and then finally generate a maze when self.generate(Prims/Kruskals) is called, result is stored in the adjacency dictionary/matrix.

#Graph class inspired from TA-led mini lecture: Graph Algorithms.
#Used visualization from https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm, to understand Prim's concept.
#Used https://en.wikipedia.org/wiki/Kruskal%27s_algorithm to understand Kruskal's concept.

#CLASS USED TO GENERATE PRIM'S MAZE FOR EASY MODE
class Prims(object): #used class to store sets in self. & cleanliness
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
    
    def getDifferences(self, node): #returns the neighbors of input node, which it is not connected to (used to help find walls in getWalls)
        connections = self.matrix.table[node]
        neighbors = set()
        for direction in self.directions: #check in each direction
            possibleNeighbor = self.moveinDirection(node, direction)
            if self.inBorders(possibleNeighbor):
                neighbors.add(possibleNeighbor) 
        differences = set()
        
        for neighbor in neighbors: #if neighbor is not connected add to diffs
            if neighbor not in connections:
                differences.add(neighbor)
        return differences

    def getWalls(self): #returns set of each wall dividing maze
        walls = set()
        for node in self.matrix.table:
            differences = self.getDifferences(node)
            for difference in differences:
                wall = (node, difference) 
                reversedWall = (difference, node) #to remove repeats
                if wall not in walls and reversedWall not in walls:
                    walls.add(wall)
        return walls
    
    def __getitem__(self, item):
        return self.matrix[item]

class Graph(object): #class to manipulate an MST
    def __init__(self, rows, cols):
        self.table = {} #dictionary for adjacency list
        self.rows, self.cols = rows, cols #for maze dimensions
        self.grid = [cols * [None] for i in range(rows)] #initialize empty grid
        self.directions = ([-1, 0], [1, 0], [0, -1], [0, 1])

    def connect(self, nodeX, nodeY): #nodeY added to NodeX key (mazed->frontier)
        self.table[nodeX] = self.table.get(nodeX, [])
        self.table[nodeX].append(nodeY)
        self.table[nodeY] = self.table.get(nodeY, [])
        self.table[nodeY].append(nodeX)
    
    def disconnect(self, nodeX, nodeY):#removes in all direction which it exists
        #not sure if I need it yet (may change for use) but wrote in case
        if nodeX in self.table and nodeY in self.table[nodeX]:
            self.table[nodeX].remove[nodeY]
        if nodeY in self.table and nodeX in self.table[nodeY]:
            self.table[nodeY].remove[nodeX]

    def hasPath(self, nodeX, nodeY):
        for connection in self.table[nodeX]:
            if connection == nodeY:
                return True
            for otherConnection in self.table[connection]:
                if otherConnection == nodeY:
                    return True
        return False
        
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

    def __getitem__(self, item): #lets me index 
        return self.table[item]

    def __iter__(self): #lets me iterate class in a for loop
        return iter(self.table)

    def __repr__(self):
        return str(self.table) #prints adjacency list

#CLASS USED TO GENERATE KRUSKAL'S MAZE FOR HARD MODE
class Kruskals(object):
    def __init__(self, matrix):
        self.matrix = matrix
        self.forest = self.makeForest()
        self.edges = self.getEdges()
        self.nodes = int(self.matrix.rows) * int(self.matrix.cols)
        self.edgeCount = len(self.edges)
    
    def makeForest(self): #generates forest, list with set for each node
        forest = []
        for row in range(self.matrix.rows):
            for col in range(self.matrix.cols):
                tree = {(row, col)}
                forest.append(tree)
        return forest

    def inBorders(self, node): #checks if a node is within the maze dimensions
        row, col = node[0], node[1]
        if 0 <= row < self.matrix.rows and 0 <= col < self.matrix.cols: 
            return True
        return False

    def moveinDirection(self, node, direction):
        nodeRow, nodeCol = node[0], node[1]
        rowInc, colInc = direction[0], direction[1]
        newNode = (nodeRow + rowInc, nodeCol + colInc) 
        return newNode

    def getNeighbors(self, node): #returns all valid neighbors of a node
        neighbors = set()
        for direction in self.matrix.directions:
            possibleNeighbor = self.moveinDirection(node, direction)
            if self.inBorders(possibleNeighbor) == True:
                neighbors.add(possibleNeighbor)
        return neighbors

    def getEdges(self): #generates a set of all possible edges in the maze
        edges = set()
        for row in range(self.matrix.rows):
            for col in range(self.matrix.cols):
                node = (row, col)
                neighbors = self.getNeighbors(node)
                for neighbor in neighbors:
                    edge = (node, neighbor)
                    reversedEdge = (neighbor, node)
                    if edge not in edges and reversedEdge not in edges:
                        edges.add(edge)
        return edges

    def mergeTrees(self, nodeX, nodeY): #merge trees of both nodes
        forest = [] #initialize new forest list
        for tree in self.forest:
            if nodeX in tree:
                nodeXTree = tree
            elif nodeY in tree:
                nodeYTree = tree
            else:
                forest.append(tree)
        newTree = nodeXTree.union(nodeYTree)
        forest.append(newTree) #appends mix of nodeXTree and nodeYTree
        self.forest = forest #update self.forest

    def isComplete(self):
        if len(self.edges) == 1:
            return True
        return False
    
    def inSameTree(self, nodeX, nodeY): #checks if two nodes are in same tree
        for tree in self.forest:
            if nodeX in tree and nodeY in tree:
                return True
        return False

    def generateKruskals(self):
        #while there are still edges and the forest has multiple trees(not MST)
        while self.isComplete() == False and len(self.forest) != 1:
            index = random.randint(0, len(self.edges)-1)
            edge = list(self.edges)[index] #select random edge
            nodeX, nodeY = edge[0], edge[1]
            if self.inSameTree(nodeX, nodeY) == False: #if nodes in diff trees
                self.matrix.connect(nodeX, nodeY) #connect them in graph class
                self.mergeTrees(nodeX, nodeY) #merge their trees
                self.edges.remove(edge) #remove from edges