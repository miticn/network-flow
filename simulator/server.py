#server class
from event import Event
import heapq
import numpy as np

class Server:
    def __init__(self, id: int, s : int, event_queue: list[Event], P_array: list[int]):
        self.job_queue = []
        self.timestamp = 0
        self.ticks_working = 0
        self.jobs_done = 0
        self.event_queue = event_queue
        self.id = id
        self.s = s
        self.P_array = P_array
        self.J_Jobs = 0

    def get_J(self):
        return self.J_Jobs/self.timestamp
    
    def tick(self):
        if len(self.event_queue) == 0:
            return
        if len(self.job_queue) > 0:
            self.ticks_working += self.event_queue[0].timestamp - self.timestamp
            self.J_Jobs += (self.event_queue[0].timestamp - self.timestamp) * len(self.job_queue)
        self.timestamp = self.event_queue[0].timestamp
        
        if self.event_queue[0].fromm == self.id:
            self.job_queue.pop(0)
            self.jobs_done += 1
            if len(self.job_queue) > 0:
                self.emitEvent()
        if self.event_queue[0].to == self.id:
            self.job_queue.append((self.event_queue[0].timestamp, self.event_queue[0].timestamp_start))
            if len(self.job_queue) == 1:
                self.emitEvent()
            
    def emitEvent(self):
        timestamp = np.random.exponential(self.s) + self.timestamp
        #print(self.P_array)
        to = np.random.choice(len(self.P_array), p=self.P_array)

        heapq.heappush(self.event_queue, Event(timestamp, self.id, to, self.job_queue[0][1]))


    def get_U(self):
        return self.ticks_working/self.timestamp
    
    def get_X(self):
        return self.jobs_done/self.timestamp  # throughput