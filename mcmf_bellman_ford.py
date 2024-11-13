
from sys import maxsize
from typing import List
import pandas as pd
import time

found = []
N = 0
cap = []

flow = []
cost = []

dad = []
dist = []
pi = []

INF = maxsize 

def search(src: int, sink: int) -> bool:
	found = [False for _ in range(N)]
	dist = [INF for _ in range(N + 1)]
	dist[src] = 0

	while (src != N):
		best = N
		found[src] = True
  
		for k in range(N):
			if (found[k]):
				continue

			if (flow[k][src] != 0):
				val = (dist[src] + pi[src] -
						pi[k] - cost[k][src])

				if (dist[k] > val):
					dist[k] = val
					dad[k] = src

			if (flow[src][k] < cap[src][k]):
				val = (dist[src] + pi[src] -
						pi[k] + cost[src][k])

				if (dist[k] > val):
					dist[k] = val
					dad[k] = src

			if (dist[k] < dist[best]):
				best = k
		src = best

	for k in range(N):
		pi[k] = min(pi[k] + dist[k], INF)
	return found[sink]

def getMaxFlow(
  capi: List[List[int]], 
  costi: List[List[int]], 
  src: int, sink: int
  ) -> List[int]:

	global cap, cost, found, dist, pi, N, flow, dad
	cap = capi
	cost = costi

	N = len(capi)
	found = [False for _ in range(N)]
	flow = [[0 for _ in range(N)]
			for _ in range(N)]
	dist = [INF for _ in range(N + 1)]
	dad = [0 for _ in range(N)]
	pi = [0 for _ in range(N)]

	totflow = 0
	totcost = 0

	while (search(src, sink)):
		amt = INF
		x = sink
		
		while x != src:
			amt = min(
				amt, flow[x][dad[x]] if
				(flow[x][dad[x]] != 0) else
				cap[dad[x]][x] - flow[dad[x]][x])
			x = dad[x]

		x = sink
		
		while x != src:
			if (flow[x][dad[x]] != 0):
				flow[x][dad[x]] -= amt
				totcost -= amt * cost[x][dad[x]]

			else:
				flow[dad[x]][x] += amt
				totcost += amt * cost[dad[x]][x]
				
			x = dad[x]

		totflow += amt
	return [totflow, totcost]

if __name__ == "__main__":
  start_time = time.time()
  
  vehicle_data = pd.read_csv('data/final_matrix_bike.csv')
  length_data = pd.read_csv('data/final_matrix_length.csv')

  vehicle_data = vehicle_data.drop(columns=['Unnamed: 0'])
  length_data = length_data.drop(columns=['Unnamed: 0'])
  
  source = vehicle_data.columns.get_loc("Sân bay Tân Sơn Nhất")
  sink = vehicle_data.columns.get_loc("Ngã tư Bảy Hiền")

  cap = vehicle_data.values.tolist()
  cost = length_data.values.tolist()

  result = getMaxFlow(cap, cost, source, sink)
  print("Bellman-Ford")
  print('from: Sân bay Tân Sơn Nhất')
  print('to: Ngã tư Bảy Hiền')
  print("Max flow: {} - Min cost: {}".format(result[0], result[1]))
 
  end_time = time.time()
  print(f"The program runs in {round(end_time - start_time, 4)}s")
