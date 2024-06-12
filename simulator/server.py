#server class
from event import Event
import heapq
import numpy as np

class Server:
    def __init__(self, id: int, s : int, event_queue: list[Event], event_publish_queue: list[Event], P_array: list[int]):
        self.job_queue = []
        self.timestamp = 0
        self.ticks_working = 0
        self.jobs_done = 0
        self.event_queue = event_queue
        self.id = id
        self.s = s
        self.event_publish_queue = event_publish_queue
        self.P_array = P_array

    def get_J(self):
        return len(self.job_queue)
    
    def tick(self):
        if len(self.job_queue) > 0:
            self.ticks_working += self.timestamp - self.event_queue[0].timestamp
        self.timestamp = self.event_queue[0].timestamp
        
        if self.event_queue[0].fromm == self.id:
            self.job_queue.pop(0)
            self.jobs_done += 1
            if len(self.job_queue) > 0:
                pass
        if self.event_queue[0].to == self.id:
            self.job_queue.append(self.event_queue[0].timestamp)
            if len(self.job_queue) == 1:
                pass
            
    def emitEvent(self, event: Event):
        timestamp = np.random.exponential(self.s) + self.timestamp
        to = np.random.choice(len(self.P_array), p=self.P_array)

        self.event_publish_queue.append(Event(timestamp, self.id, to))


    def get_U(self):
        return self.ticks_working/self.timestamp
    
    def get_X(self):
        return self.jobs_done/self.timestamp  # throughput