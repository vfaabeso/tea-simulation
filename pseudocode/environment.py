# import necessary libraries

class Environment(SimObject):
    def __init__(self, cooling_rate=1.0: float, ambient_temp=20: float,
        time_tick=1.0: float, evap_rate=1.0) -> None:
        self._cooling_rate = cooling_rate
        self._ambient_temp = ambient_temp
        self._time_tick = time_tick
        self._evap_rate = evap_rate
