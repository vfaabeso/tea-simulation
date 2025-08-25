# import necessary libraries

# for now the constants are stored here 
MIN_TEMP: float = -273.15

class Container(Entity):
    def __init__(self, id="": str, temp_init=100.0: float,
        vol_init=1000.0: float, vol_max=2000.0: float, heating_rate=1.0: float,
        is_heater_on=False: bool, tea_particle_amount=0.0: float,
        tea_content=TeaState(): TeaState) -> None:
        super.__init__(id)
        self._temp_init = temp_init
        self._vol_init = vol_init
        self._vol_max = vol_max
        self._heating_rate = heating_rate
        self._is_heater_on = is_heater_on
        self._tea_particle_amount = tea_particle_amount
        self._tea_content = tea_content
        # variables
        self._temp_curr = temp_init
        self._vol_curr = vol_init

    # place them in a custom file later
    number = int | float

    # TODO: It would be more efficient if we put our correction here 
    # for example, if the condition is set to true, then we 
    # warn the user that the value has been clamped
    # Another critique: what if there is no lower or upper bound?
    def _clamp(self, n: number, lower: number, upper: number) -> number:
        return max(lower, min(n, upper))

    # TODO: The comments in the errors can be put in the class themselves
    # like a default message.
    # Alternatively, there should be a more efficient way of doing this
    # since we notice that there are common errors appearing
    # but we might suffer from the difficulty of updating the code if we do it
    # Also this if-else solution is memory efficient
    # We can repurpose these messages in the simulation by printing them 
    # before updating (clamping).
    # Another critique I have is that there might have been a validation 
    # separated for initializing the variables and during updates via clamping
    def validate(self) -> None:
        """Returns nothing but raises an exception if it encountered a 
        semantic discrepancy."""
        if self._temp_init < MIN_TEMP:
            raise LowerBoundError("Initial temperature below absolute zero.")
        if self._vol_init < 0:
            raise LowerBoundError("Initial volume below zero.")
        if self._vol_init+self._tea_content._volume > self._vol_max:
            raise UpperBoundError(
                "Initial volume above maximum capacity. \
                Consider also the volume of the tea.")
        if self._vol_max < 0:
            raise LowerBoundError("Maximum volume below zero.")
        if self._heating_rate < 0:
            raise LowerBoundError("Heating rate below zero.")
        if self._tea_particle_amount < 0:
            raise LowerBoundError("Tea particle amount below zero.")
        if self._temp_curr < MIN_TEMP:
            raise LowerBoundError("Current temperature below absolute zero.")
        if self._vol_curr < 0:
            raise LowerBoundError("Current volume below zero.")
        if self._vol_curr+self._tea_content._volume > self._vol_max:
            raise UpperBoundError("Volume above maximum capacity.")

    # TODO: Although it would be more efficient to clamp specific variables
    # we can use this for the update_values, or forgo this function altogether
    def correct_values(self) -> None:
        # clamp it all
        pass

    def update_values(self, update_dict: dict) -> None:
        pass

    def view_status(self, show_static=False: bool) -> dict:
        pass


    
