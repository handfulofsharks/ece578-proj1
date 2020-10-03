import numpy as np
import random
import sys
import os
from copy import deepcopy
import scipy.stats as st



def transmission(args):
    is_ready = queue
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
    
def calculate_backoff(sim_time):
    
def detect_collision(sim_time):
    collision_detected = random.randint(0,1)
    return collision_detected
    
def sifs(sim_time):
    
def ack(sim_time):
    
def resolve_collision(sim_time):
    
def collision(sim_time):
    
def reset(sim_time):


class Args():
    def __init__(self):
        description = 'command line inputs for lhs design'
        parser = argparse.ArgumentParser(description=description)
        inputs = self.parseArgs(parser)
        
        self.dim = inputs.frame_rate
        self.duration = inputs.duration
        
        
    def parseArgs(self, parser):
        
        parser.add_argument('-f', '--frame_rate', dest='frame_rate', type=int,
                            action='store', default=200,
                            help='Frame rate for network.')
        
        parser.add_argument('--duration', 'd', dest='duration', type=int,
                            action='store', default=10,
                            help='Duration for the simulation.')
        
        return parser.parse_args()
    
if __name__=='__main__':
    args = Args()
    main(args)