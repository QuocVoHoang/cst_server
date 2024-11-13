import numpy as np
import heapq
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import time


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


df_cost = pd.read_csv('data/final_matrix_length.csv')
df_capacity = pd.read_csv('data/final_matrix_bike.csv')


cost_matrix = df_cost.iloc[:, 1:].to_numpy() 
capacity_matrix = df_capacity.iloc[:, 1:].to_numpy()



def get_result_min_cost_max_flow(cost_matrix, capacity_matrix, source, sink,nodes):
    max_flow, min_cost, paths = min_cost_max_flow(cost_matrix, capacity_matrix, source, sink)
    return max_flow, min_cost

nodes = list(df_cost.columns)

start_location = "Sân bay Tân Sơn Nhất"
end_location = "Ngã tư Bảy Hiền"

start_time = time.time()
try:
    start_index = nodes.index(start_location)
    end_index = nodes.index(end_location)
    print('Dijkstra')
    print('from: Sân bay Tân Sơn Nhất')
    print('to: Ngã tư Bảy Hiền')
    max_flow, min_cost = get_result_min_cost_max_flow(cost_matrix, capacity_matrix, start_index,end_index,nodes)
    print(f"Max flow: {max_flow} - Min cost: {min_cost}")
    end_time = time.time()
    print(f'Program runs in {round(end_time - start_time, 4)}s')
except ValueError:
    print("Điểm đi hoặc điểm đến không có trong danh sách.")