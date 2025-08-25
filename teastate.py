from entity import Entity
import custom_exceptions as cex
from utils import number

class TeaState(Entity):
    def __init__(self, id: str, start_particle_count: float=0.0, volume: float=0.0,
                 particle_release_rate: float=1.0) -> None:
        super().__init__(id)
        self.start_particle_count = start_particle_count
        self.volume = volume
        self.particle_release_rate = particle_release_rate
        # variables
        self.current_particle_amount = start_particle_count
        self._init_validate()

    # for checking constants
    def _init_validate(self) -> None:
        if self.start_particle_count < 0:
            raise cex.LowerBoundError(
                f"Initial particle count ({self.start_particle_count}) \
                    cannot be negative."
            )
        if self.volume < 0:
            raise cex.LowerBoundError(
                f"Volume ({self.volume}) cannot be negative."
            )
        if self.particle_release_rate < 0:
            raise cex.LowerBoundError(
                f"Particle release rate ({self.particle_release_rate}) \
                    cannot be negative."
            )
    
    # for updating variables
    def _validate(self) -> None:
        if self.current_particle_amount < 0:
            raise cex.LowerBoundError(
                f"Current particle amount ({self.particle_release_rate}) \
                    cannot be negative."
            )
    
    def _update_value(self, dict_key:str, value:any) -> None:
        # only update updatable variables
        match dict_key:
            case "current_particle_amount":
                self.current_particle_amount += value
            case _:
                raise cex.InvalidArgumentError(
                    f"Variable {dict_key} might not exist or that it is a static\
                        variable."
                )
    
    def update_values(self, update_dict: dict) -> None:
        for key, value in update_dict.items():
            self._update_value(key, value)
        # check for every update
        self._validate()

    def to_json(self, show_static: bool=False) -> dict:
        # prepare variable status
        status = {
            "id": self.id,
            "current_particle_amount": self.current_particle_amount
        }
        if show_static:
            status = status | {
                "start_particle_count": self.start_particle_count,
                "volume": self.volume,
                "particle_release_rate": self.particle_release_rate,
            }
        return status