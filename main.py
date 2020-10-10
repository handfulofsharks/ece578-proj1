from node import Node, State
from channel import Channel
import math

A = Node(seed=3)
C = Node(seed=3)
channel = Channel()
collisions = 0
a_succ = 0
c_succ = 0

#number of slots for 10 seconds
max_slots = math.ceil(10/10e-6)

for slot in range(0, max_slots):
    #checks if a packet is ready for transmit and adds it to queue
    A.check_packet_ready(slot)
    C.check_packet_ready(slot)
    if not channel.is_idle:
        channel.idle_count -= 1
        if channel.idle_count <= 0:
            channel.is_idle = True
            channel.idle_count = 50

    if A.state == State.ready_to_transmit:
        if A.backoff is None:
            A.calc_backoff()
        A.state = State.waiting_to_transmit

    if C.state == State.ready_to_transmit:
        if C.backoff is None:
            C.calc_backoff()
        C.state = State.waiting_to_transmit

    if A.state == State.waiting_to_transmit:
        #wait until channel is idle for DIFS slots
        if channel.is_idle:
            A.difs_duration -= 1
        else:
            A.difs_duration = 2
        if A.difs_duration <= 0:
            #decrement backoff slots
            if channel.is_idle:
                A.backoff -= 1
                if A.backoff <= 0:
                    #transmit
                    A.state = State.transmitting
                    a_succ += 1
                    A.backoff = None
    if C.state == State.waiting_to_transmit:
        if channel.is_idle:
            C.difs_duration -= 1
        else:
            C.difs_duration = 2
        if C.difs_duration <= 0:
            C.backoff -= 1
            if C.backoff <= 0:
                C.state = State.transmitting
                c_succ += 1
                C.backoff = None
                
    if A.state == State.transmitting and C.state == State.transmitting:
        #collision
        print("collision")
        A.cw = A.cw * 2
        A.backoff = None
        C.cw = C.cw * 2
        collisions += 1
        C.backoff = None
    if A.state == State.transmitting or C.state == State.transmitting:
        channel.is_idle = False

import pdb; pdb.set_trace()