import numpy as np
from server import Server
from event import Event

class JobGenerator:
    def __init__(self, alpha,  event_queue: list[Event], event_publish_queue: list[Event]):
        self.average_generation_time = 1/alpha
        self.time_to_generation_event = np.random.exponential(self.average_generation_time)
        self.event_queue = event_queue
        self.event_publish_queue = event_publish_queue

    def tick(self):
        pass
