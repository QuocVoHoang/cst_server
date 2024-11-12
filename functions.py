import pandas as pd
from dinic import dinic_maxflow
import time

def dinic_main_function(vehicle: str, start_location_name: str, end_location_name: str):
  start_time = time.time()
  
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
  
  end_time = time.time()
  total_function_time = round(end_time - start_time, 4)
  print(f"Max flow from {start_location_name} to {end_location_name} is {result}")
  print(f"The dinic function runs in {total_function_time}s")
  return result
