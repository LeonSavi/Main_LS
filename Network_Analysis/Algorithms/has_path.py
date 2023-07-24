
########################
### for DIRECT GRAPH ###
########################

# acycle path: a path that starts where it begins.
# does a path exist between two nodes???


def main():
    graph = {
        'f': ['g','i'],
        'g': ['h'],
        'h': [],
        'i': ['g','h'],
        'j': ['i'],
        'k': []
    }

    print('first depth approach')
    hasPath(graph, 'f', 'i')

    print('first breadth approach')
    hasPath_fb(graph, 'f', 'i')

    
# if there is a pth between the source (src) and destination (dst)

def hasPath(graph, src, dst): 
    if src == dst: return True

    for neighbor in graph[src]:
        if hasPath(graph, neighbor, dst) == True:
            return True#, print(True)
        
    return False#,print(False),print(src)


def hasPath_fb(graph, src, dst):
    queue = [src]

    while len(queue) > 0:
        current = queue.pop(0)

        if current == dst:
            return True
        
        for neighbor in graph[current]:
            queue.append(neighbor)
    
    return False


if __name__ == "__main__":
    main()
