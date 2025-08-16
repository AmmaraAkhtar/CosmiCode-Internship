def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0  
    
    visited = set()

    while len(visited) < len(graph):
        min_node = None
        for node in graph:
            if node not in visited:
                if min_node is None or dist[node] < dist[min_node]:
                    min_node = node
        if min_node is None:
            break

        for neighbor, weight in graph[min_node].items():
            new_dist = dist[min_node] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist

        visited.add(min_node)

    return dist

graph = {
    'A': {'B': 4, 'C': 2},
    'B': {'A': 4, 'C': 1, 'D': 5},
    'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
    'D': {'B': 5, 'C': 8, 'E': 2, 'Z': 6},
    'E': {'C': 10, 'D': 2, 'Z': 3},
    'Z': {'D': 6, 'E': 3}
}


print(dijkstra(graph, 'A'))
