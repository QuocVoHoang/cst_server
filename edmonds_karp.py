import csv

def read_graph_from_csv(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)
        
    node_names = data[0][1:]  
    vertices = len(node_names)
    graph = Graph(vertices)
    graph.node_names = node_names

    for i in range(1, vertices + 1):
        for j in range(1, vertices + 1):
            if float(data[i][j]) > 0:
                graph.add_edge(i - 1, j - 1, float(data[i][j]))
    return graph

class Graph:
    def __init__(self, size):
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [''] * size

    def add_edge(self, u, v, c):
        self.adj_matrix[u][v] = c

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def bfs(self, s, t, parent):
        visited = [False] * self.size
        queue = []  
        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.pop(0) 

            for ind, val in enumerate(self.adj_matrix[u]):
                if not visited[ind] and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
        return visited[t]
    
    def get_node_index(self, node_name):
        if node_name in self.node_names:
            return self.node_names.index(node_name)
        else:
            raise ValueError(f"Node name '{node_name}' not found in the graph.")


    def edmonds_karp(self, source, sink):
        parent = [-1] * self.size
        max_flow = 0

        while self.bfs(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            while(s != source):
                path_flow = min(path_flow, self.adj_matrix[parent[s]][s])
                s = parent[s]

            max_flow += path_flow
            v = sink
            while(v != source):
                u = parent[v]
                self.adj_matrix[u][v] -= path_flow
                self.adj_matrix[v][u] += path_flow
                v = parent[v]

            path = []
            v = sink
            while(v != source):
                path.append(v)
                v = parent[v]
            path.append(source)
            path.reverse()
        return max_flow


def edmonds_karp_main_function(vehicle: str, start_location_name: str, end_location_name: str):
    if start_location_name == end_location_name:
        return 0
    else:
        if vehicle == 'car':
            graph = read_graph_from_csv('data/final_matrix_car.csv')
        elif vehicle == 'bike':
            graph = read_graph_from_csv('data/final_matrix_bike.csv')

        source = graph.get_node_index(start_location_name)
        sink = graph.get_node_index(end_location_name)
        
        edmonds_karp = graph.edmonds_karp(source, sink)
        
        return edmonds_karp

# print(edmonds_karp_main_function('bike', 'Sân bay Tân Sơn Nhất', 'Ngã tư Bảy Hiền'))