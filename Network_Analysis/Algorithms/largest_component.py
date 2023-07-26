# undirect graph: largest componet aka largest island
from pprint import pprint

def main():

    graph = {
        0:[8,1,5],
        1:[0],
        5:[0,8],
        8:[0,5],
        2:[3,4],
        3:[2,4],
        4:[3,2]
    }

    largest = largestComponent(graph)

    pprint(largest)


def largestComponent(graph):
    #create a set of visited nodes, so he won't check them again
    visited = set()
    # set largest value to 0
    cnt = 0
    # if bigger than largest value, update largest value
    for node in graph.keys():
        init = explore_cnt(graph ,node, visited)
        if init > cnt: cnt = init

    return cnt 

# each node belongs to an island only
def explore_cnt(graph, node, visited):
    # if the node has already been checked, do not checked twice
    if node in visited: return 0

    visited.add(node)
    # set initial size of the node/island to 1
    size = 1 
    # add one for each new node explored from this point
    for neighbor in graph[node]:
        size += explore_cnt(graph, neighbor, visited)
    
    return size


if __name__ == "__main__":
    main()