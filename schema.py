import custom_exceptions as cex
from utils import number

class Schema:
    def __init__(self, var_type:type, min_val:number=None,
                  max_val:number=None) -> None:
        self._type = var_type
        self._min = min_val
        self._max = max_val
        # validate
        self._init_validate()

    def _init_validate(self) -> None:
        """
        Validate the initialized schema.
        """
        if self._min is not None and self._max is not None \
            and self._min > self._max:
            raise cex.InconsistentBoundsError(
                f"Minimum value {self._min} is higher than the \
                    maximum value {self._max}"
            )
        
    def validate(self, value: any) -> None:
        # check if type is different
        if not isinstance(value, self._type):
            raise cex.InvalidSchemaValueError(
                f"Type {self._type} does not match the value {value}."
            )
        # for upper and lower bounds
        if isinstance(value, number):
            if self._min is not None and self._min > value:
                raise cex.InvalidSchemaValueError(
                    f"Minimum value {self._min} is larger than the input value\
                        {value}."
                )
            if self._max is not None and self._max < value:
                raise cex.InvalidSchemaValueError(
                    f"Input value {value} is larger than the maximum value\
                        {self._max}."
                )
            