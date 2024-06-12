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
        self.cumulative_probs = np.cumsum(self.P_array)
        if self.id <= 3:
            self.indicies_n = 3000000
            self.indicies_index = 0
            self.indicies = np.searchsorted(self.cumulative_probs, np.random.random(size=self.indicies_n), side="right")
        self.exponential_values_n = 3000000
        self.exponential_values = np.random.exponential(s, size=self.exponential_values_n)
        self.exponential_index = 0
        self.job_queue_len = len(self.job_queue)


    def get_J(self):
        return self.J_Jobs/self.timestamp
    
    def update_timestamp(self):
        #self.job_queue_len = len(self.job_queue)
        if self.job_queue_len != 0:
            self.ticks_working += self.event_queue[0].timestamp - self.timestamp
            self.J_Jobs += (self.event_queue[0].timestamp - self.timestamp) * self.job_queue_len
        self.timestamp = self.event_queue[0].timestamp
        
    def tick_from(self):
        self.update_timestamp()
        self.job_queue.pop(0)
        self.job_queue_len -= 1
        self.jobs_done += 1
        if self.job_queue_len != 0:
            self.emitEvent()

    def tick_to(self):
        self.update_timestamp()
        self.job_queue.append((self.event_queue[0].timestamp, self.event_queue[0].timestamp_start))
        self.job_queue_len += 1
        if self.job_queue_len == 1:
            self.emitEvent()
            
    def emitEvent(self):
        timestamp = self.exponential_values[self.exponential_index] + self.timestamp
        self.exponential_index = (self.exponential_index + 1) % self.exponential_values_n
        #print(self.P_array)

        if self.id > 3:
            to = len(self.P_array) - 1
        else:
            to = self.indicies[self.indicies_index]
            self.indicies_index = (self.indicies_index + 1) % self.indicies_n

        heapq.heappush(self.event_queue, Event(timestamp, self.id, to, self.job_queue[0][1]))


    def get_U(self):
        return self.ticks_working/self.timestamp
    
    def get_X(self):
        return self.jobs_done/self.timestamp  # throughput