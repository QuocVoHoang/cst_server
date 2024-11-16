import csv
import sys

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.capacity = [[0] * vertices for _ in range(vertices)]
        self.node_names = []

    def add_edge(self, u, v, w):
        self.capacity[u][v] = w

    def get_node_index(self, node_name):
        if node_name in self.node_names:
            return self.node_names.index(node_name)
        else:
            raise ValueError(f"Node name '{node_name}' not found in the graph.")


def read_graph_from_csv(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)
        
    node_names = data[0][1:]  # First row contains node names
    vertices = len(node_names)
    graph = Graph(vertices)
    graph.node_names = node_names

    for i in range(1, vertices + 1):
        for j in range(1, vertices + 1):
            if float(data[i][j]) > 0:
                graph.add_edge(i - 1, j - 1, float(data[i][j]))

    return graph

class PushRelabel:
    def __init__(self, graph):
        self.graph = graph
        self.V = graph.V
        self.excess = [0] * self.V
        self.height = [0] * self.V
        self.flow = [[0] * self.V for _ in range(self.V)]

    def push(self, u, v):
        delta = min(self.excess[u], self.graph.capacity[u][v] - self.flow[u][v])
        self.flow[u][v] += delta
        self.flow[v][u] -= delta
        self.excess[u] -= delta
        self.excess[v] += delta

    def relabel(self, u):
        min_height = sys.maxsize
        for v in range(self.V):
            if self.graph.capacity[u][v] - self.flow[u][v] > 0:
                min_height = min(min_height, self.height[v])
        self.height[u] = min_height + 1

    def discharge(self, u):
        while self.excess[u] > 0:
            for v in range(self.V):
                if self.graph.capacity[u][v] - self.flow[u][v] > 0 and self.height[u] == self.height[v] + 1:
                    self.push(u, v)
                    if self.excess[u] == 0:
                        break
            else:
                self.relabel(u)

    def max_flow(self, source, sink):
        self.height[source] = self.V
        self.excess[source] = sys.maxsize
        for v in range(self.V):
            if self.graph.capacity[source][v] > 0:
                self.push(source, v)

        active = [i for i in range(self.V) if i != source and i != sink and self.excess[i] > 0]
        while active:
            u = active.pop(0)
            self.discharge(u)
            if self.excess[u] > 0:
                active.append(u)

        return sum(self.flow[source][v] for v in range(self.V))

def push_relabel_main_function(vehicle: str, start_location_name: str, end_location_name: str):
    if start_location_name == end_location_name:
        return 0
    else:
        if vehicle == 'car':
            graph = read_graph_from_csv('data/final_matrix_car.csv')
        elif vehicle == 'bike':
            graph = read_graph_from_csv('data/final_matrix_bike.csv')

        push_relabel = PushRelabel(graph)
        
        source = graph.get_node_index(start_location_name)
        sink = graph.get_node_index(end_location_name)
        max_flow_value = push_relabel.max_flow(source, sink)
        return max_flow_value

# print(push_relabel_main_function('bike', 'Sân bay Tân Sơn Nhất', 'Ngã tư Bảy Hiền'))