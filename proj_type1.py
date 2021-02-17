import operator

correctArr = [[1,2,3],[4,5,6],[7,8,0]]

print("Syntax Check: Clear")

class Node:

    def __init__(self):
        self.arr = [[]]
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f


#Structure: 1 2 3
#           4 5 6
#           7 8 (b) --> 0
#correctArr = [[1,2,3],[4,5,6],[7,8,0]]

#Manhattan Distance
#To compute we know the row and column position of each item in the correctArr, thus to compute find the row and column of your current position for each
#item and then subtract by the rows and columsn of the correctArr, then add the differences to get the Manhattan Distance for each value. Sum for each
#index and assign to your h(n)

#Misplaced Tiles
#To compute we can compare our currArr to the correctArr and each value that isn't each to each other will increment by 1. The final value will be passed
#into our h(n)

def misplacedTiles(nodes, newnodes):
#^IDK if this is implemented correctly
    for w in range(len(newnodes)):
        nodes.append(new_nodes[w])
    hval = 0
    for i in range(len(nodes)):
        for j in range(len(nodes[i].arr)):
            for k in range(len(nodes[i].arr)):
                if correctArr[j][k] != nodes[i].arr[j][k]:
                    hval = hval + 1
        nodes[i].h = hval
        nodes[i].f = nodes[i].g + nodes[i].h
        hval = 0
    sorted_nodes = sorted(nodes, key=operator.attrgetter('f')) #Learned method from https://stackoverflow.com/questions/4010322/sort-a-list-of-class-instances-python
    return sorted_nodes


#Uniform Cost Search
#To compute each time we branch to a new node we will add one to our cost of that said node. As we continue down the levels of our tree we increment for each levels
#we assign a the level to be the g(n) of the current node.

def uniCostSearch(nodes, newnodes):
#^IDK if this is implemented correctly
    for w in range(len(newnodes)):
        nodes.append(newnodes[w])
    sorted_nodes = sorted(nodes, key=operator.attrgetter('g'))
    return sorted_nodes


#A*
#To do either of the A* when we finish getting the values of h(n) we will add it to g(n) of the current node and store into f(n)

#General Search
def generalsearch(QUEUEINGFUNCTION):
    initpuz = Node()
    initpuz.arr = [[1,2,3],[4,5,6],[0,7,8]]
    nodes = [initpuz]
    while True:
        if len(nodes)==0:
            return "Solution could not be found"
        testnode = nodes.pop(0)
        if correctArr == testnode.arr:
            return testnode
        nodes = QUEUEINGFUNCTION(nodes, expand(testnode, nodes))

def expand(node, nodelist):
    row, col = findblank(node.arr)
    temparr = node.arr
    temparr2 = temparr
    nodec = 0
    if row != 2: #Slide up
        temparr2[row][col],temparr2[row+1][col] = temparr2[row+1][col],temparr2[row][col]
        n1 = Node()
        n1.arr = temparr2
        n1.g = node.g + 1
        temparr2 = temparr
        nodelist.append(n1)
        nodec = nodec + 1
    if row != 0: #Slide down
        temparr2[row][col],temparr2[row-1][col] = temparr2[row-1][col],temparr2[row][col]
        n2 = Node()
        n2.arr = temparr2
        n2.g = node.g + 1
        temparr2 = temparr
        nodelist.append(n2)
        nodec = nodec + 1
    if col != 2: #Slide right
        temparr2[row][col],temparr2[row][col+1] = temparr2[row][col+1],temparr2[row][col]
        n3 = Node()
        n3.arr = temparr2
        n3.g = node.g + 1
        temparr2 = temparr
        nodelist.append(n3)
        nodec = nodec + 1
    if col != 0: #Slide left
        temparr2[row][col],temparr2[row][col-1] = temparr2[row][col-1],temparr2[row][col]
        n4 = Node()
        n4.arr = temparr2
        n4.g = node.g + 1
        temparr2 = temparr
        nodelist.append(n4)
        nodec = nodec + 1
    print(nodec)
    return nodelist

def findblank(arr):
    i = 0
    j = 0
    for i in range(len(arr)):
        for j in range(len(arr)):
            if arr[i][j] == 0:
                return i , j

initpuz = Node()
initpuz.arr = [[1,2,3],[4,5,6],[7,8,0]]
testlist = [initpuz]
list = []
test = generalsearch(uniCostSearch(testlist, list))
print(test)
