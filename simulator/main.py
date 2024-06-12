import server
import heapq
from job_generator import JobGenerator
from exit_node import ExitNode
from util import *
import time

import csv
from collections import defaultdict


def simulate(K:int, alpha: int, r: int, P:np.ndarray, time_min : int = 30, MAX_K: int = 5):
    event_queue = []
    heapq.heapify(event_queue)
    s = np.array([4, 10, 15, 15, 25, 25, 25, 25, 25])
    #P = get_P_matrix(K)
    
    max_timestamp = time_min * 60 * 1000

    Servers = [server.Server(i,s[i],event_queue,P[i]) for i in range(K+4)]
    servers_len = len(Servers)
    jobGenerator = JobGenerator(alpha*r, event_queue, max_timestamp)
    exitNode = ExitNode(len(Servers))

    while len(event_queue) != 0:
        event = heapq.heappop(event_queue)
        if event.fromm == -1:
            jobGenerator.tick(event)
        else:
            Servers[event.fromm].tick_from(event)
        
        if event.to == servers_len:
            exitNode.tick(event)
        else:
            Servers[event.to].tick_to(event)


    padding = [0 for i in range(K,MAX_K)] 
    result = [K]+ [r]+ [exitNode.get_T()/1000] + [s.get_U() for s in Servers] + padding +\
             [s.get_X()*1000 for s in Servers] + padding + \
             [s.get_J() for s in Servers] + padding
    return result

def write_results_to_csv(filename, header, results):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for result in results:
            writer.writerow(result)


header = ['K', 'r', 'T', 'Ucpu', 'Uds1', 'Uds2', 'Uds3', 'Udu1', 'Udu2', 'Udu3', 'Udu4', 'Udu5',
          'Xcpu', 'Xds1', 'Xds2', 'Xds3', 'Xdu1', 'Xdu2', 'Xdu3', 'Xdu4', 'Xdu5',
          'Jcpu', 'Jds1', 'Jds2', 'Jds3', 'Jdu1', 'Jdu2', 'Jdu3', 'Jdu4', 'Jdu5']

start_time = time.time()

#create dictionary of P matrixes
P = {}
for i in range(2, 6):
    P[i] = get_P_matrix(i)

alpha_k = {2:0.07919999999999999, 3:0.1188, 4:0.15839999999999999, 5:0.1584}
r_list = [0.30, 0.55, 0.80, 1.00]

results = []

from concurrent.futures import ProcessPoolExecutor
with ProcessPoolExecutor() as executor:
    futures = [executor.submit(simulate, k, alpha_k[k], r, P[k]) for k in range(2, 6) for r in r_list]
    for future in futures:
        results.append(future.result())

end_time = time.time()
execution_time = end_time - start_time
write_results_to_csv('rezultati_simulacija.csv', header, results)
print(f"Execution time: {execution_time} seconds")


#100 iterations
start_time = time.time()
iterations = 100
results = defaultdict(list)

with ProcessPoolExecutor() as executor:
    futures = [executor.submit(simulate, k, alpha_k[k], r, P[k]) for k in range(2, 6) for r in r_list for i in range(iterations)]
    for future in futures:
        result = future.result()
        key = (result[0], result[1])  # Use (k, r) as the key
        results[key].append(result[2:])  # Store the rest of the result

averaged_results = []
for key, value_list in results.items():
    value_array = np.array(value_list)
    averaged_values = np.mean(value_array, axis=0)
    averaged_results.append([key[0], key[1]] + averaged_values.tolist())


end_time = time.time()
execution_time = end_time - start_time


print(f"Execution time: {execution_time} seconds")

write_results_to_csv('rezultati_simulacija_usrednjeno.csv', header, averaged_results)