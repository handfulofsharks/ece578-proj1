import math
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
        np.random.seed(seed)
        self.ack = sim_params.ACK_dur
        self.backoff = None
        self.difs_duration = sim_params.DIFS_dur
        self.cw_0 = sim_params.CW_0
        self.cw_max = sim_params.CW_max
        self.cw = self.cw_0
        self.sifs_duration = sim_params.SIFS_dur
        self.frame_distribution = self.gen_dist(frame_rate,
                                           sim_params.max_sim_time_sec)
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
        temp_cw = min(self.cw, self.cw_max)
        self.backoff = np.random.randint(0, temp_cw-1)
    def gen_dist(self, lam, t, t_slot=10e-6):
        u = np.random.uniform(size=(lam*t))
        x = [-(1/lam) * math.log(1-i) for i in u]
        x = [math.ceil(i/t_slot) for i in x]
        x = list(np.cumsum(x))
        return x