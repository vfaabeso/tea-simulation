Last Updated: August 8, 2025

# Architecture

For now, the architecture is simplified where the `SimulationKernel` has an
accompanying `Interpreter`. For simplicity, *there is no need to implement a
separate `Command` data class*, since dictionaries would suffice in handling
additional arguments. For reference, below is a sample code that we will be
going for. Another reason for this dictionary approach is to discourage the
user from the interface to tinker with internal variables of the simulation.
However, setup commands directly use the classes since the commands are only
about adding objects and configuring the environment, deferring the syntax
and semantic checking to the Python interpreter and the classes themselves.
In fact, the task of the `Interpreter` became simpler, *or at least in the
setup process*: *it just checks if the argument is an instance of that class
portion*. These classes are more of treated as a dataclass to easily modify the
contents. What the simulation then does in `confirm` is to *take a deep copy*
of the appended objects and environment.

```python
from teasim import SimulationKernel, Environment
from teasim.entities import Container, Cup
import copy

sim = SimulationKernel()

# Add two containers, and three cups, under similar settings.
# We do not have to manually code every aspect since there are default values.

container_base_setup = Container(
    id="container", temp_init=100, vol_init=100
)

cup_base_setup = Cup(
    id="cup", temp_init=40, vol_init=50
)

# yes, ids have to be set up manually unfortunately

container_0_setup = copy.deepcopy(container_base_setup)
container_1_setup = copy.deepcopy(container_base_setup)

cup_0_setup = copy.deepcopy(cup_base_setup)
cup_1_setup = copy.deepcopy(cup_base_setup)
cup_2_setup = copy.deepcopy(cup_base_setup)

container_0_setup.id = "container0"
container_1_setup.id = "container1"

cup_0_setup.id = "cup0"
cup_1_setup.id = "cup1"
cup_2_setup.id = "cup2"

sim.add_objs([
    container_base_setup,
    container_base_setup,
    cup_base_setup,
    cup_base_setup,
    cup_base_setup
])

# alternatively:
# sim.add_obj(container_0_setup)
# sim.add_obj(container_1_setup)
# sim.add_obj(cup_0_setup)
# sim.add_obj(cup_1_setup)
# sim.add_obj(cup_2_setup)

env = Environment(
    cooling_rate=1, ambient_temp=20
)

sim.config_env(env)

status = sim.confirm_setup()

if status.success:
    # run simulation for 10s
    for i in range(10000):
        sim.advance()
        if i % 1000 == 0:
            sim_status = sim.view_status()
            print(sim_status)
else:
    print(status)

```

Putting commands as arguments instead of making a `Command` dataclass has the
advantage of making commands have equal importance, and further more, letting
them easily be subjected to the `Interpreter` class. Such an approach however,
is more appropriate when the `cmd` method is called.

## Steps

1. Call `add_obj` and `configure_env` commands. 
2. Confirm setup with `confirm` command.
3. We then use the `Interpreter` to perform `syntax` and `semantic` checks.
The `Interpreter` will return the `Success` status of those check stages.
4. If the *compilation* of the `add_obj` and `configure_env` commands are
successful, then the `advance` command may now be called. This implies that
there is an internal **flag** stored in the `SimulationKernel` to determine
if the simulation is ready to run, and thus `add_obj` and `configure_env`
cannot be invoked.
