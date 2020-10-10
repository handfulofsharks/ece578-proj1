class Channel:
    def __init__(self, sim_params):
        self.is_idle = True
        self.idle_count = sim_params.frame_size_slots
