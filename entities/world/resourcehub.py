from entities.entity import Entity
from entities.geometry.rectangle import Rectangle
from utilities.color import Color

class ResourceHub(Entity):

    # RESOURCE KEY:
    # 0 - RED
    # 1 - BLUE
    # 2 - GREEN
    # 3 - WHITE

    def __init__(self, x, y, width, height, resource_id):
        super(ResourceHub, self).__init__(x, y, width, height)
        self.id = resource_id
        if self.id == 0:
            self.color = Color.RED
        elif self.id == 1:
            self.color = Color.BLUE
        elif self.id == 2:
            self.color = Color.GREEN
        elif self.id == 3:
            self.color = Color.WHITE
        self.rect = Rectangle(x, y, width, height, 0, self.color)
    
    def update(self, delta_time):
        pass

    def draw(self, surface):
        self.rect.draw(surface)