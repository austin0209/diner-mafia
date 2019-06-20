from enum import IntEnum

class ItemType(IntEnum):
    FISH = 0
    COFFEE = 1
    EGGS = 2


class Item(object):
    def __init__(self, item_type):
        self.type = item_type
        
    