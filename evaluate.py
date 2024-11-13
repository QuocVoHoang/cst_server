import pandas as pd
import time
from dinic import dinic_main_function
from push_relabel import push_relabel_main_function
from edmonds_karp import edmonds_karp_main_function

def read_node():
  json_path = 'data/locations200.json'
  node200 = pd.read_json(json_path)
  node200 = node200.values.tolist()
  return node200

node200 = read_node()
node200 = node200

first_half_node = node200
last_half_node = node200[::-1]

start = time.time()

def dinic():
  ################# dinic
  for i in range(len(first_half_node)):
    maxFlow = dinic_main_function(
      vehicle='bike',
      start_location_name=first_half_node[i][0], 
      end_location_name=last_half_node[i][0]
    )
  dinic_end = time.time()
  print(f'dinic         |  {round(dinic_end - start, 5)}')

def push_relabel():
  for i in range(len(first_half_node)):
    maxFlow = push_relabel_main_function(
      vehicle='bike',
      start_location_name=first_half_node[i][0], 
      end_location_name=last_half_node[i][0]
    )
  push_relabel_end = time.time()
  print(f'push_relabel  |  {round(push_relabel_end - start, 5)}')
  
  
def edmonds_karp():
  for i in range(len(first_half_node)):
    maxFlow = edmonds_karp_main_function(
      vehicle='bike',
      start_location_name=first_half_node[i][0], 
      end_location_name=last_half_node[i][0]
    )
  edmonds_karp_end = time.time()
  print(f'edmonds_karp  |  {round(edmonds_karp_end - start, 5)}')

print(f"===== TIME FOR FINDING {len(node200)} MAX FLOWS =====")
print("Algorithm     | time (in second)")
print('------------------------------')
dinic()
print('------------------------------')
push_relabel()
print('------------------------------')
edmonds_karp()