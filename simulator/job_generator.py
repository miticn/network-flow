import numpy as np
from event import Event

class JobGenerator:
    def __init__(self, alpha,  event_queue: list[Event], max_timestamp: int ):
        self.average_generation_time = 1/alpha
        self.event_queue = event_queue
        self.event_queue.append(Event(np.random.exponential(self.average_generation_time), -1, 0))
        self.max_timestamp = max_timestamp

    def tick(self):
        if self.event_queue[0].fromm == -1:
            timestamp = np.random.exponential(self.average_generation_time) + self.event_queue[0].timestamp
            if timestamp < self.max_timestamp:
                self.event_queue.append(Event(timestamp, -1, 0))
