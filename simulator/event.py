class Event(object):
    def __init__(self, timestamp: int, fromm: int, to : int):
        self.timestamp = timestamp
        self.fromm = fromm
        self.to = to
        self.marked = False

    def __repr__(self):
        return f'Node value: {self.timestamp}, from: {self.fromm}, to: {self.to}'

    def __lt__(self, other):
        return self.timestamp < other.timestamp