class SimulationWarning(UserWarning):
    """Base Class for Simulation Warnings"""

# Critique:
# How do you successfully inform the user about the new id?
# or even the ids of unnamed entities?
class IdAlreadyExistsWarning(SimulationWarning):
    """Called when an id already exists."""