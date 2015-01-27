import numpy as np


# TODO: rewrite all of this!!!

def finddegrees(adj):
    # number of nodes is just length of adj
    degrees = [0 for i in range(len(adj))]
    for i in range(len(adj)):
        number = 0
        for j in range(len(adj[i])):
            number += adj[i][j]
        list = [0 for k in range(int(number))]
        number2 = 0
        # list is list of nodes we're joined to, when we're joined twice, repeat the vertex with 2 links. can geenralise further by just doing for i in range(adj[i][j]) 
        for j in range(len(adj[i])):
            if adj[i][j] != 0:
                for s in range(int(adj[i][j])):
                    list[number2] = j
                    number2 += 1
        degrees[i] = list
    return degrees


# the array created above will give the column headings for the shift oeprator.use above function to create another list with first coin state index of each node, then add index from degree to get coin state we want.

# to find first coin state of each node create a number and ad degree of each node in order to it.

def firstnode(degree):
    number = 0
    array = [0 for i in range(len(degree))]
    for i in range(len(degree)):
        array[i] = number
        number += len(degree[i]) 
    return array


def forcoinstate(degree, i, j):
    number = 0
    # scroll through and add one each time its not equal, have another number to indicate whether we've got to the node or not, and therefore whether or not we should stop yet
    number2 = 0
    for k in range(len(degree[i])):
        if number2 == 0:
            if degree[i][k] != j:
                number += 1
            else:
                number2 = 1
    if number == len(degree[i]):
        return 'no link between nodes i and j'
    else:
        return number
        
    
    

def createshift(adj):
    degree = finddegrees(adj)
    nodeindex = firstnode(degree)
    # create matrix of correct size from degree, size is last index of firstnode plus degree of that node
    size = nodeindex[len(adj)-1] + len(degree[len(adj)-1])
    # remove duplicates otherwise things below get repeated. 
    degree2 = [[0] for i in range(len(degree))]
    for i in range(len(degree)):
        degree2[i] = list(set(degree[i]))
    array = np.zeros((size, size), dtype=int)
    # go through each node in turn to assign correct indices to links between coin states of each node
    for i in range(len(degree)):
        # index of first coin state of node we're on
        index1 = nodeindex[i]
        number = 0
       # scroll through nodes that node were on now is joined to
        for j in range(len(degree2[i])):
            nolinks = adj[degree2[i][j]][i]
            # don't want to just scroll through js here, need to select specific node
            number = forcoinstate(degree, i, degree[i][j])
            #print number
            coinstate1 = index1 + number
            # index of node coin state index1 + j joins to. find correct coin state there to link to by finding which index of degree[nextnode] gives the node we're on
            node = degree[i][j]
            for k in range(len(degree2[node])):
                if degree2[node][k] == i:
                    coinstate2 = nodeindex[node] + forcoinstate(degree, node, i)
            for k in range(int(nolinks)):
                array[coinstate1 + k][coinstate2 + k] = 1
    for i in range(len(array)):
        for j in range(len(array)):
            if array[i][j] == 1:
                array[j][i] = 1
    return array


