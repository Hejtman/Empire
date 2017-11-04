from Game.base.utils import calculate_time


class Queue:
    def __init__(self, finished):
        self.finished = finished
        self.performing = None
        self.finish_time = None

    def start(self, performing, cost, time_now, resources):
        self.performing = performing
        self.finish_time = time_now + calculate_time(cost, resources)

    def finish(self):
        self.finished[self.performing] += 1
        self.performing = None
        self.finish_time = None
