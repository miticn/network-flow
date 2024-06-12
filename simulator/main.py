import server
import heapq
from event import Event
from job_generator import JobGenerator
from exit_node import ExitNode
from util import *
import time

import csv


def simulate(K:int, alpha: int, r: int, time_min : int = 30, MAX_K: int = 5):
    event_queue = []
    heapq.heapify(event_queue)
    s = [4, 10, 15, 15, 25, 25, 25, 25, 25]
    P = get_P_matrix(K)

    exit_column = np.zeros((P.shape[0], 1))
    for i in range(K):
        exit_column[-i-1] = 1

    P = np.hstack((P, exit_column))

    
    max_timestamp = time_min * 60 * 1000

    Servers = [server.Server(i,s[i],event_queue,P[i]) for i in range(K+4)]

    jobGenerator = JobGenerator(alpha/1000*r, event_queue, max_timestamp)
    exitNode = ExitNode(6, event_queue)

    first = True
    while len(event_queue)!=0 or first:
        first = False
        jobGenerator.tick()
        for s in Servers:
            s.tick()

        exitNode.tick()
        #print(event_queue)
        heapq.heappop(event_queue)


    padding = ["" for i in range(K,MAX_K)] 
    result = [K]+ [r]+ [exitNode.get_T()/1000] + [s.get_U() for s in Servers] + padding +\
             [s.get_X()*1000 for s in Servers] + padding + \
             [s.get_J() for s in Servers] + padding
    return result


start_time = time.time()

alpha_k = {2: 79.19999999999999, 3:118.8, 4:158.39999999999998, 5:158.4}
r_list = [0.30, 0.55, 0.80, 1.00]

results = []
def run_simulation(k, r):
    return simulate(k, alpha_k[k], r)

from concurrent.futures import ProcessPoolExecutor
with ProcessPoolExecutor() as executor:
    futures = [executor.submit(run_simulation, k, r) for k in range(2, 6) for r in r_list]
    for future in futures:
        results.append(future.result())

end_time = time.time()
execution_time = end_time - start_time

with open('rezultati_simulacija.csv', 'w', newline='') as csvfile:
    header = ['K', 'r', 'T', 'Ucpu', 'Uds1', 'Uds2', 'Uds3', 'Udu1', 'Udu2', 'Udu3', 'Udu4', 'Udu5',
                  'Xcpu', 'Xds1', 'Xds2', 'Xds3', 'Xdu1', 'Xdu2', 'Xdu3', 'Xdu4', 'Xdu5',
                  'Jcpu', 'Jds1', 'Jds2', 'Jds3', 'Jdu1', 'Jdu2', 'Jdu3', 'Jdu4', 'Jdu5']
    writer = csv.writer(csvfile)
    writer.writerow(header)
    for result in results:
        writer.writerow(result)
print(f"Execution time: {execution_time} seconds")