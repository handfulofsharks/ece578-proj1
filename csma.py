import numpy as np
import argparse
import random
import sys
import os
from copy import deepcopy
import scipy.stats as st
from distrib import generateDistribution as gen_dist

def main(sim_params):
    frame_rates = [200,300,500,1000,2000]
    for frame_rate in frame_rates:
        X = gen_dist(frame_rate,
                     sim_params.max_sim_time_sec,
                     sim_params.slot_dur_us)
        import pdb; pdb.set_trace()

def transmission(args):
    is_ready = queue()
    if is_ready == 1:
        difs()
        calculate_backoff()
        transmission()
        collision_detected = detect_collision()
        while collision_detected == 1:
            resolve_collision()
            collision_detected = detect_collision()
        
    
def queue(sim_time):
    is_ready = random.randint(0,1)
    return is_ready
    
def difs(sim_time):
    is_ready = random.randint(0,1)
    return is_ready
    
def calculate_backoff(sim_time):
    is_ready = random.randint(0,1)
    return is_ready
    
def detect_collision(sim_time):
    collision_detected = random.randint(0,1)
    return collision_detected
    
def sifs(sim_time):
    is_ready = random.randint(0,1)
    return is_ready
    
def ack(sim_time):
    is_ready = random.randint(0,1)
    return is_ready
    
def resolve_collision(sim_time):
    is_ready = random.randint(0,1)
    return is_ready
    
def collision(sim_time):
    is_ready = random.randint(0,1)
    return is_ready
    
def reset(sim_time):
    is_ready = random.randint(0,1)
    return is_ready


class Sim_Params():
    def __init__(self):
        description = 'command line inputs for lhs design'
        parser = argparse.ArgumentParser(description=description)
        inputs = self.parseArgs(parser)
        
        self.frame_size_byte = inputs.frame_size_bytes
        self.frame_size_slots = inputs.frame_size_slots
        self.ACK = inputs.ACK
        self.RTS = inputs.ACK
        self.CTS = inputs.CTS
        self.slot_dur_us = inputs.slot_dur_us
        self.DIFS = inputs.DIFS_dur
        self.SIFS = inputs.SIFS_dur
        self.CW0 = inputs.CW0
        self.CW_max = inputs.CW_max
        self.max_sim_time_sec = inputs.max_sim_time_sec
        
        
    def parseArgs(self, parser):
        
        parser.add_argument('--frame_size_bytes', dest='frame_size_bytes', type=int,
                            action='store', default=1500,
                            help='Frame rate for network.')
        
        parser.add_argument('--frame_size_slots', dest='frame_size_slots', type=int,
                            action='store', default=50,
                            help='Frame rate for network.')
        
        parser.add_argument('--ACK', dest='ACK', type=int,
                            action='store', default=2,
                            help='Duration for the simulation.')
        
        parser.add_argument('--RTS', dest='RTS', type=int,
                            action='store', default=2,
                            help='Duration for the simulation.')
        
        parser.add_argument('--CTS', dest='CTS', type=int,
                            action='store', default=2,
                            help='Duration for the simulation.')
        
        parser.add_argument('--slot_dur_us', '-sd', dest='slot_dur_us', type=int,
                            action='store', default=10e-6,
                            help='Duration for the simulation.')
        
        parser.add_argument('--DIFS', dest='DIFS_dur', type=int,
                            action='store', default=2,
                            help='Duration for the simulation.')
        
        parser.add_argument('--SIFS', dest='SIFS_dur', type=int,
                            action='store', default=1,
                            help='Duration for the simulation.')
        
        parser.add_argument('--CW0', dest='CW0', type=int,
                            action='store', default=4,
                            help='Duration for the simulation.')
        
        parser.add_argument('--CW_max', dest='CW_max', type=int,
                            action='store', default=1024,
                            help='Duration for the simulation.')
        
        parser.add_argument('--max_sim_time', dest='max_sim_time_sec', type=int,
                            action='store', default=10,
                            help='Duration for the simulation.')
        
        return parser.parse_args()
    
if __name__=='__main__':
    sim_params = Sim_Params()
    main(sim_params)