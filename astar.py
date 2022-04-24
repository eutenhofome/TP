import mazeGen
#aStar inspired by https://www.geeksforgeeks.org/a-search-algorithm/, and TA-led mini lecture: Graph Algorithms.

class PriorityQueue(object):
    def __init__(self):
        self.priorityQueue = []

    def add(self, fcost, hcost, node):
        self.priorityQueue.append((fcost, hcost, node))

    def isIn(self, node):
        for value in self.priorityQueue:
            if value[2] == node:
                return True
        return False

    def remove(self):
        maxFCost = 0
        maxHCost = 0
        maxCostIndex = 0

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
    startGCost, startFCost, startHCost = 0, 0, 0
    closedList[startNode] = (startGCost, startHCost, startFCost)
    openList.add(startFCost, startHCost, startNode)
    #f0-h1-g2
    tracedPath = {} #tracks node lineage [neighbor : papa]

    while openList.isComplete() == False:
        papaNode = openList.remove()[2] #returns popped high priority node
        if papaNode == endNode: #ends for loop when final node reached
            break #stops tha loop
        for neighbor in matrix.table[papaNode]: #loop thru each neighbor
            neighborGCost = closedList[papaNode][2] + 1 #unweighted graph
            neighborHCost = h(neighbor, endNode)
            neighborFCost = neighborGCost + neighborHCost
            neighborClosedFCost = closedList[neighbor][2] #j for ease

            if neighbor not in closedList or (neighborFCost < neighborClosedFCost): #if less fcost than stored
                closedList[neighbor] = (neighborGCost, neighborHCost, neighborFCost) #update neighbor info
                tracedPath[neighbor] = papaNode #attach papa to son
                openList.add(neighborFCost, neighborHCost, neighbor)
    path = makePath(tracedPath, startNode, endNode)
    return path

def makePath(roughPath, startNode, endNode): #helper to organize path
    currNode = endNode
    pathList = [currNode]
    while currNode != startNode:
        currNode = roughPath[currNode]
        pathList.append(currNode)
    pathList.reverse() #to select nextNode at path[0], dont like using -1 for index
    pathList = pathList[1:] #easier for aliens to just start going asap
    return pathList