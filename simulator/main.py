import server
import heapq
from event import Event
from job_generator import JobGenerator

event_queue = []
event_publish_queue = []
s = []
P = []
K = 3
time_min = 30
max_timestamp = time_min * 60 * 1000

Servers = [server.Server(i,s[i],event_queue,event_publish_queue,P[i]) for i in range(k)]

JobGenerator = JobGenerator(1/4, Servers[0])

while event_queue[0].timestamp < max_timestamp:
    JobGenerator.tick()
    for s in Servers:
        s.tick()

    for event in event_publish_queue:
        heapq.heappush(event_queue, event)

    event_publish_queue.clear()
