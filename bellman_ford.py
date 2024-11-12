import sys
import time
import pandas as pd

# Hàm Bellman-Ford để tìm đường đi tối ưu (với chi phí nhỏ nhất)
def bellman_ford(graph, source, n, capacity, cost, flow):
    dist = [float('inf')] * n
    dist[source] = 0
    parent = [-1] * n

    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if capacity[u][v] - flow[u][v] > 0 and dist[u] + cost[u][v] < dist[v]:
                    dist[v] = dist[u] + cost[u][v]
                    parent[v] = u

    return dist, parent

# Hàm cập nhật lưu lượng trên các cạnh (điều chỉnh theo dòng chảy)
def update_flow(flow, parent, source, sink, n):
    path_flow = float('inf')
    s = sink
    while s != source:
        path_flow = min(path_flow, capacity[parent[s]][s] - flow[parent[s]][s])
        s = parent[s]
    
    v = sink
    while v != source:
        u = parent[v]
        flow[u][v] += path_flow
        flow[v][u] -= path_flow
        v = parent[v]
    
    return path_flow

# Hàm tìm Min-Cost Max-Flow
def min_cost_max_flow(n, capacity, cost, source, sink):
    flow = [[0] * n for _ in range(n)]  # Dòng chảy khởi tạo là 0
    max_flow = 0
    min_cost = 0

    while True:
        dist, parent = bellman_ford(capacity, source, n, capacity, cost, flow)

        # Nếu không tìm thấy đường đi từ source đến sink, kết thúc
        if dist[sink] == float('inf'):
            break

        # Cập nhật dòng chảy cho đường đi tối ưu vừa tìm được
        path_flow = update_flow(flow, parent, source, sink, n)

        # Cộng dồn max flow và chi phí
        max_flow += path_flow
        min_cost += path_flow * dist[sink]

    return max_flow, min_cost


# n = 5
# capacity = [ 
#     [ 0, 3, 1, 0, 3 ], 
#     [ 0, 0, 2, 0, 0 ], 
#     [ 0, 0, 0, 1, 6 ], 
#     [ 0, 0, 0, 0, 2 ],
#     [ 0, 0, 0, 0, 0 ] 
# ]

# cost = [ 
#     [ 0, 2, 0, 0, 2 ], 
#     [ 0, 0, 0, 3, 0 ], 
#     [ 0, 0, 0, 0, 0 ], 
#     [ 0, 0, 0, 0, 1 ],
#     [ 0, 0, 0, 0, 0 ] 
# ]

start_time = time.time()

vehicle_data = pd.read_csv('data/final_matrix_bike.csv')
length_data = pd.read_csv('data/final_matrix_length.csv')

vehicle_data = vehicle_data.drop(columns=['Unnamed: 0'])
length_data = length_data.drop(columns=['Unnamed: 0'])

source = vehicle_data.columns.get_loc("AEON Mall Bình Tân")
sink = vehicle_data.columns.get_loc("Bệnh viện Nhi Đồng 1")

capacity = vehicle_data.values.tolist()
cost = length_data.values.tolist()

n = len(capacity)

max_flow, min_cost = min_cost_max_flow(n, capacity, cost, source, sink)
print('from: AEON Mall Bình Tân')
print('to: Bệnh viện Nhi Đồng 1')
print("Max flow: {} - Min cost: {}".format(max_flow, min_cost))

end_time = time.time()
total_function_time = round(end_time - start_time, 4)
print(f"The program runs in {total_function_time}s")
