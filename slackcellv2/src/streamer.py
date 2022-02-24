import queue


class DataStreamer:
    """Shameless copied from https://github.com/MaxHalford/flask-sse-no-deps"""

    def __init__(self):
        self.listeners = []

    def listen(self):
        self.listeners.append(queue.Queue(maxsize=10))
        return self.listeners[-1]

    def stream(self, data, event=None):
        # We go in reverse order because we might have to delete an element,
        # which will shift theindices backward
        msg = f'data: {data}\n\n'
        if event is not None:
            msg = f'event: {event}\n{msg}'

        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]
