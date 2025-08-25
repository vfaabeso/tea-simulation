Last Updated: August 7, 2025

# Commands

This section discusses the proper use of commands, syntactically and
semantically.

**Syntax** refers to the arguments in the command dictionary, or sometimes
class (e.g. if non-existent arguments are there), and whether appropriate
data types are used or not.

**Semantics** refers to the logical coherence of the arguments.

## Setup Commands

These commands are intentionally strict, and hence, the program would halt if
the user has syntax and semantic errors.

### `add_obj`

Adds object/entity to the simulation. The program halts if `add_obj` command is
invoked after confirming the setup, by checking the `is_ready_to_run` flag and
prints an error.

* Syntax
```python
sim.cmd(action="add_obj", <Entity>)
```

### `configure_env`

Configures the `Environment`. Raises a warning `Status` if called again when
the previous environment configuration is successful.

* Syntax
```python
sim.cmd(action="configure_env", <Environment>)
```

### `confirm`

Confirms the current setup (objects added and the environment configured)
and compiles the setup. Returns a `Status` object to check if the setup is
valid. The `Interpreter` checks the syntactic and semantic validity of the
setup.

* Syntax
```python
sim.cmd(action="confirm")
```

* Return
`Status` class.

* Mechanics
Uses the `Interpeter` to check for the entities in the `entity_dict` and the
`environment`, both their syntax (implied by Python) and semantics (`SimObject`
has `validate()`). If successful, then the `is_ready_to_run` flag is set to
**True**.

## Simulation Commands

An optional field can be appended in the dictionaries: `is_strict`. By default,
this boolean is **False**, which means that the commands may be invoked but if
the arguments are incorrect, a warning message would be returned instead.

### `advance`

Advances the simulation by one tick.

* Syntax
```python
sim.cmd(action="advance")
```

### `view_obj`

Views the status of an object with a specific id, with select variables.

* Syntax
```python
sim.cmd(action="view_obj", {
    "id" <str>: str,
    "show_static" <bool>: False})
```

- show_static: if **True** then static variables such as initial variables
will also be shown. Otherwise, dynamic variables related to the simulation will
be shown.

* Semantics
- id: should refer to existing object

* Return <Dict>

### `view_status`

Views the status of the whole simulation, along with all status of the objects.
This uses the `view_status` function of the `Entity` class. To be more precise,
this command views the current tick, the environment state (if `verbose` is set
to **True**), and every object status. The `verbose` argument, if **True**
implies that the `show_static` of entities will be set to **True**.

* Syntax
```python
sim.cmd(action="view_status", {"verbose" <bool>: False})
```

* Return <Dict>

Example:
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


