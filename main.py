import operator
import copy
import time

correctArr = [[1,2,3],[4,5,6],[7,8,0]] #The final array that will denote we reached the correct solution
dictionary = [] #Keeps track of all nodes that have been seen
expnodes = 0

class Node: #Made a node class that has the array of each step of the puzzle as well as its g h and f values to compare

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

def manhattanDist(nodes, newnodes):
    count = 1
    for w in range(len(newnodes)):
        nodes.append(newnodes[w])
    hval = 0
    for i in range(len(nodes)):
        for j in range(len(nodes[i].arr)):
            for k in range(len(nodes[i].arr)):
                if count == 9:
                     continue
                else:
                     s1, s2 = findval(count, nodes[i].arr)
                     hval = hval + abs(s1 - j) + abs(s2 - k)
                     count = count + 1
        nodes[i].h = hval
        nodes[i].f = nodes[i].g + nodes[i].h
        hval = 0
        count = 1
    sorted_nodes = sorted(nodes, key=operator.attrgetter('f', 'g'))
    return sorted_nodes


#Misplaced Tiles
#To compute we can compare our currArr to the correctArr and each value that isn't each to each other will increment by 1. The final value will be passed
#into our h(n). To do this we just checked for each value in the array if it was matching the correct array at each give index. If it doesn't we just increment the value by 1

def misplacedTiles(nodes, newnodes):
#^IDK if this is implemented correctly
    for w in range(len(newnodes)):
        nodes.append(newnodes[w])
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
    for w in range(len(newnodes)):
        nodes.append(newnodes[w])
    return nodes

def QUEUEINGFUNCTION(nodes, newnodes, queuefunc):
    newnodes_u = removeDups(newnodes)
    if queuefunc == 1:
        return uniCostSearch(nodes, newnodes_u)
    if queuefunc == 2:
        return misplacedTiles(nodes, newnodes_u)
    if queuefunc == 3:
        return manhattanDist(nodes, newnodes_u)

#Remove Duplicates: This function will take in the newnodes and check if they are already in a dictionary continaing all nodes seen. If it was not contained
#we then add that node into our dictionary. If they are in the dictionary we simply pop.
def removeDups(newnodes):
    checker = True
    newnodes_u = []
    for i in range(len(newnodes)):
        for j in range(len(dictionary)):
            if(newnodes[i].arr == dictionary[j].arr):
                checker = False
        if(checker):
            newnodes_u.append(newnodes[i])
        checker = True
    dictionary.extend(newnodes_u)
    return newnodes_u

#General Search, generally taken from the template with added printing lines, and added some counters for prinitng results.
def generalsearch(str_node, queuefunc):
    nodes = [str_node]
    dictionary.append(str_node)
    nodes_maxlen = 0
    nodes_expanded = 0
    while True:
        if len(nodes) > nodes_maxlen:
            nodes_maxlen = len(nodes)
        if len(nodes)==0:
            return "Solution could not be found"
        testnode = nodes.pop(0)
        nodes_expanded = nodes_expanded + 1
        print("Checking Puzzle:")
        for i, ind in enumerate(testnode.arr): #learned from https://www.tutorialspoint.com/enumerate-in-python
            print(*ind)
        if correctArr == testnode.arr:
            print("^ is the correct node!")
            print("Depth:", testnode.g)
            print("Max Queue Size:", nodes_maxlen, "nodes")
            print("The Number of Nodes Expanded:", nodes_expanded, "nodes")
            print("CPU Time:", time.process_time(), 'seconds')
            print("Nodes remaining in queue", len(nodes), "nodes")
            return testnode
        nodes = QUEUEINGFUNCTION(nodes, expand(testnode), queuefunc)

#The expand function takes the node that we most recently cheked and finds each possible move that we could be making. This is then passed into another fucntion to remove redundant puzzles
def expand(node):
    row, col = findblank(node.arr)
    tempnode = copy.deepcopy(node)
    temparr2 = copy.deepcopy(tempnode.arr)
    nodelist = []
    if row != len(node.arr)-1: #Slide up
        temparr2[row][col],temparr2[row+1][col] = temparr2[row+1][col],temparr2[row][col]
        n1 = Node()
        n1.arr = temparr2
        n1.g = node.g + 1
        temparr2 = copy.deepcopy(tempnode.arr)
        nodelist.append(n1)
    if row != 0: #Slide down
        temparr2[row][col],temparr2[row-1][col] = temparr2[row-1][col],temparr2[row][col]
        n2 = Node()
        n2.arr = temparr2
        n2.g = node.g + 1
        temparr2 = copy.deepcopy(tempnode.arr)
        nodelist.append(n2)
    if col != len(node.arr)-1: #Slide right
        temparr2[row][col],temparr2[row][col+1] = temparr2[row][col+1],temparr2[row][col]
        n3 = Node()
        n3.arr = temparr2
        n3.g = node.g + 1
        temparr2 = copy.deepcopy(tempnode.arr)
        nodelist.append(n3)
    if col != 0: #Slide left
        temparr2[row][col],temparr2[row][col-1] = temparr2[row][col-1],temparr2[row][col]
        n4 = Node()
        n4.arr = temparr2
        n4.g = node.g + 1
        temparr2 = copy.deepcopy(tempnode.arr)
        nodelist.append(n4)
    return nodelist

#Helper function that will find where the blank in the puzzle is on any passed in array
def findblank(arr):
    i = 0
    j = 0
    for i in range(len(arr)):
        for j in range(len(arr)):
            if arr[i][j] == 0:
                return i , j
#Helper fucntion I realized I needed after I made the find blank function. I could have just deleted find blank but it would have been more editing.
def findval(num, arr):
    i = 0
    j = 0
    for i in range(len(arr)):
        for j in range(len(arr)):
            if arr[i][j] == num:
                return i , j

#Main running code, and GUI the preset array and running the general search
initpuz = Node()
puzztype = input("Welcome to Rahul Sohi's 8-puzzler solver. Enter 1 to use a preset puzzle or 2 to enter your own ")
if (int(puzztype) == 1):
    initpuz.arr = [[1,3,6],[5,0,2],[4,7,8]]
if (int(puzztype) == 2):
    arr = list(map(int, input("Enter the first line with a space in bettween the numbers: ").split()))
    arr2 = list(map(int, input("Enter the second line with a space in bettween the numbers: ").split()))
    arr3 = list(map(int, input("Enter the first line with a space in bettween the numbers: ").split()))
    initpuz.arr = [arr, arr2, arr3]
queue_type = input("What hueristic would you like: \n (1) for Uniform Cost Search, (2) for Misplaced Tiles, or (3) Manhattan Distance? ")
generalsearch(initpuz, int(queue_type))
