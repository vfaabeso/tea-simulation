class Entity:
    def __init__(self, id: str) -> None:
        self.id = id

    # this is called every time we initialize variables
    def _validate(self) -> None:
        raise NotImplementedError

    # def correct_values(self) -> None:
    #     raise NotImplementedError
    
    def update_values(self, update_dict: dict) -> None:
        raise NotImplementedError
    
    def to_json(self, show_static: bool=False) -> dict:
        raise NotImplementedError
    
