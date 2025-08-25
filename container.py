from entity import Entity
from teastate import TeaState
import custom_exceptions as cex
from utils import MIN_TEMP, number

class Container(Entity):

    def __init__(self, id: str, temp_init: float=100.0, vol_init: float=1000.0,
                 vol_max: float=2000.0, heating_rate: float=1.0, is_heater_on: bool=False,
                 tea_particle_amount: float=0.0, tea_content: TeaState=TeaState(id="")) -> None:
        super().__init__(id)
        self.temp_init = temp_init
        self.vol_init = vol_init
        self.vol_max = vol_max
        self.heating_rate = heating_rate
        self.is_heater_on = is_heater_on
        # variables
        self.temp_curr = temp_init
        self.vol_curr = vol_init
        self.tea_particle_amount = tea_particle_amount
        self.tea_content = tea_content
        # set up the tea state id if blank
        if not self.tea_content.id:
            self.tea_content.id = id + "_tea_state"
        # finally, validate
        self._init_validate()

    # validation for initialization
    def _init_validate(self) -> None:
        # ordering here matters (e.g. vol max first before checking the upper
        # bounds of volume)
        # validate the tea state

        self.tea_content._init_validate()
        if self.temp_init < MIN_TEMP:
            raise cex.LowerBoundError(f"Initial temperature ({self.temp_init}) cannot be \
                                      below absolute zero.")
        if self.vol_init < 0:
            raise cex.LowerBoundError(f"Initial volume ({self.vol_init}) cannot \
                                      be below zero.")
        if self.vol_max < 0:
            raise cex.LowerBoundError(f"Maximum volume ({self.vol_max}) \
                                      cannot be below zero.")
        if self.vol_init+self.tea_content.volume > self.vol_max:
            raise cex.UpperBoundError(
                f"Initial volume ({self.vol_init}) plus tea volume \
                 cannot be ({self.tea_content.volume}) above maximum capacity.")
        if self.heating_rate < 0:
            raise cex.LowerBoundError(f"Heating rate ({self.heating_rate}) cannot \
                                      be below zero.")
        if self.tea_particle_amount < 0:
            raise cex.LowerBoundError(f"Tea particle amount ({self.tea_particle_amount}) \
                                      cannot be below zero.")

    def _validate(self) -> None:
        """Returns nothing but raises an exception if it encountered a 
        semantic discrepancy."""
        # validate the tea state
        self.tea_content._validate()
        if self.tea_particle_amount < 0:
            raise cex.LowerBoundError(f"Tea particle amount ({self.tea_particle_amount}) \
                                      cannot be below zero.")
        if self.temp_curr < MIN_TEMP:
            raise cex.LowerBoundError(f"Current temperature ({self.temp_curr}) cannot \
                                      be below absolute zero.")
        if self.vol_curr < 0:
            raise cex.LowerBoundError(f"Current volume ({self.vol_curr}) cannot be \
                                      below zero.")
        if self.vol_curr+self.tea_content.volume > self.vol_max:
            raise cex.UpperBoundError(f"Current volume ({self.vol_init}) plus tea volume \
                 cannot be ({self.tea_content.volume}) above maximum capacity.")
        
    # update a single value from dict
    # also has a checker accompanied

    def _update_value(self, dict_key:str, value:any) -> None:
        # only update updatable variables
        # update the tea first
        match dict_key:
            case "temp_curr":
                self.temp_curr += value
            case "vol_curr":
                self.vol_curr += value
            case "tea_particle_amount":
                self.tea_particle_amount += value
            case "tea_content":
                # defer to tea state
                self.tea_content.update_values(value)
            case _:
                raise cex.InvalidArgumentError(
                    f"Variable {dict_key} might not exist or that it is a static\
                        variable."
                )

    # warning: this directly updates the values
    # but this is fine for now since the values of each
    # entity are not codependent with each other
    def update_values(self, update_dict: dict) -> None:
        for key, value in update_dict.items():
            self._update_value(key, value)
        # check for every update
        self._validate()

    # this is actually more of a serialization function
    def to_json(self, show_static: bool=False) -> dict:
        # prepare variable status
        status = {
            "id": self.id,
            "temp_curr": self.temp_curr,
            "vol_curr": self.vol_curr,
            "tea_particle_amount": self.tea_particle_amount,
            "tea_content": self.tea_content.to_json(show_static)
        }
        if show_static:
            status = status | {
                "temp_init": self.temp_init,
                "vol_init": self.vol_init,
                "vol_max": self.vol_max,
                "heating_rate": self.heating_rate,
                "is_heater_on": self.is_heater_on,
            }
        return status