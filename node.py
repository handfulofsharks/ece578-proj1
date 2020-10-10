from distrib import generateDistribution as gen_dist
import numpy as np
from queue import Queue
from enum import Enum
class State(Enum):
    idle = 0
    ready_to_transmit = 1
    waiting_to_transmit = 2
    transmitting = 3

class Node:

    def __init__(self, sim_params, frame_rate, seed=None):
        self.ack = sim_params.ACK_dur
        self.backoff = None
        self.difs_duration = sim_params.DIFS_dur
        self.cw_0 = sim_params.CW_0
        self.cw = self.cw_0
        self.sifs_duration = sim_params.SIFS_dur
        self.frame_distribution = gen_dist(frame_rate,
                                           sim_params.max_sim_time_sec,
                                           seed=seed)
        self.frame_idx = 0
        self.state = State.idle
        self.queue = Queue(maxsize=len(self.frame_distribution))

    def check_packet_ready(self, slot):
        if slot == self.frame_distribution[self.frame_idx]:
            self.queue.put(slot)
            if self.frame_idx < len(self.frame_distribution) - 1:
                self.frame_idx += 1 
        if self.state == State.transmitting:
            return
        elif not self.queue.empty() and self.state != State.waiting_to_transmit:
            self.state = State.ready_to_transmit
        else:
            self.state = State.idle

    def calc_backoff(self):
        self.backoff = np.random.randint(0, self.cw-1)