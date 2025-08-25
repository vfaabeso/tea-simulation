# insert necessary imports

class Cup(Entity):
    def __init__(self, id="": str, temp_init=0.0: float, vol_init=0.0: float,
        vol_max=250.0: float, tea_particle_amount=0.0: float, 
        tea_content=TeaState(): TeaState) -> None:
        super.__init__(id)
        self._temp_init = temp_init
        self._vol_init = vol_init
        self._vol_max = vol_max
        self._tea_particle_amount = tea_particle_amount
        self._tea_content = tea_content
        # variables
        self._vol_curr = vol_init
        self._temp_curr = temp_init
        
