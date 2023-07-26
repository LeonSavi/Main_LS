##### undirect graph #####
from pprint import pprint 


def main():
    
    edges = [
        ['i','j'],
        ['k','i'],
        ['m','k'],
        ['k','l'],
        ['o','n']
        ]
    
    adj_list = buildGraph(edges)
    pprint(hasPathInd(adj_list, 'i', 'l',set()))


# from edges list of list to adjency dictionary
def buildGraph(edges):

    graph = {}

    for edge in edges:
        a,b = edge

        if not a in graph.keys(): graph[a] = []
        if not b in graph.keys(): graph[b] = []

        graph[a].append(b)
        graph[b].append(a)

    return graph


# check if a path exists between two nodes 
# take care to possible infinite loops with the 'set' visited
def hasPathInd(graph,src,dst, visited):

    if src == dst: return True

    if src in visited: return False

    visited.add(src)

    for neighbor in graph[src]:
        if hasPathInd(graph,neighbor,dst,visited) == True:
            return True
        
    return False



if __name__ == "__main__":
    main()