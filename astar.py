import mazeGen

rows, cols = 2, 2
matrix = mazeGen.Graph(rows, cols)
maze = mazeGen.mazeGenerator(matrix)
maze.generatePrims()

class PriorityQueue(object):
    def __init__(self):
        self.priorityQueue = []

    def add(self, fcost, hcost, node):
        self.priorityQueue.append((fcost, hcost, node))
    
    def remove(self):
        maxFCost = 0
        maxHCost = 0
        maxCostIndex = None

        for index in range(len(self.priorityQueue)):
            value = self.priorityQueue[index]
            fCost, hCost = value[0], value[1]

            if fCost > maxFCost:
                maxFCost = fCost
                maxCostIndex = index
                if hCost > maxHCost:
                    maxHCost = hCost

            elif fCost == maxFCost and hCost > maxHCost:
                maxHCost = hCost
                maxCostIndex = index

        return self.priorityQueue.pop(maxCostIndex)
    
    def isComplete(self):
        if len(self.priorityQueue) == 0:
            return True
        return False

    def __repr__(self):
        return self.priorityQueue

def h(startNode, endNode):
    startRow, startCol = startNode[0], startNode[1]
    endRow, endCol = endNode[0], endNode[1]
    manhattanDist = abs(endRow - startRow) + abs(endCol - startCol)
    return manhattanDist

def f(gCount, startNode, endNode):
    fCount = gCount + h(startNode, endNode)
    return fCount

def aStar(startNode, endNode, matrix):
    directions = {(-1, 0), (1,0), (0, -1), (0, 1)}
    priorityQueue = PriorityQueue()
    gCosts = dict()
    fCosts = dict()
    for node in matrix.table:
        gCosts[node] = 1000
        fCosts[node] = 1000
    gCosts[startNode] = 0
    fCosts[startNode] = h(startNode, endNode)
    
    startFCost = h(startNode, endNode) + 0
    startHCost = h(startNode, endNode)
    priorityQueue.add(startFCost, startHCost, startNode)
    
    allPaths = {}
    while priorityQueue.isComplete() == False:
        currNode = priorityQueue.remove()[2]
        if currNode == endNode:
            break
        for neighborNode in matrix.table[currNode]:
            neighborGCost = gCosts[currNode] + 1
            neighborFCost = neighborGCost + h(currNode, endNode)
            neighborHCost = h(currNode, endNode)
            if neighborFCost < fCosts[neighborNode]:
                gCosts[neighborNode] = neighborGCost
                fCosts[neighborNode] = neighborFCost
                priorityQueue.add(neighborFCost, neighborHCost, neighborNode)
                allPaths[neighborNode] = currNode
        
    sortedPath = {}
    currNode = endNode

    while currNode != startNode:
        sortedPath[allPaths[currNode]] = currNode
        currNode = allPaths[currNode]
    return sortedPath

rows, cols = 12, 24
matrix = mazeGen.Graph(rows, cols)
maze = mazeGen.mazeGenerator(matrix)
maze.generatePrims()
print(aStar((0,0),(11,23),matrix))