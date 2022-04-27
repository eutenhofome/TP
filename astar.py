import mazeGen
#ASTAR FILE: uses aStar for pathfinding by taking in a startnode, endnode, and a matrix (dictionary with each node's connections), used for enemy pathfinding and capybara sensing to get them to jump up). Utilizes a PriorityQueue to simplify the aStar code, prioritized fCost, then hCost.

#aStar inspired by https://www.geeksforgeeks.org/a-search-algorithm/, https://www.baeldung.com/java-a-star-pathfinding, and TA-led mini lecture: Graph Algorithms.

class PriorityQueue(object):
    def __init__(self):
        self.priorityQueue = []
        self.lineage = dict()

    def add(self, fcost, hcost, node, papa):
        self.priorityQueue.append((fcost, hcost, node, papa))
        self.lineage[node] = papa

    def getPapa(self, node):
        for value in self.priorityQueue:
            if value[2] == node:
                return value[3]
    def getValue(self, node):
        for value in self.priorityQueue:
            if value[2] == node:
                return value
    def isIn(self, node):
        for value in self.priorityQueue:
            if value[2] == node:
                return True
        return False

    def remove(self): #follows best template to remove from queue
        maxFCost = 0
        maxHCost = 0
        maxCostIndex = 0
        #made to prioritize fCost, and then hCost if fcosts are equal
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
        return str(self.priorityQueue)

def h(startNode, endNode):  #manhattandist between 2 nodes
    startRow, startCol = startNode[0], startNode[1]
    endRow, endCol = endNode[0], endNode[1]
    manhattanDist = abs(endRow - startRow) + abs(endCol - startCol)
    return manhattanDist

def aStar(startNode, endNode, matrix):
    openList = PriorityQueue() #checked nodespriorityQueue, ranking (f then h)
    closedList = dict() #all nodes dict, key = fcost, hcost
    for node in matrix.table: #init each node as inf, 1000 works here
        closedList[node] = (1000, 1000, 2000) #gcost, hcost, fcost
    startG, startF, startH = 0, 0, 0
    closedList[startNode] = (startG, startH, startF)
    openList.add(startF, startH, startNode, None)
    #f0-h1-g2

    while openList.isComplete() == False:
        papaNode = openList.remove()[2] #returns popped high priority node

        #after each new papaNode, if papa is endNode, the search is complete and return path
        if papaNode == endNode:
            pathList = []
            while papaNode != None:
                pathList.append(papaNode)
                papaNode = openList.lineage[papaNode] #get papa's papa

            pathList.reverse() 
            pathList = pathList[1:] #removes firstNode(alien location)
            return pathList

        for neighbor in matrix.table[papaNode]: #loop thru each neighbor
            neighborG = closedList[papaNode][2] + 1 #unweighted graph
            neighborH = h(neighbor, endNode)
            neighborF = neighborG + neighborH
            neighborClosedF = closedList[neighbor][2] #j for ease

            if neighbor not in closedList or (neighborF < neighborClosedF): #if less fcost than stored
                closedList[neighbor] = (neighborG, neighborH, neighborF) #update neighbor info
                openList.add(neighborF, neighborH, neighbor, papaNode)

