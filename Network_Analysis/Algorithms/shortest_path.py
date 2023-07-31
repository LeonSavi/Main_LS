from undirect_graph import buildGraph
from pprint import pprint

# shortest path can be defined as the shortest number of edges that i have to go
# through to get to node a to node b

# two approaches are possibles: breadth first traversal and depth first traversal

# BFT might be the best option as it explore gradually all the nodes close to the starting points

# Each time i explore a new node i add one to my distance: (node, distance)

# each time i need to visit the neighbor of a node: do not consider the old nodes

def main():

    edges = [
        ['w','x'],
        ['x','y'],
        ['z','y'],
        ['z','v'],
        ['w','v']
        ]
    
    graph_adj = buildGraph(edges)

    pprint(shortestPath(graph_adj, 'w', 'z'))


def shortestPath(graph, node1, node2):

    visited = set(node1)
    # list of lists
    queue = [[node1,0]]

    while len(queue) > 0:

        [node, distance] = queue.pop()

        if node == node2: return distance

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append([neighbor,distance+1])
    
    return -1



if __name__ == '__main__':
    main()
