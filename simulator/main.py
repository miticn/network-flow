import server
import heapq
from event import Event
from job_generator import JobGenerator
from exit_node import ExitNode
from util import *
import time

start_time = time.time()


event_queue = []
s = [4, 10, 15, 15, 25, 25, 25, 25, 25]
K = 2
P = get_P_matrix(K)

exit_column = np.zeros((P.shape[0], 1))
for i in range(K):
    exit_column[-i-1] = 1

P = np.hstack((P, exit_column))

time_min = 30
max_timestamp = time_min * 60 * 1000

Servers = [server.Server(i,s[i],event_queue,P[i]) for i in range(K+4)]

jobGenerator = JobGenerator(79.19999999999999/1000, event_queue, max_timestamp)
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



print("T", exitNode.get_T()/1000, "s")
for s in Servers:
    print("U",s.id, s.get_U())
    print("X",s.id, s.get_X()*1000)
    print("J",s.id, s.get_J())
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")