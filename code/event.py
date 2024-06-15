class Event(object):
    def __init__(self, timestamp: int, fromm: int, to : int, timestamp_start: int = None):
        self.timestamp = timestamp
        if timestamp_start == None:
            self.timestamp_start = timestamp
        else:
            self.timestamp_start = timestamp_start
        self.fromm = fromm
        self.to = to

    def __repr__(self):
        return f'Node value: {self.timestamp}, from: {self.fromm}, to: {self.to}'

    def __lt__(self, other):
        return self.timestamp < other.timestamp