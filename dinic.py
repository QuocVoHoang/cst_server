from collections import deque
import pandas as pd

def bfs(source, sink, level, size, adjacency_matrix):
  for i in range(size):
    level[i] = -1
  level[source] = 0
  queue = deque([source])
  while queue:
    u = queue.popleft()
    for v in range(size):
      if level[v] < 0 and adjacency_matrix[u][v] > 0:
        level[v] = level[u] + 1
        queue.append(v)
  return level[sink] >= 0

def dfs(u, flow, sink, level, start, size, adjacency_matrix):
  if u == sink:
    return flow
  while start[u] < size:
    v = start[u]
    if level[v] == level[u] + 1 and adjacency_matrix[u][v] > 0:
      curr_flow = min(flow, adjacency_matrix[u][v])
      temp_flow = dfs(v, curr_flow, sink, level, start, size, adjacency_matrix)
      if temp_flow > 0:
        adjacency_matrix[u][v] -= temp_flow
        adjacency_matrix[v][u] += temp_flow
        return temp_flow
    start[u] += 1
  return 0

def dinic_maxflow(size, source, sink, adjacency_matrix):
  max_flow = 0
  level = [-1] * size
  while bfs(source, sink, level, size, adjacency_matrix):
    start = [0] * size
    while True:
      flow = dfs(source, float('Inf'), sink, level, start, size, adjacency_matrix)
      if flow == 0:
        break
      max_flow += flow
  return max_flow

def dinic_main_function(vehicle: str, start_location_name: str, end_location_name: str):
  if start_location_name == end_location_name:
    return 0
  else:
    if vehicle == 'car':
      vehicle_data = pd.read_csv('data/final_matrix_car.csv')
    elif vehicle == 'bike':
      vehicle_data = pd.read_csv('data/final_matrix_bike.csv')

    vehicle_data = vehicle_data.drop(columns=['Unnamed: 0'])
    adjacency_matrix = vehicle_data.values.tolist()
    matrix_size = len(adjacency_matrix)

    source = vehicle_data.columns.get_loc(start_location_name)
    sink = vehicle_data.columns.get_loc(end_location_name)
    
    result = dinic_maxflow(
      size=matrix_size, 
      source=source, 
      sink=sink, 
      adjacency_matrix=adjacency_matrix
    )
    return result

print(dinic_main_function('bike', 'Sân bay Tân Sơn Nhất', 'Ngã tư Bảy Hiền'))