from queue import Queue


class Scheduler(object):
    def __init__(self):
        self.q = Queue()

    def get(self):
        if not self.q.empty():
            return self.q.get_nowait()
        else:
            return None


scheduler = Scheduler()
