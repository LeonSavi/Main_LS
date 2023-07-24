# Create a dictionary of adjacencys for a direct graph

graph = {
    'a': ['b','c'],
    'b': ['d'],
    'c': ['e'],
    'd': ['f'],
    'e': [],
    'f': []
}

# depth first traversal algorithm
# starting from 'a': a,b,d... but you can do also a,c,e,b,d
# explore a direcntion as much as possible before changing direction
# stack algorithm: 

#breadth first traversal
# starting from 'a': a,b,c,...
# explore all the neighbor from a starting point, explore eveything evenly
# queue algorithm: first in first out

# both algo explore the same nodes

print('First Traversal Iterative')
def depthFirstPrint(graph, source):
    stack = [source]
    
    while len(stack) > 0:
        current = stack.pop()
        print(current)
        
        for neighbor in graph[current]:
            stack.append(neighbor)

depthFirstPrint(graph, source = 'a')


print('First Traversal Recurseverly') # ok if there are dead-ends
def depthFirstPrintR(graph, source):
    print(source)

    for neighbor in graph[source]:
        depthFirstPrintR(graph, neighbor)

depthFirstPrintR(graph, source = 'a')


print('Breadth first Traversal')
def breadthFirstPrint(graph, source): 
    queue = [source]

    while len(queue) > 0:
        current = queue.pop(0)
        print(current)
        for neighbor in graph[current]:
            queue.append(neighbor)

breadthFirstPrint(graph, source = 'a')