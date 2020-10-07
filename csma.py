import argparse

import numpy as np
import pandas as pd

from distrib import generateDistribution as gen_dist

def main(sim_params):
    # Frame rates are declared in project outline.
    frame_rates = [200,300,500,1000,2000]
    # Loops through each frame rate for analysis.
    for frame_rate in frame_rates:
        # Generates a uniform set of slot times for data transmissions in which
        # the will be ready, not neccessarily the time they will actually be
        # be transmitted.
        X_a = gen_dist(frame_rate,
                     sim_params.max_sim_time_sec,
                     sim_params.slot_dur_us,
                     seed=3)
        # Generates a uniform set of slot times for data transmissions in which
        # the will be ready, not neccessarily the time they will actually be
        # be transmitted.
        X_c = gen_dist(frame_rate,
                     sim_params.max_sim_time_sec,
                     sim_params.slot_dur_us,
                     seed=5)
        # creates queue using CSMA transmission protocol from the uniform slots
        # generated above.
        df_a = create_queue_A(sim_params, X_a)
        df_c = create_queue_C(sim_params, X_c)
        merged_queue = merge_queues(df_a,df_c)
        import pdb; pdb.set_trace()
        

def create_queue_A(sim_params, X_a):
    np.random.seed(1)
    # create columns for pandas data frame.
    # NOTE aside from Init_Slot, all values starting from pos 3 are the ending
    # slot number.
    columns = ['sender','receiver','init_slot','difs','backoff','frame_transmission','sifs','ack']
    # initialize data_set which will be appeneded to in following for loop
    # for pandas data frame.
    data_set = list()
    # sender and receiver values for later post processing use.
    sender = 'a'
    receiver = 'b'
    for transmission in X_a:
        # identifies the first slot in which the transmission will be ready
        init_slot = transmission
        # adds the DIFS duration to the init_slot var to indicate that DIFS 
        # protocol was completed.
        end_DIFS = init_slot + sim_params.DIFS_dur
        # Calculates the backoff duration by taking a random int between
        # 0 and CW0 -1 and then adds the backoff duration to the end_DIFS var
        # to indicate that backoff protocol was completed.
        end_backoff = end_DIFS + np.random.randint(0,sim_params.CW0-1)
        # adds the frame transmission duration to the end_backoff_var to 
        # indicate that frame was transmitted.
        end_frame_trasnsmission = end_backoff + sim_params.frame_size_slots
        # adds the SIFS duration to the end_frame_transmission to indicate 
        # that SIFS protocol was completed.
        end_SIFS = end_frame_trasnsmission + sim_params.SIFS_dur
        # adds the ACK duration to the end_SIFS var to indicate that ACK 
        # protocol was completed.
        end_ACK = end_SIFS + sim_params.ACK_dur
        # puts all the variables into a list for pandas
        trans_slots = [sender, receiver, init_slot, end_DIFS, end_backoff, end_frame_trasnsmission, end_SIFS, end_ACK]
        # determins if the current iteration is the first iteration of the 
        # transmissions.
        if len(data_set) > 0:
            # gets the end_ACK slot number from the previous iteration
            prev_end_slot = data_set[-1][-1]
            # if the current init_slot value is smaller than the previous 
            # iterations ACK slot number
            if init_slot < prev_end_slot:
                # get the difference between the two values and add one slot
                # to get the slot after completion of the previous ACK.
                slot_dif = prev_end_slot - init_slot + 1
                # pulls the sender and receiver values out as we can't add int
                # to strs
                info = trans_slots[:2]
                # add the wait time to the current iteration's transmission
                trans_slots = list(trans_slots[-6:] + slot_dif)
                # recombines s&r values to slot values
                trans_slots = info + trans_slots
        # append slot list to master data_set for pandas
        data_set.append(trans_slots)
    # create pandas data frame for easy data visualization and analysis
    df = pd.DataFrame(data=data_set, columns=columns)
    return df
        

def create_queue_C(sim_params, X_c):
    np.random.seed(1)
    # create columns for pandas data frame.
    # NOTE aside from Init_Slot, all values starting from pos 3 are the ending
    # slot number.
    columns = ['sender','receiver','init_slot','difs','backoff','frame_transmission','sifs','ack']
    # initialize data_set which will be appeneded to in following for loop
    # for pandas data frame.
    data_set = list()
    # sender and receiver values for later post processing use.
    data_set = list()
    sender = 'c'
    receiver = 'd'
    for transmission in X_c:
        # identifies the first slot in which the transmission will be ready
        init_slot = transmission
        # adds the DIFS duration to the init_slot var to indicate that DIFS 
        # protocol was completed.
        end_DIFS = init_slot + sim_params.DIFS_dur
        # Calculates the backoff duration by taking a random int between
        # 0 and CW0 -1 and then adds the backoff duration to the end_DIFS var
        # to indicate that backoff protocol was completed.
        end_backoff = end_DIFS + np.random.randint(0,sim_params.CW0-1)
        # adds the frame transmission duration to the end_backoff_var to 
        # indicate that frame was transmitted.
        end_frame_trasnsmission = end_backoff + sim_params.frame_size_slots
        # adds the SIFS duration to the end_frame_transmission to indicate 
        # that SIFS protocol was completed.
        end_SIFS = end_frame_trasnsmission + sim_params.SIFS_dur
        # adds the ACK duration to the end_SIFS var to indicate that ACK 
        # protocol was completed.
        end_ACK = end_SIFS + sim_params.ACK_dur
        # puts all the variables into a list for pandas
        trans_slots = [sender, receiver, init_slot, end_DIFS, end_backoff, end_frame_trasnsmission, end_SIFS, end_ACK]
        # determins if the current iteration is the first iteration of the 
        # transmissions.
        if len(data_set) > 0:
            # gets the end_ACK slot number from the previous iteration
            prev_end_slot = data_set[-1][-1]
            # if the current init_slot value is smaller than the previous 
            # iterations ACK slot number
            if init_slot < prev_end_slot:
                # get the difference between the two values and add one slot
                # to get the slot after completion of the previous ACK.
                slot_dif = prev_end_slot - init_slot + 1
                # pulls the sender and receiver values out as we can't add int
                # to strs
                info = trans_slots[:2]
                # add the wait time to the current iteration's transmission
                trans_slots = list(trans_slots[-6:] + slot_dif)
                # recombines s&r values to slot values
                trans_slots = info + trans_slots
        # append slot list to master data_set for pandas
        data_set.append(trans_slots)
    # create pandas data frame for easy data visualization and analysis
    df = pd.DataFrame(data=data_set, columns=columns)
    return df

def merge_queues(queue_a, queue_b):
    # initialize list for merged_queue data frame that this function resturns
    master_queue = list()
    # initializes column values
    columns = ['sender','receiver','init_slot','difs','backoff','frame_transmission','sifs','ack']
    # combines queues from a and c together, ignore indexes
    merged_queue = queue_a.append(queue_b, ignore_index=True)
    # sorts df by init_slot
    merged_queue = merged_queue.sort_values(by=['init_slot'])
    # resets the indexes to be logical in order for my sanity and OCD
    merged_queue = merged_queue.reset_index(drop=True)
    # initializes a variable for comparison to determine collisions
    previous_row = None
    # loops through transmission queue
    for index, row in merged_queue.iterrows():
        # turns row to list
        current_row = row.tolist()
        # if not the first row
        if previous_row is not None:
            # if the current init_slot value is smaller than the previous 
            # iterations ACK slot number
            if current_row[2] < previous_row[-1]:
                # get the difference between the two values and add one slot
                # to get the slot after completion of the previous ACK.
                diff = previous_row[-1] - current_row[2] + 1
                # pulls the sender and receiver values out as we can't add int
                # to strs
                info = current_row[:2]
                # add the wait time to the current iteration's transmission
                trans_slots = [x + diff for x in current_row[-6:]]
                # recombines s&r values to slot values
                current_row = info + trans_slots
        # append transmission to master_queue list for pandas
        master_queue.append(current_row)
        # assigns the current row to the previous row var for the next 
        # iteration
        previous_row = current_row
    # create pandas data frame for easy data visualization and analysis
    df = pd.DataFrame(data=master_queue, columns=columns)
    return df
        
        
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
        self.RTS_dur = inputs.ACK_dur
        self.CTS_dur = inputs.CTS_dur
        self.slot_dur_us = inputs.slot_dur_us
        self.DIFS_dur = inputs.DIFS_dur
        self.SIFS_dur = inputs.SIFS_dur
        self.CW0 = inputs.CW0
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
        
        parser.add_argument('--RTS', dest='RTS_dur', type=int,
                            action='store', default=2,
                            help='Duration in slots for RTS protocol.')
        
        parser.add_argument('--CTS', dest='CTS_dur', type=int,
                            action='store', default=2,
                            help='Duration in slots for CTS protocol.')
        
        parser.add_argument('--slot_dur_us', '-sd', dest='slot_dur_us', type=int,
                            action='store', default=10e-6,
                            help='Conversion factor for slot duration to sec.')
        
        parser.add_argument('--DIFS', dest='DIFS_dur', type=int,
                            action='store', default=2,
                            help='Duration in slots for DIFS protocol.')
        
        parser.add_argument('--SIFS', dest='SIFS_dur', type=int,
                            action='store', default=1,
                            help='Duration in slots for SIFS protocol.')
        
        parser.add_argument('--CW0', dest='CW0', type=int,
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
    main(sim_params)