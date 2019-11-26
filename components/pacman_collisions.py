from pysmile.component import Component
from pysmile.components.transform import TransformComponent
from pysmile.components.collisions.collider import Collider
from objects.base_cell import Wall


class PacmanCollisions(Component):
    def __init__(self, field):
        super().__init__()
        self.field = field
        self.entity = None

    def can_move_in_direction(self, direction):
        trans = self.entity.get_component(TransformComponent)
        col = self.entity.get_component(Collider)
        if not trans or not col:
            return

        collider = col.get_collider()[0].move(direction)
        cells = self.field.get_cells_around(trans.position + direction)
        for cell in cells:
            if isinstance(cell, Wall) and cell.rect.colliderect(collider):
                return False
        return True

    def applied_on_entity(self, entity):
        self.entity = entity
