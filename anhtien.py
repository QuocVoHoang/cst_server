import numpy as np
import heapq
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


def dijkstra(cost_matrix, capacity_matrix, source, sink, parent):
    num_nodes = len(cost_matrix)
    distances = [float('inf')] * num_nodes
    distances[source] = 0
    parent[source] = -1
    priority_queue = [(0, source)]  

    while priority_queue:
        dist_u, u = heapq.heappop(priority_queue)

        if dist_u > distances[u]:
            continue

        for v in range(num_nodes):
            if capacity_matrix[u][v] > 0 and distances[v] > distances[u] + cost_matrix[u][v]:
                distances[v] = distances[u] + cost_matrix[u][v]
                parent[v] = u
                heapq.heappush(priority_queue, (distances[v], v))

    return distances[sink] != float('inf')

def get_path(parent, sink):
    path = []
    v = sink
    while v != -1:
        path.append(v)
        v = parent[v]
    path.reverse()
    return path

def get_path(parent, sink):
    path = []
    v = sink
    while v != -1:
        path.append(v)
        v = parent[v]
    path.reverse()
    return path

def min_cost_max_flow(cost_matrix, capacity_matrix, source, sink):
    num_nodes = len(cost_matrix)
    parent = [-1] * num_nodes
    max_flow = 0
    min_cost = 0
    paths = []  

    while dijkstra(cost_matrix, capacity_matrix, source, sink, parent):
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, capacity_matrix[u][v])
            v = parent[v]

        v = sink
        path = [] 
        while v != source:
            u = parent[v]
            capacity_matrix[u][v] -= path_flow
            capacity_matrix[v][u] += path_flow
            min_cost += path_flow * cost_matrix[u][v]
            path.append((u, v)) 
            v = parent[v]
        
        max_flow += path_flow
        paths.append((get_path(parent, sink), path_flow))  

    return max_flow, min_cost, paths



df_capacity = pd.read_csv('data/mock_flow.csv')
df_cost = pd.read_csv('data/mock_length.csv')


cost_matrix = df_cost.iloc[:, 1:].to_numpy() 
capacity_matrix = df_capacity.iloc[:, 1:].to_numpy()


def get_result_min_cost_max_flow(cost_matrix, capacity_matrix, source, sink,nodes):
    max_flow, min_cost, paths = min_cost_max_flow(cost_matrix, capacity_matrix, source, sink)
    print("Lưu lượng tối đa là:", max_flow)
    print("Chi phí tối thiểu:", min_cost)
    print("Các đường đi ngắn nhất và luồng của từng đường đi:")

    # for path, flow in paths:
    #     print("Đường đi:", " -> ".join(map(lambda x: nodes[x], path)), "| Luồng:", flow)



nodes = list(df_cost.columns)
start_location = "A"
end_location = "E"

# Tìm chỉ số của điểm đi và điểm đến
try:
    start_index = nodes.index(start_location)
    end_index = nodes.index(end_location)
    get_result_min_cost_max_flow(cost_matrix, capacity_matrix, start_index,end_index,nodes)
except ValueError:
    print("Điểm đi hoặc điểm đến không có trong danh sách.")