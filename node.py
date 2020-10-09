import distrib
import numpy as np
import queue
class Node:

    def __init__(self, seed=None):
        self.difs_duration = 2
        self.cw_0 = 4
        self.cw = self.cw_0
        self.sifs_duration = 2
        self.frame_distribution = distrib.generateDistribution(200, 10, seed=seed)
        self.frame_idx = 0
        self.ready = False
        self.queue = queue.Queue()

    def check_packet_ready(self, slot):
        if slot == self.frame_distribution[self.frame_idx]:
            self.queue.put(slot)
        self.ready = not self.queue.empty()

    def is_ready(self, slot):
        return self.ready

    def calc_backoff(self):
        self.backoff = np.random.randint(0, self.cw-1)