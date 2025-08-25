# Simulation Architecture

We can simplify the whole process into three steps: `input`, `commit`, and
`update`.

## Input 

Before committing, the `Simulation` accepts **command dictionaries** which are 
stored in the `Simulation` instance. To be precise, these **command dictionaries**
pertain to commands that will change the state of the simulation. This is 
different from **meta-commands** which refer to commands about the commands 
themselves, for example, **input**, **view_commands**, etc.

### Command Dictionary 

Important fields in the dictionary include:
- agent : str - identifier which agent the command is delegated from
- command : str - the identifier (or name) of the command, e.g. add, pour
- is_strict : bool - if True, then the simulation would come to halt
when such an invalid command is inputted, default to False, which delivers
warnings instead

#### Considerations

We can change this command dictionary into a `Command` class, with additional
parameters encapsulated to a dictionary, like so:

```
Command(agent="Player0", command="pour", is_strict=False, {
    "from": "Container0", "to": "Cup0", "volume": 100
})
```

## Commit 

The `Simulation` calls the `Interpreter` to **verify** and **process** the 
inserted commands. These are the two primary stages of the interpreter.
**verify** aims to check if all of the commands are valid, and returns a **status**
if there are inconsistencies within the command dictionary list, while
**process** simplifies, batches, and orders the commands, and returns
**status** that the commands are ready to be executed. To enforce rigidity,
*inputs cannot be further accepted once the commands have been committed
successfully*. To clarify, we can think of this commit process as **deferring**
commands to the simulator.

### Verify 

This commit stage verifies the inputted commands before going into further
stages. This includes checking if the commands would be possible to perform by
the `Player` or `Agent` simultaneously, thus requiring some access to the
simulation's `ActionBuffer`. We can split this stage into `syntax_checking`, 
`expound`, `semantic_check`, and `collision_check` substages.

#### Syntax Checking

This checks the correctness of the `Commmand` instance.

#### Expound

The task of this stage is to append implicit fields in each of the `Command`
classes such as **duration** for tasks that require more than one tick. For 
example, take the **pour** command, we can calculate the **duration** by using
the flow rate of the origin medium (e.g. Container).

#### Collision Check

This substage ensures that there are no tasks that will collide with 
`ActionBuffer`, in cases where the agent cannot do things simultaneously.
Furthermore, we will consider **blocking**, to check the current conditions of
objects, such as if they are being held by agents.

#### Considerations

This verify stage may be excluded from the interpreter process since it couples
with the `Simulation`. However, the **Syntax Checking** substage is a task 
appropriate for `Interpreter`, while **Expound** and **Collision Check**
depends a lot from `Simulation`.

### Process 

This stage can be split into five substages: `simplify`, `batching`,
`ordering`, `grouping`, and `delegate`.

#### Simplify 

An example of this is if we have to deal with compound commands, for example,
co-dependent commands. Take the `pour()` command for example. This may be 
structured as `pour(from, to, volume)`. Since we are going to `batch` these 
commands per object, we will then split them into appropriate commands such as 
`add(obj, volume, obj.temp)` and `sub(obj, volume)`.

#### Batching 

In this stage, we batch the commands from the `simplify` stage per simulation 
object, for example, commands for Container1 will be batched apart from
commands for other object instances.

#### Ordering 

Per batch, we then order the commands, for example, volume subtraction comes
first before volume addition (with temperature).

#### Grouping

Since the commands are ordered per batch, we can further group the commands
by tuple so that the `Simulation` will handle how would such grouped commands
be dealt with. After all, this is simply the interpreter and thus we do not 
need to simplify these commands by physics laws, and simply delegate it to the
simulator or engine.

#### Delegate 

In this substage, we finally append the resulting commands to the `ActionBuffer`
to be consumed in the `Update` stage.

## Update 

The update function is called without arguments. Previously, we have argued
that this method can be invoked once the commands are committed by some time 
*dt*. *dt* is in tick units, and tick units are to be set when the `Simulation`
is being set up. We can add *future flexibility* in this so that *dt > 1*.
But this is nonsensical: how would commands be processed after the first *dt*?
Therefore, we can call the update without the *dt* argument. Overall, the 
`update` function updates `SimulationState` by one tick.

The `update` function can be split into `consume`, `simplify`, `process`, and
`advance` stages.

### Consume 

For commands that are in the `ActionBuffer`, at this point, the command has a 
**remaining ticks** field. We collect the necessary components such as volume,
temperature, tea amount, etc. for the `simplify` stage. After this collection,
we decrement **remaining ticks** by one, and once the **remaining ticks** reach
zero, they are removed from the buffer. Additionally, we remove associated
`locks` if the command is exhausted. At the same time, `locks` will be enforced
once a command has been consumed.

### Simplify

Since the commands are now grouped, we will simplify them with the use of a 
`BufferLiquid`. For example, if there are two `add` commands, we then first add
the first command to that buffer liquid (currently empty), and then add the 
second liquid, calculating properties such as resulting volume, tea granular
amount, and temperature (by averaging). Though, this `BufferLiquid` might only
be useful *when we talk about adding liquids together*.

### Process

We can then finally process those liquids from `BufferLiquid` to the object we
are pertaining to, and add them to the target medium. Or if we are subtracting
liquids, simply remove them from the medium.

### Advance

This is where we apply our knowledge in ODE where the state of the variables
are updated by physics laws by one tick.

# Comments

# Further Challenges

1. It would be appropriate to provide test cases for such a sophisitcated
engine.
