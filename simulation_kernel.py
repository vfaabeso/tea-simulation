from environment import Environment
from entity import Entity
import custom_exceptions as cex
from container import Container
from cup import Cup
import copy

class SimulationKernel():
    def __init__(self) -> None:
        self._entity_dict: dict[str, Entity] = {}
        self._environment: Environment = Environment()
        # we replaced id handling with a simple list
        # but I believe it's a fundamental principle that we shouldn't
        # assign ids automatically
        self._id_list: list[str] = []
        self._is_ready_to_run: bool = False
        self._current_tick: int = 0

    def add_obj(self, entity: Entity) -> None:
        if self._is_ready_to_run:
            raise cex.SimulationNotReadyError(
                "Method cannot be invoked without \
                SimulationKernel.confirm_setup() having successfully called \
                beforehand."
            )
        else:
            # first check if the id is present in the list
            if entity.id in self._id_list:
                raise cex.IdAlreadyExistsError(
                    f"ID {entity.id} already exists in one of the entities."
                )
            self._id_list.append(entity.id)
            # and therefore add the entity
            self._entity_dict[entity.id] = entity

    def add_objs(self, entity_list: list[Entity]) -> None:
        for entity in entity_list:
            self.add_obj(entity)

    def config_env(self, env: Environment) -> None:
        self._environment = env

    def confirm_setup(self) -> None:
        if self._is_ready_to_run:
            raise cex.SetupAlreadyConfirmedError(
                "Method invoked again when the simulation setup is already \
                confirmed."
            )
        self._is_ready_to_run = True

    def advance(self) -> None:
        if not self._is_ready_to_run:
            raise cex.SimulationNotReadyError(
                "Method cannot be invoked due to simulation not fully set up \
                properly."
            )
        # I am not sure if this will cause an error 
        # because we are modifying the dictionary that we are looping
        # if that happens, we might do a double buffer approach
        for id, entity in self._entity_dict.items():
            if isinstance(entity, Entity):
                if isinstance(entity, Container):
                    self._advance_container(self._entity_dict[id])
                elif isinstance(entity, Cup):
                    self._advance_cup(self._entity_dict[id])
                else:
                    raise cex.EntityTypeNotSupportedError(
                        "Update for this entity type is not supported."
                    )
            else:
                raise cex.InvalidArgumentError(
                    f"Object {str(entity)} not an entity for the simulation."
                )

    def _advance_container(self, container: Container) -> None:
        # for easier reference
        env = self._environment
        # calculate the differentials
        # there are overridable constants if we specify but we assume that the
        # constants to be used are from the environment
        # for example, cooling rate may differ per entity
        dT = env.cooling_rate * (container.temp_curr - env.ambient_temp)
        dV = env.evap_rate * (container.temp_curr - env.ambient_temp)
        dp = container.tea_content.particle_release_rate \
            * container.tea_content.current_particle_amount
        # apply time tick
        dT *= env.time_tick
        dV *= env.time_tick
        dp *= env.time_tick
        
        # update the variables
        container.update_values({
            "temp_curr": -dT,
            "vol_curr": -dV,
            "tea_content": {
                "current_particle_amount": -dp
            },
            "tea_particle_amount": dp
        })
        
        # clamp the contents of the container
        # container.correct_values()

    def _advance_cup(self, cup: Cup) -> None:
        # for easier reference
        env = self._environment
        # calculate the differentials
        # there are overridable constants if we specify but we assume that the
        # constants to be used are from the environment
        # for example, cooling rate may differ per entity
        dT = env.cooling_rate * (cup.temp_curr - env.ambient_temp)
        dV = env.evap_rate * (cup.temp_curr - env.ambient_temp)
        dp = cup.tea_content.particle_release_rate \
            * cup.tea_content.current_particle_amount
        # apply time tick
        dT *= env.time_tick
        dV *= env.time_tick
        dp *= env.time_tick
        
        # update the variables
        cup.update_values({
            "temp_curr": -dT,
            "vol_curr": -dV,
            "tea_content": {
                "current_particle_amount": -dp
            },
            "tea_particle_amount": dp
        })
        
        # clamp the contents of the container
        # cup.correct_values()

    def cmd(action: str, args: dict) -> None:
        raise NotImplementedError

    def obj_catalog(self) -> list[str]:
        return self.entity_dict.keys()

    def view_obj(self, id: str, show_static: bool=False) -> dict:
        if id not in self._id_list:
            raise cex.NonExistentObjectError(
                "Object with such id does not exist."
            )
        entity = self._entity_dict[id]
        return entity.view_status(show_static)

    def view_status(self, verbose: bool=False) -> dict:
        status_dict = {}
        for id, entity in self._entity_dict.items():
            status_dict[id] = entity.to_json(verbose)
        if verbose:
            status_dict["env"] = self._environment
        return status_dict

    

