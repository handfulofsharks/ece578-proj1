import argparse
import math

import pandas as pd

from channel import Channel
from node import Node, State
from plot_wrapper import plot_wrapper

def wrapper(sim_params):
    # Frame rates are declared in project outline.
    frame_rates = [200,300,500,1000,2000]
    # frame_rates = list(range(200,2010))
    # frame_rates = frame_rates[0::10]
    # Loops through each frame rate for analysis.
    columns = ['scenario',
                'frame_rate',
                'collisions',
                'a_succ',
                'c_succ',
                'a_thruput',
                'c_thruput',
                'fairness_index']
    scenario1_csma = list()
    scenario1_vcs = list()
    scenario2_csma = list()
    scenario2_vcs = list()
    for frame_rate in frame_rates:
        scenario1_csma.append(['Scenario A with  CSMA'] + Scenario1_CSMA(sim_params,frame_rate))
        scenario1_vcs.append(['Scenario A with VCS'] + Scenario1_VCS(sim_params,frame_rate))
        scenario2_csma.append(['Scenario B with CSMA'] + Scenario2_CSMA(sim_params,frame_rate))
        scenario2_vcs.append(['Scenario B with VCS'] + Scenario2_VCS(sim_params,frame_rate))
    data = scenario1_csma + scenario1_vcs + scenario2_csma + scenario2_vcs
    df = pd.DataFrame(data=data, columns=columns)
    plot_wrapper(df)


def Scenario1_CSMA(sim_params, frame_rate):
    
    A = Node(sim_params, frame_rate, seed=3)
    C = Node(sim_params, frame_rate, seed=5)
    channel = Channel(sim_params)
    collisions = 0
    a_succ = 0
    c_succ = 0
    
    #number of slots for 10 seconds
    max_slots = math.ceil(sim_params.max_sim_time_sec/sim_params.slot_dur_us)
    
    for slot in range(0, max_slots):
        #checks if a packet is ready for transmit and adds it to queue
        A.check_packet_ready(slot, C)
        C.check_packet_ready(slot, A)
        if not channel.is_idle:
            channel.idle_count -= 1
            if channel.idle_count <= 0:
                channel.is_idle = True
                channel.idle_count = sim_params.frame_size_slots + sim_params.SIFS_dur + sim_params.ACK_dur
                if A.state == State.transmitting:
                    A.state = State.idle
                if C.state == State.transmitting:
                    C.state = State.idle
            continue
    
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
            collisions += 1
            A.cw = A.cw * 2
            A.backoff = None
            A.state = State.idle
            A.difs_duration = 2
            C.cw = C.cw * 2
            C.backoff = None
            C.state = State.idle
            C.difs_duration = 2
        elif A.state == State.transmitting and not C.state == State.transmitting:
            channel.is_idle = False
            A.backoff = None
            a_succ += 1
            A.cw = A.cw_0
            C.cw = C.cw_0
            A.queue.get()
            A.difs_duration = 2
            C.difs_duration = 2

        elif not A.state == State.transmitting and C.state == State.transmitting:
            channel.is_idle = False
            C.backoff = None
            c_succ += 1
            A.cw = A.cw_0
            C.cw = C.cw_0
            C.queue.get()
            A.difs_duration = 2
            C.difs_duration = 2
                   
    a_thruput = get_throughput_bits(a_succ,
                                    sim_params.frame_size_bytes,
                                    sim_params.max_sim_time_sec,
                                    scale=10e3)
    c_thruput = get_throughput_bits(c_succ,
                                    sim_params.frame_size_bytes,
                                    sim_params.max_sim_time_sec,
                                    scale=10e3)
    
    fairness_index = get_fairness_index(a_succ,c_succ,max_slots,sim_params)
    return [frame_rate, collisions, a_succ, c_succ, a_thruput, c_thruput, fairness_index]


def Scenario1_VCS(sim_params, frame_rate):
    A = Node(sim_params, frame_rate, seed=3)
    C = Node(sim_params, frame_rate, seed=5)
    channel = Channel(sim_params)
    collisions = 0
    a_succ = 0
    c_succ = 0

    #number of slots for 10 seconds
    max_slots = math.ceil(sim_params.max_sim_time_sec/sim_params.slot_dur_us)
    
    for slot in range(0, max_slots):
        #checks if a packet is ready for transmit and adds it to queue
        A.check_packet_ready(slot, C)
        C.check_packet_ready(slot, A)
        if not channel.is_idle:
            channel.idle_count -= 1
            if channel.idle_count <= 0:
                channel.is_idle = True
                channel.idle_count = sim_params.frame_size_slots + sim_params.SIFS_dur + sim_params.ACK_dur + 2 + 2 +  1 + 1
                if A.state == State.transmitting:
                    A.state = State.idle
                if C.state == State.transmitting:
                    C.state = State.idle
            continue
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
                        #send RTS + NAV
                        A.state = State.transmitting
        
        if C.state == State.waiting_to_transmit:
            if channel.is_idle:
                C.difs_duration -= 1
            else:
                C.difs_duration = 2
            if C.difs_duration <= 0:
                #decrement backoff slots
                if channel.is_idle:
                    C.backoff -= 1
                    if C.backoff <= 0:
                        #send RTS + NAV
                        C.state = State.transmitting
        
        if A.state == State.transmitting and C.state == State.transmitting:
            #collision
            collisions += 1
            A.cw = A.cw * 2
            A.backoff = None
            A.state = State.idle
            A.difs_duration = 2
            C.cw = C.cw * 2
            C.backoff = None
            C.state = State.idle
            C.difs_duration = 2
        elif A.state == State.transmitting and not C.state == State.transmitting:
            channel.is_idle = False
            A.backoff = None
            a_succ += 1
            A.cw = A.cw_0
            C.cw = C.cw_0
            A.queue.get()
            A.difs_duration = 2
            C.difs_duration = 2

        elif not A.state == State.transmitting and C.state == State.transmitting:
            channel.is_idle = False
            C.backoff = None
            c_succ += 1
            A.cw = A.cw_0
            C.cw = C.cw_0
            C.queue.get()
            A.difs_duration = 2
            C.difs_duration = 2
                   
    a_thruput = get_throughput_bits(a_succ,
                                    sim_params.frame_size_bytes,
                                    sim_params.max_sim_time_sec,
                                    scale=10e3)
    c_thruput = get_throughput_bits(c_succ,
                                    sim_params.frame_size_bytes,
                                    sim_params.max_sim_time_sec,
                                    scale=10e3)
    
    fairness_index = get_fairness_index(a_succ,c_succ,max_slots,sim_params)
    return [frame_rate, collisions, a_succ, c_succ, a_thruput, c_thruput, fairness_index]          


def Scenario2_CSMA(sim_params, frame_rate):
    A = Node(sim_params, frame_rate, seed=3)
    C = Node(sim_params, frame_rate, seed=5)
    collisions = 0
    a_succ = 0
    c_succ = 0

    #number of slots for 10 seconds
    max_slots = math.ceil(sim_params.max_sim_time_sec/sim_params.slot_dur_us)
    
    for slot in range(0, max_slots):
        A.check_packet_ready(slot, C)
        C.check_packet_ready(slot, A)

        if A.state == State.ready_to_transmit:
            if A.backoff is None:
                A.calc_backoff()
            A.state = State.waiting_to_transmit
        if C.state == State.ready_to_transmit:
            if C.backoff is None:
                C.calc_backoff()
            C.state = State.waiting_to_transmit
        
        if A.state == State.waiting_to_transmit:
            # DIFS is always decremented because A cannot see C so it always 
            # beleives channel is idle
            A.difs_duration -= 1
            if A.difs_duration <= 0:
                A.backoff -= 1
                if A.backoff <= 0:
                    A.state = State.transmitting
                    A.transmit_count = A.get_transmit_count(sim_params)

        if C.state == State.waiting_to_transmit:
            # DIFS is always decremented because A cannot see C so it always
            # beleives channel is idle
            C.difs_duration -= 1
            if C.difs_duration <= 0:
                C.backoff -= 1
                if C.backoff <= 0:
                    C.state = State.transmitting
                    C.transmit_count = C.get_transmit_count(sim_params)
                    
        if A.state == State.transmitting:
            A.transmit_count -= 1
        if C.state == State.transmitting:
            C.transmit_count -= 1

        if A.state == State.transmitting and C.state == State.transmitting:
            if A.valid or C.valid:
                A.valid = False 
                C.valid = False
                collisions += 1

        if A.state == State.transmitting:
            if A.transmit_count <= 0:
                if A.valid:
                   a_succ += 1
                   A.queue.get()
                   A.reset_node()
                else:
                    A.collision()
                   
        if C.state == State.transmitting:
            if C.transmit_count <= 0:
                if C.valid:
                    c_succ += 1
                    C.queue.get()
                    C.reset_node()
                else:
                    C.collision()
                   
    a_thruput = get_throughput_bits(a_succ,
                                    sim_params.frame_size_bytes,
                                    sim_params.max_sim_time_sec,
                                    scale=10e3)
    c_thruput = get_throughput_bits(c_succ,
                                    sim_params.frame_size_bytes,
                                    sim_params.max_sim_time_sec,
                                    scale=10e3)
    
    fairness_index = get_fairness_index(a_succ,c_succ,max_slots,sim_params)
    return [frame_rate, collisions, a_succ, c_succ, a_thruput, c_thruput, fairness_index]


def Scenario2_VCS(sim_params, frame_rate):
    
    A = Node(sim_params, frame_rate, seed=3)
    C = Node(sim_params, frame_rate, seed=5)
    collisions = 0
    a_succ = 0
    c_succ = 0
    #number of slots for 10 seconds
    max_slots = math.ceil(sim_params.max_sim_time_sec/sim_params.slot_dur_us)
    
    for slot in range(0, max_slots):
        A.check_packet_ready(slot, C)
        C.check_packet_ready(slot, A)
        
        if A.state == State.ready_to_transmit:
            if A.backoff is None:
                A.calc_backoff()
            A.state = State.waiting_to_transmit
        if C.state == State.ready_to_transmit:
            if C.backoff is None:
                C.calc_backoff()
            C.state = State.waiting_to_transmit
        
        if A.state == State.waiting_to_transmit:
            # DIFS is always decremented because A cannot see C so it always 
            # beleives channel is idle
            A.difs_duration -= 1
            if A.difs_duration <= 0:
                A.backoff -= 1
                if A.backoff <= 0:
                    A.state = State.sending_RTS
                    A.RTS_end = A.get_NAV(sim_params) + slot
                    A.CTS_count = 6

        if C.state == State.waiting_to_transmit:
            # DIFS is always decremented because A cannot see C so it always
            # beleives channel is idle
            C.difs_duration -= 1
            if C.difs_duration <= 0:
                C.backoff -= 1
                if C.backoff <= 0:
                    C.state = State.sending_RTS
                    C.RTS_end = C.get_NAV(sim_params) + slot
                    C.CTS_count = 6
                    
        if A.state == State.sending_RTS and C.state == State.sending_RTS:
            #collision
            if A.valid or C.valid:
                A.valid = False 
                C.valid = False
                collisions += 1
                A.collision()
                C.collision()

        if A.state == State.sending_RTS and C.state != State.sending_RTS:
            A.CTS_count -= 1
            if A.CTS_count <= 0:
                if A.valid:
                    #set C nav vector
                    C.state = State.waiting_NAV
                    C.NAV = A.RTS_end -1
                    A.state = State.transmitting
                    A.transmit_count = A.get_transmit_count(sim_params)

        if A.state != State.sending_RTS and C.state == State.sending_RTS:
            C.CTS_count -= 1
            if C.CTS_count <= 0:
                if C.valid:
                    #set C nav vector
                    A.state = State.waiting_NAV
                    A.NAV = C.RTS_end-1
                    C.state = State.transmitting
                    C.transmit_count = C.get_transmit_count(sim_params)
                    
        if A.state == State.waiting_NAV:
            if A.NAV == slot:
                A.state = State.idle

        if C.state == State.waiting_NAV:
            if C.NAV == slot:
                C.state = State.idle
        
        if A.state == State.transmitting:
            A.transmit_count -= 1
            if A.transmit_count <= 0:
                a_succ += 1
                A.queue.get()
                A.reset_node()

        if C.state == State.transmitting:
            C.transmit_count -= 1
            if C.transmit_count <= 0:
                c_succ += 1
                C.queue.get()
                C.reset_node()
                   
    a_thruput = get_throughput_bits(a_succ,
                                    sim_params.frame_size_bytes,
                                    sim_params.max_sim_time_sec,
                                    scale=10e3)
    c_thruput = get_throughput_bits(c_succ,
                                    sim_params.frame_size_bytes,
                                    sim_params.max_sim_time_sec,
                                    scale=10e3)
    
    fairness_index = get_fairness_index(a_succ,c_succ,max_slots,sim_params)
    return [frame_rate, collisions, a_succ, c_succ, a_thruput, c_thruput, fairness_index]

            
def get_throughput_bits(successes, byte_frame_size, sim_time, scale):
    return 8*(successes * byte_frame_size/sim_time)/scale


def get_fairness_index(a_succ,c_succ,max_slots,sim_params):
    a_perc = (a_succ*sim_params.frame_size_slots)/max_slots
    c_perc = (c_succ*sim_params.frame_size_slots)/max_slots
    return a_perc/c_perc
    
    
class Sim_Params():
    def __init__(self):
        description = 'command line inputs for lhs design'
        parser = argparse.ArgumentParser(description=description)
        # parses command line inputs.
        inputs = self.parseArgs(parser)
        # assigns inputs from parseArgs function to class members
        self.frame_size_bytes = inputs.frame_size_bytes
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