from node import Node, State
from channel import Channel
import math

a = Node(seed=3)
c = Node(seed=3)
channel = Channel()


#number of slots for 10 seconds
max_slots = math.ceil(10/10e-6)

for slot in range(0, max_slots):
    #checks if a packet is ready for transmit and adds it to queue
    a.check_packet_ready(slot)
    c.check_packet_ready(slot)

    if not channel.is_idle:
        channel.idle_count -= 1
        if channel.idle_count <= 0:
            channel.is_idle = True
            channel.idle_count = 50

    if a.state == State.ready_to_transmit:
        a.calc_backoff()
        a.state = State.waiting_to_transmit

    if c.state == State.ready_to_transmit:
        c.calc_backoff()
        c.state = State.waiting_to_transmit

    if a.state == State.waiting_to_transmit:      
        #wait until channel is idle for DIFS slots
        if channel.is_idle:
            a.difs_duration -= 1
        else:
            a.difs_duration = 2
        if a.difs_duration <= 0:
            #decrement backoff slots
            if channel.is_idle:
                a.backoff -= 1
                if a.backoff <= 0:
                    #transmit
                    a.state == State.transmitting
    if c.state == State.waiting_to_transmit:
        if channel.is_idle:
            c.difs_duration -= 1
        else:
            c.difs_duration = 2
        if c.difs_duration <= 0:
            c.backoff -= 1
            if c.backoff <= 0:
                c.state == State.transmitting
    
    if a.state == State.transmitting and c.state == State.transmitting:
        #collision
        print("collision")
    if a.state == State.transmitting or c.state == State.transmitting:
        channel.is_idle = False