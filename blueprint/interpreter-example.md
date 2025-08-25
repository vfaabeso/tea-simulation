# Interpreter Example

Suppose that the commands are the following

## Input

```
Command(agent="Player0", command="pour", is_strict=False, {
    "from": "Container0", "to": "Cup0", "volume": 100
})

Command(agent="Player1", command="pour", is_strict=False, {
    "from": "Container1", "to": "Cup0", "volume": 100
})

```

## Commit

### Verify

#### Syntax Checking

This stage would suggest that the inputs are syntactically correct.

#### Expound

In this stage, implicit inference of missing fields are appended to the object
part of the commands. In our case, pouring requires the temperatures of the
container and the cup. The result of this stage would be as follows.

```
Command(agent="Player0", command="pour", is_strict=False, {
    "from": "Container0", "to": "Cup0", "volume": 100,
    "from_volume": 950, "to_volume": 20,
    "from_temp": 95, "to_temp": 20
})

Command(agent="Player1", command="pour", is_strict=False, {
    "from": "Container1", "to": "Cup0", "volume": 100,
    "from_volume": 850, "to_volume": 20,
    "from_temp": 85, "to_temp": 20
})

```

#### Semantic Check 

