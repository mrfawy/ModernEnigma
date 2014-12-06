from Switch import Switch
from CharIndexMap import CharIndexMap
from Wiring import Wiring
class PlugBoard(Switch):
    def __init__(self,wiring):
        super().__init__(wiring)
