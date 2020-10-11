class Channel:
    def __init__(self, sim_params):
        self.is_idle = True
        self.idle_count = sim_params.frame_size_slots + sim_params.SIFS_dur + sim_params.ACK_dur + 2 + 2 +  1 + 1 #RTS + CTS + 2x SIFS
