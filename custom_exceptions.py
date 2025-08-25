class SimulationError(Exception):
    """Base Class for Simulation Errors"""

class EntityTypeNotSupportedError(SimulationError):
    """Raised when a non-existent entity type is called."""

class IdAlreadyExistsError(SimulationError):
    """Called when an id already exists."""
    
class InvalidArgumentError(SimulationError):
    """Signifies that custom arguments (e.g. dictionaries) are syntactically
    and/or semantically invalid."""
        
class NonExistentObjectError(SimulationError):
    """Signifies that the object being selected does not exist, for example,
    when being queried in an id catalog."""

class SetupAlreadyConfirmedError(SimulationError):
    """Called when `SimulationKernel.confirm_setup()` is already 
    successfully invoked"""
    
class SimulationAlreadyConfirmedError(SimulationError):
    """Raised when setup commands are still called after the confirmation
    of the simulation setup."""

class SimulationNotReadyError(SimulationError):
    """Raised when certain methods are run even if the simulation is not yet
    set up properly and/or completely."""

class SemanticError(SimulationError):
    """Signifies semantic errors in the status of simulation variables."""

class DuplicateEntityIdError(SemanticError):
    """Raised if there are duplicate entity ids."""

class ValueOutOfRangeError(SemanticError):
    """Raised if the value is out of valid range."""

class LowerBoundError(ValueOutOfRangeError):
    """Raised if a value is below the accepted lower threshold."""

class UpperBoundError(ValueOutOfRangeError):
    """Raised if a value is above the accepted upper threshold."""

# schemas
class SchemaError(Exception):
    """Base schema error."""

class InvalidSchemaValueError(SchemaError):
    """Raised when the input value contradicts the schema constraints."""

class InconsistentBoundsError(SchemaError):
    """Raised when min > max in schema definition."""