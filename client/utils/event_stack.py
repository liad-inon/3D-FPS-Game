from collections import deque

class EventStack:
    def __init__(self):
        self.stack = deque()

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.stack:
            return self.stack.popleft()
        else:
            raise StopIteration

    def push(self, event):
        self.stack.append(event)

