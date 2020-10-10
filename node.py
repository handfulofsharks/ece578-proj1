import distrib
import numpy as np
from queue import Queue
from enum import Enum
class State(Enum):
    idle = 0
    ready_to_transmit = 1
    waiting_to_transmit = 2
    transmitting = 3

class Node:

    def __init__(self, seed=None):
        self.backoff = None
        self.difs_duration = 2
        self.cw_0 = 4
        self.cw = self.cw_0
        self.sifs_duration = 2
        self.frame_distribution = distrib.generateDistribution(200, 10, seed=seed)
        self.frame_idx = 0
        self.state = State.idle
        self.queue = Queue(maxsize=len(self.frame_distribution))

    def check_packet_ready(self, slot):
        if slot == self.frame_distribution[self.frame_idx]:
            self.queue.put(slot)
        if not self.queue.empty():
            self.state = State.ready_to_transmit
        else:
            self.state = State.idle

    def calc_backoff(self):
        self.backoff = np.random.randint(0, self.cw-1)