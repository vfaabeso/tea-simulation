Last Updated: August 5, 2025

> Note: These commands include commands during the simulation.

# Current Commands

## Commands (High-Level)

These commands are executed while the setup is already configured.

1. Pour Liquid
- Spigot to Container
- Container to Cup
- Container to Container
- Cup to Cup
2. Discard Liquid
- From Container
- From Cup
3. Add Tea Leaves
- To Container
- To Cup
4. Toggle Container Heater

## Meta Commands

### Configuration

1. Add Objects
2. Configure Environment
3. Confirm Setup

### During Simulation

1. View Objects
2. Get Object State
3. Insert Command
4. Commit
5. Update

# Previous Commands

view_items()
- Views objects inside the simulation.
- The objects then should have a name tag.
- This results in viewing all objects along their fundamental characteristics.

get_state(name_tag)
- Prints the state of the object with a given name tag

add_water(name_tag, volume, temperature)
- Adds water to object

subtract_water(name_tag, volume)
- Removes water from object

commit()
- Compiles the commands inserted so far
- Checks if there are errors in the inserted list of commands
- Used to check if we are ready to call the update function
- There will be a flag to check if the commands are successfully compiled
Otherwise, calling update will fail or be not allowed.

update(dt)
- Updates the whole simulation by one tick

# Challenges

What if the player calls add_water then subtract_water?
- One possible solution is that we subtract_water first before we add water
This avoids the complication in adjusting the temperature of the water

- It is likely that in the compile or commit method,
we will group the commands by name_tag, so that adding water to one cup
is different from adding water to another cup.

# Further Fixes
- We can aggregate the changes by differentiating source and target in
add/subtract water classes, and on a larger scope, by name_tag. We can call
this aggregation in a class called DeltaObject
