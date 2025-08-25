# import necessary libraries

class Entity(SimObject):
    def __init__(self, id="": str) -> None:
        self.id = id 

    # OVERRIDE
    def correct_values(self) -> None:
        pass
     
    # OVERRIDE
    def update_values(self, update_dict: dict) -> None:
        pass

    # OVERRIDE
    def view_status(self, show_static=False: bool) -> dict:
        pass
