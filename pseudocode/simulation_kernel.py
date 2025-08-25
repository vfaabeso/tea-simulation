# TODO: insert necessary imports
from environment import Environment

class SimulationKernel():
    def __init__(self) -> None:
        self._entity_dict: dict[str, Entity] = {}
        # TODO: check if the argument for Environment is correct
        self._environment: Environment = Environment()
        # TODO: add this ID handler to the documentation
        self._id_handler: IdHandler = IdHandler()
        self._is_ready_to_run: bool = False
        self._current_tick: int = 0

    def add_obj(self, entity: Entity) -> None:
        if not self._is_ready_to_run:
            raise SimulationNotReadyError(
                "Method cannot be invoked without \
                SimulationKernel.confirm_setup() having successfully called \
                beforehand."
            )
        else:
            # does the entity already have an id?
            # it defaults to a blank string if not invoked
            id = entity.id
            if id == "":
                # by definition generateId generates non-existent ids
                id = self._id_handler.generateId(entity)
                # add the obj first before registration 
                self._entity_dict[id] = entity
            # by definition, the registerId function will handle even duplicate
            # cases
            self._id_handler.registerId(id)

    def add_objs(self, entity_list: List[Entity]) -> None:
        for entity in entity_list:
            self.add_obj(entity)

    def config_env(self, env: Environment) -> None:
        self._environment = env

    def confirm_setup() -> None:
        if self._is_ready_to_run:
            raise SetupAlreadyConfirmedError(
                "Method invoked again when the simulation setup is already \
                confirmed."
            )
        self._is_ready_to_run = True

    def advance() -> None:
        if not self._is_ready_to_run:
            raise SimulationNotReadyError(
                "Method cannot be invoked due to simulation not fully set up \
                properly."
            )
        # I am not sure if this will cause an error 
        # because we are modifying the dictionary that we are looping
        # if that happens, we might do a double buffer approach
        for id, entity in self.entity_dict.items():
            if isinstance(entity, Container):
                self._advance_container(self.entity_dict[id])
            elif isinstance(entity, Cup):
                self._advance_cup(self.entity_dict[id])
            else:
                raise EntityTypeNotSupportedError(
                    "Entity type does not exist."
                )

    def _advance_container(self, container: Container) -> None:
        # for easier reference
        env = self.environment
        # calculate the differentials
        # there are overridable constants if we specify but we assume that the
        # constants to be used are from the environment
        # for example, cooling rate may differ per entity
        dT = env.cooling_rate * (container.temp_curr - env.ambient_temp)
        dV = env.evap_rate * (container.temp_curr - env.ambient_temp)
        dp = container.teastate.particle_release_rate \
            * container.teastate.current_particle_count
        # apply time tick
        dT *= env.time_tick
        dV *= env.time_tick
        dp *= env.time_tick
        
        # update the variables
        container.update_values({
            "temp_curr": -dT,
            "volume_curr": -dV,
            "tea_content.current_particle_count": -dp,
            "tea_particle_amount": +dp
        })
        
        # clamp the contents of the container
        container.correct_values()

    def _advance_cup(self, cup: Cup) -> None:
        # for easier reference
        env = self.environment
        # calculate the differentials
        # there are overridable constants if we specify but we assume that the
        # constants to be used are from the environment
        # for example, cooling rate may differ per entity
        dT = env.cooling_rate * (cup.temp_curr - env.ambient_temp)
        dV = env.evap_rate * (cup.temp_curr - env.ambient_temp)
        dp = cup.teastate.particle_release_rate 
            \* cup.teastate.current_particle_count
        # apply time tick
        dT *= env.time_tick
        dV *= env.time_tick
        dp *= env.time_tick
        
        # update the variables
        cup.update_values({
            "temp_curr": -dT,
            "volume_curr": -dV,
            "tea_content.current_particle_count": -dp,
            "tea_particle_amount": +dp
        })
        
        # clamp the contents of the container
        cup.correct_values()

    def cmd(action: str, args: dict) -> None:
        raise NotImplementedError

    def obj_catalog() -> List[str]:
        return self.entity_dict.keys()

    def view_obj(id: str, show_static=False: bool) -> dict:
        if not self._id_handler.idExists(id):
            raise NonExistentObjectError(
                "Object with such id does not exist."
            )
        entity = self._entity_dict[id]
        return entity.view_status(show_static)

    def view_status(verbose=False: bool) -> dict:
        status_dict = {}
        for id, entity in self._entity_dict.items():
            status_dict[id] = entity.view_status(verbose)
        if verbose:
            status_dict["env"] = self._environment
        return status_dict

    

