from event import Event
class ExitNode:
    def __init__(self, id: int, event_queue: list[Event]) -> None:
        self.id = id
        self.event_queue = event_queue
        self.jobs_done = 0
        self.cumulative_time = 0

    def tick(self):
        self.jobs_done += 1
        #print(self.event_queue[0].timestamp, self.event_queue[0].timestamp_start)
        self.cumulative_time += self.event_queue[0].timestamp - self.event_queue[0].timestamp_start

    def get_T(self):
        #print(self.cumulative_time)
        #print(self.jobs_done)
        return self.cumulative_time/self.jobs_done