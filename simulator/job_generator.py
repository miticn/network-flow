import numpy as np
from event import Event

class JobGenerator:
    def __init__(self, alpha,  event_queue: list[Event], max_timestamp: int ):
        self.average_generation_time = 1/alpha
        self.event_queue = event_queue
        self.exponential_values_n = 3000000
        self.exponential_values = np.random.exponential(self.average_generation_time, size=self.exponential_values_n)
        self.exponential_index = 1
        self.event_queue.append(Event(self.exponential_values[0], -1, 0))
        self.max_timestamp = max_timestamp

    def tick(self):
        timestamp = self.exponential_values[self.exponential_index] + self.event_queue[0].timestamp
        self.exponential_index = (self.exponential_index + 1) % self.exponential_values_n
        if timestamp < self.max_timestamp:
            self.event_queue.append(Event(timestamp, -1, 0))
