# insert necessary libraries

class TeaState(SimObject):
    def __init__(self, start_particle_count=0.0: float, volume=0.0: float,
        particle_release_rate=1.0: float) -> None:
        super.__init__()
        self._start_particle_count = start_particle_count
        self._volume = volume
        self._particle_release_rate = particle_release_rate
        # variables
        self._current_particle_count = start_particle_count
