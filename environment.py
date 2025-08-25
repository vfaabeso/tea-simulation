class Environment():
    def __init__(self, cooling_rate: float=1.0, ambient_temp: float=20.0,
                 time_tick: float=1.0, evap_rate: float=1.0) -> None:
        self.cooling_rate = cooling_rate
        self.ambient_temp = ambient_temp
        self.time_tick = time_tick
        self.evap_rate = evap_rate
