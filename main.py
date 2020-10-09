from node import Node
from channel import Channel
import math

a = Node(seed=3)
c = Node(seed=5)
channel = Channel()

#number of slots for 10 seconds
max_slots = math.ceil(10/10e-6)

for slot in range(0, max_slots):
    #checks if a packet is ready for transmit and adds it to queue
    a.check_packet_ready(slot)
    c.check_packet_ready(slot)

    if a.is_ready(slot):
        a.calc_backoff()
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
                    channel.is_idle = False
    if c.is_ready(slot):
        c.calc_backoff()
        if channel.is_idle:
            c.difs_duration -= 1
        else:
             c.difs_duration = 2
        if c.difs_duration <= 0:
            c.backoff -= 1
            if c.backoff <= 0:
                channel.is_idle = False


            


        