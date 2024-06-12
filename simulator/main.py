import server
import heapq
from event import Event
from job_generator import JobGenerator
from util import *

def publish_events(event_queue, event_publish_queue):
    for event in event_publish_queue:
        heapq.heappush(event_queue, event)
    event_publish_queue.clear()

event_queue = []
event_publish_queue = []
s = [4, 10, 15, 15, 25, 25, 25, 25, 25]
K = 3
P = get_P_matrix(K)

exit_column = np.zeros((P.shape[0], 1))
for i in range(K):
    exit_column[-i-1] = 1

P = np.hstack((P, exit_column))

time_min = 30
max_timestamp = time_min * 60 * 1000

Servers = [server.Server(i,s[i],event_queue,event_publish_queue,P[i]) for i in range(K+4)]

JobGenerator = JobGenerator(1/4, event_queue, event_publish_queue, max_timestamp)

publish_events(event_queue, event_publish_queue)

first = True
while len(event_queue)!=0 or first:
    first = False
    JobGenerator.tick()
    for s in Servers:
        s.tick()

    #print(event_queue)
    heapq.heappop(event_queue)
    publish_events(event_queue, event_publish_queue)
