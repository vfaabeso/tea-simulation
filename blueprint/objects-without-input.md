Last Updated: August 16, 2025

# Fundamental Classes

## SimulationKernel

The main simulation engine.

* Constructor
```python
SimulationKernel()
```

* Non-Constant Variables
- entity_dict <dict>
Dictionary of `Entity` that are added in the simulation. The keys are the `id`s
of the inputted entities.

Example:
```python
{
    "container0": <Container>,
    "container1": <Container>,
    "cup0": <Cup>
}
```

- environment <Environment>
- is_ready_to_run=False <bool>
Acts as a flag if the commit is successful. If **True**, setup commands such as
`add_obj` and `config_env` would raise the `SimulationAlreadyConfirmedError`
error and would halt the program.

- current_tick=0 <int>
The time tick of the simulation.

* Methods

- Setup

- `add_obj(entity: Entity)`
Adds an entity to the simulation. The program throws the 
`SimulationAlreadyConfirmedError`an error if `add_obj` command is invoked after
confirming the setup, by checking the `is_ready_to_run` flag.

- `add_objs(entity_list: List[Entity])`
Adds entities from a given list. Uses the `add_obj(...)` method repeatedly.

- `config_env(env: Environment)`
Sets up the environment of the simulation.

- `confirm_setup()`
[!] Minor tweaks: I don't think the `Status` object would then be necessary if 
we can handle exceptions and warnings. Also, the reason why we changed the 
`SetupAlreadyConfirmed` to an error is because it is a "silly" error to commit 
and might as well correct the user first to run the program again.

[!] Critique: There is no need to run validate here, and it would be better
if we call `validate` for `SimObject` instantiation and update.

Confirms the setup before running the simulation. The `is_ready_to_run` flag 
is set to **True**. Calls a `SetupAlreadyConfirmedError` if called when the
first invocation is successful.

- Simulation

These methods are only callable once `confirm` has been successfully called.
Otherwise, the program will throw a `SimulationNotReadyError`.

- `advance()`
Advances the simulation by one tick.

Mechanics:
For each `Entity`, we update the internal state by each physics equations,
simplified into first-order ordinary differential equations (ODEs). This
implies the need for separate `_advance-*` methods for each type of `Entity`.
A sample Python code would be the following.

```python
new_dict = {}

for id, entity in self.entity_dict.items():
    if isinstance(entity, Container):
        new_dict[id] = self._advance_container(entity)
    elif isinstance(entity, Cup):
        new_dict[id] = self._advance_cup(entity)
    else:
        # throw an error here
        pass

self.entity_dict = new_dict
```

For `_advance_container()` as an example.

[!] Critique: No need to return the container. Please review how object 
modification works in Python. I have modified it in the pseudocode.

```python
def _advance_container(self, container) -> Container:
    # for easier reference
    env = self.environment
    # calculate the differentials
    # there are overridable constants if we specify but we assume that the
    # constants to be used are from the environment
    # for example, cooling rate may differ per entity
    dT = env.cooling_rate * (container.temp_curr - env.ambient_temp)
    dV = env.evap_rate * (container.temp_curr - env.ambient_temp)
    dp = container.teastate.particle_release_rate * container.teastate.current_particle_count
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
    # return
    return container

```

- `cmd(action: str, args: dict)`
This method will be available if input handling will be implemented in the
near future. For now, will raise a Python-native `NotImplementedError`.

- `obj_catalog()`
Views the list of `id`s present in the `entity_dict`. Returns a <List<str>>.

- `view_obj(id: str, show_static=False: bool)`
Views the object status by giving the `id` as argument. Raises an error if
object does not exist (`NonExistentObjectError`). This error is raised for 
scenarios when the object is to be fetched and modified. If `show_static` is 
**True** then static variables such as initial variables will also be shown. 
Otherwise, dynamic variables related to the simulation will be shown. 
Returns a <dict>.

- `view_status(verbose=False: bool)`
Views the overall status of the simulation at the current tick. The `verbose`
argument, if **True** implies that the `show_static` of entities will be set to
**True**, and that the `Environment` will also be shown. Returns a <dict>.

Sample Output

```python
{
    "current_tick": 100,
    "entities": {
        "container0": {
            "type": "container",
            "temp_curr": 95.0,
            "vol_curr": 200.0,
            "tea_particle_amount": 45.0,
            "tea_content": {
                "current_particle_count": 20.0
            }
        }
    }
}
```

## Interpreter

Will be implemented once input handling is added. For now, there seems to be no
need to implement it.

# Objects

This section is necessary to understand appropriate commands that may be
invoked. To be more precise, this is about the arguments that they take
which are usually invoked when adding them in the simulation.

The id can be generated by an `IdGenerator` when added to the SimulationKernel
via `add_obj` if there is no value inputted.

*Both the syntax and semantics will be checked when calling the constructor.*

## SimObject

Superclass of all objects (excluding `SimulationKernel` and `Interpreter`).
This is not invoked directly.

* Constructor
```python
SimObject()
```

* Methods
- `validate()`
Checks the initial variables and the semantics of the initial variables.
Otherwise, if semantics are not followed, then the `SemanticError` error will 
be thrown. *This is called everytime instantiation or update occurs*.

## Entity

This is a superclass of `Container` and `Cup`. This may not be invoked
directly.

* Constructor
```python
Entity(
    id: str = ""
)
```

* Methods

- `correct_values()`

Corrects the values of variables, for example, if they surpass the expected
minimum and maximum values. For example, temperature should not be below
-273.15 celsius, and therefore, when this function is called, the values will
be clamped. *There should be notification if some values have to be clamped*

- `update_values(update_dict)`

Applies updates to the values by a given dictionary. An example call would be 
the following:

```python
container.update_values({
        "temp_curr": -dT,
        "volume_curr": -dV,
        "tea_content.current_particle_count": -dp,
        "tea_particle_amount": +dp
    })
```

This function requires validation of inputs. Alternatively we can create a 
`Delta` class, for example `DeltaContainer`. However, this would result in 
"subclass" bloating since we have to make separate classes for these.
If the inputs are incorrect, the  `InvalidArgumentError` will be raised.

- `view_status(show_static=False)`

Views the status of the entity by printing select variables. `show_static`
being false means that (mostly) dynamic variables related to the evolution of
the simulation will only be shown. Otherwise, most variables will be shown.
Returns as a dictionary.

## Container

* Constructor
```python
Container(
    id: str,
    temp_init=100.0: float,
    vol_init=1000.0: float,
    vol_max=2000.0: float,
    heating_rate=1.0: float,
    is_heater_on=False: bool,
    tea_particle_amount=0.0: float,
    tea_content=TeaState(): TeaState
)
```

`tea_content` has a default `TeaState` settings (see `TeaState`).

* Non-Constant Variables

```python
temp_curr: float
vol_curr: float
tea_particle_amount: float
tea_content: TeaState
```

* Semantics
Semantics error fall into `SemanticError` where specific errors will inherit
from. `ValueOutOfRangeError` may have subclasses `LowerBoundError` and 
`UpperBoundError`.

- id: no identical ids
If violated: `DuplicateEntityIdError`

- temp_init: -273.15 is the lower bound
If violated: `ValueOutOfRangeError`
Can have the subclass `LowerBoundError`.

- vol_init: no negative values and tea_content.volume+vol_init must not exceed
vol_max
If violated: `ValueOutOfRangeError`
Can have the subclasses `LowerBoundError` and `UpperBoundError`.

- vol_max: no negative values
If violated: `ValueOutOfRangeError`
Can have the subclass `LowerBoundError`.

- heating_rate: only positive values
If violated: `ValueOutOfRangeError`
Can have the subclass `LowerBoundError`.

- tea_particle_amount: no negative values
If violated: `ValueOutOfRangeError`
Can have the subclass `LowerBoundError`.

- temp_curr: -273.15 is the lower bound
If violated: `ValueOutOfRangeError`
Can have the subclass `LowerBoundError`.

- vol_curr: no negative values and tea_content.volume+vol_init must not exceed
vol_max
If violated: `ValueOutOfRangeError`
Can have the subclasses `LowerBoundError` and `UpperBoundError`.

## Cup

* Constructor
```python
Cup(
    id: str,
    temp_init=0.0: float,
    vol_init=0.0: float,
    vol_max=250.0: float,
    tea_particle_amount=0.0: float,
    tea_content=TeaState(): TeaState
)
```

`tea_content` has a default `TeaState` settings (see `TeaState`).

* Non-Constant Variables
```python
vol_curr: float
temp_curr: float
tea_particle_amount: float
tea_content: TeaState
```

* Semantics
Semantics error fall into `SemanticError` where specific errors will inherit
from. `ValueOutOfRangeError` may have subclasses `LowerBoundError` and 
`UpperBoundError`.

- id: no identical ids
If violated: `DuplicateEntityIdError`

- temp_init: -273.15 is the lower bound
If violated: `ValueOutOfRangeError`
Can have the subclass `LowerBoundError`.

- vol_init: no negative values and tea_content.volume+vol_init must not exceed
vol_max
If violated: `ValueOutOfRangeError`
Can have the subclasses `LowerBoundError` and `UpperBoundError`.

- vol_max: no negative values
If violated: `ValueOutOfRangeError`
Can have the subclass `LowerBoundError`.

- tea_particle_amount: no negative values
If violated: `ValueOutOfRangeError`
Can have the subclass `LowerBoundError`.

- vol_curr: no negative values and tea_content.volume+vol_init must not exceed
vol_max
If violated: `ValueOutOfRangeError`
Can have the subclasses `LowerBoundError` and `UpperBoundError`.

- temp_curr: -273.15 is the lower bound
If violated: `ValueOutOfRangeError`
Can have the subclass `LowerBoundError`.

## TeaState

This refers to the internal tea state of the container or cup.
We can simplify our simulation a bit in that *there should only be one tea
flavor per container or cup*.

* Constructor
```python
TeaState(
    start_particle_count=0.0: float,
    volume=0.0: float,
    particle_release_rate=1.0: float
)
```

* Internal Variables
```python
current_particle_count: float
```

* Semantics
- start_particle_count: no negative values
If violated: `ValueOutOfRangeError`
Can have the subclass `LowerBoundError`.

- volume: no negative values
If violated: `ValueOutOfRangeError`
Can have the subclass `LowerBoundError`.

- particle_release_rate: no negative values
If violated: `ValueOutOfRangeError`
Can have the subclass `LowerBoundError`.

- current_particle_count: no negative values
If violated: `ValueOutOfRangeError`
Can have the subclass `LowerBoundError`.


# Other Classes

## Environment

* Constructor 
```python
Environment(
    cooling_rate=1: float,
    ambient_temp=20: float,
    time_tick=1: float,
    evap_rate=1: float,
)
```

## IdHandler

[!] Revision: This only is diminished into a list since
we don't have to generate ids in favor of manual id inputting

`SimulationKernel` uses this ID handler to generate the id if the id is not
explicitly provided in constructing entities. It also holds the ids currently
in store.

* Constructor
```python
IdHandler()
```

* Non-constant Variables
- id_catalog <List<str>>: list of ids registered
- num_counter <dict>: a counter to keep track of the counters to be put in the
ids. Here is an example content.
```python
{
    "container": 1,
    "cup": 2
}
```

* Methods

- `generateId(entity: Entity) : str`
Generates an id for the entity. Uses `id_catalog` for checking existing ids and
num_counter for the numerical part of the id. By definition, it should generate
ids that do not exist yet. Returns an id string.

- `registerId(id: str)`
[!] Consideration: We can have reserve keywords, for example, we may not have
"env" as an id name because it can be used in `SimulationKernel.view_status()`

Places the id into the `id_catalog`. Program raises a `IdAlreadyExistsWarning`
if the id already exists and instead creates a new one similar to the original 
id. For example, if the id `Container` already exists and that `Container0` id
does not exist yet, based on the `num_counter`, then the proposed new id would 
be `Container0`.

- `idExists(id: str)`
Checks if the id already exists.

Mechanism:
Ensure that after adding the `Entity` to the `entity_dict` of `SimulationKernel`
assuming that the `id` is unique, we register that id to check for duplicates in
future addition of entities.

## Status

* Constructor
```python
Status(
    success: bool,
    msg: str
)
```

