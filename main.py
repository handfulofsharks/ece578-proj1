import argparse
import math

from channel import Channel
from node import Node, State
import pandas as pd

def wrapper(sim_params):
    # Frame rates are declared in project outline.
    frame_rates = [200,300,500,1000,2000]
    # Loops through each frame rate for analysis.
    columns = ['frame_rate', 'collisions', 'a_succ', 'c_succ']
    data = list()
    for frame_rate in frame_rates:
        data.append(main(sim_params,frame_rate))
    df = pd.DataFrame(data=data, columns=columns)
    import pdb; pdb.set_trace()


def main(sim_params, frame_rate):
    
    A = Node(sim_params, frame_rate, seed=3)
    C = Node(sim_params, frame_rate, seed=3)
    channel = Channel(sim_params)
    collisions = 0
    a_succ = 0
    c_succ = 0
    
    #number of slots for 10 seconds
    max_slots = math.ceil(sim_params.max_sim_time_sec/10e-6)
    
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
        if C.state == State.waiting_to_transmit:
            if channel.is_idle:
                C.difs_duration -= 1
            else:
                C.difs_duration = 2
            if C.difs_duration <= 0:
                C.backoff -= 1
                if C.backoff <= 0:
                    C.state = State.transmitting
                    
        if A.state == State.transmitting and C.state == State.transmitting:
            #collision
            A.cw = A.cw * 2
            A.backoff = None
            C.cw = C.cw * 2
            collisions += 1
            C.backoff = None
        elif A.state == State.transmitting and not C.state == State.transmitting:
            channel.is_idle = False
            A.backoff = None
            a_succ += 1
            A.cw = A.cw_0
            C.cw = C.cw_0
        elif not A.state == State.transmitting and C.state == State.transmitting:
            channel.is_idle = False
            C.backoff = None
            c_succ += 1
            A.cw = A.cw_0
            C.cw = C.cw_0
    
    return [frame_rate, collisions, a_succ, c_succ]


class Sim_Params():
    def __init__(self):
        description = 'command line inputs for lhs design'
        parser = argparse.ArgumentParser(description=description)
        # parses command line inputs.
        inputs = self.parseArgs(parser)
        # assigns inputs from parseArgs function to class members
        self.frame_size_byte = inputs.frame_size_bytes
        self.frame_size_slots = inputs.frame_size_slots
        self.ACK_dur = inputs.ACK_dur
        self.slot_dur_us = inputs.slot_dur_us
        self.DIFS_dur = inputs.DIFS_dur
        self.SIFS_dur = inputs.SIFS_dur
        self.CW_0 = inputs.CW_0
        self.CW_max = inputs.CW_max
        self.max_sim_time_sec = inputs.max_sim_time_sec
        
    def parseArgs(self, parser):
        
        parser.add_argument('--frame_size_bytes', dest='frame_size_bytes', type=int,
                            action='store', default=1500,
                            help='Frame size in bytes for network.')
        
        parser.add_argument('--frame_size_slots', dest='frame_size_slots', type=int,
                            action='store', default=50,
                            help='Frame size in slots for network.')
        
        parser.add_argument('--ACK', dest='ACK_dur', type=int,
                            action='store', default=2,
                            help='Duration in slots for ACK protocol.')
        
        parser.add_argument('--slot_dur_us', '-sd', dest='slot_dur_us', type=int,
                            action='store', default=10e-6,
                            help='Conversion factor for slot duration to sec.')
        
        parser.add_argument('--DIFS', dest='DIFS_dur', type=int,
                            action='store', default=2,
                            help='Duration in slots for DIFS protocol.')
        
        parser.add_argument('--SIFS', dest='SIFS_dur', type=int,
                            action='store', default=1,
                            help='Duration in slots for SIFS protocol.')
        
        parser.add_argument('--CW0', dest='CW_0', type=int,
                            action='store', default=4,
                            help='Initial transmission window dur in slots.')
        
        parser.add_argument('--CW_max', dest='CW_max', type=int,
                            action='store', default=1024,
                            help='Max transmission window dur in slots.')
        
        parser.add_argument('--max_sim_time', dest='max_sim_time_sec', type=int,
                            action='store', default=10,
                            help='Duration for the simulation.')
        
        return parser.parse_args()
    
if __name__=='__main__':
    sim_params = Sim_Params()
    wrapper(sim_params)