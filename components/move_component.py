from pysmile.component import Component
from pysmile.components.transform import TransformComponent
from pysmile.events.update import UpdateEvent
from pysmile.math.vector2 import Vector2
from pysmile.components.renderer import RendererComponent
from pysmile.renderers.tile_renderer import TileRenderer

from components.pacman_collisions import PacmanCollisions
from events.change_tile import PacmanChangeTileEvent
from objects.base_cell import Meta, Floor


class MoveComponent(Component):
    def __init__(self, speed):
        super().__init__()
        self.entity = None
        self.speed = speed
        self.direction = Vector2(1, 0)
        self.new_direction = None
        self.previous_tile = None

    def add_direction(self, x, y):
        self.new_direction = Vector2(x, y)

    def update(self, _):
        if self.direction.magnitude() == 0:
            return

        trans = self.entity.get_component(TransformComponent)
        collsion = self.entity.get_component(PacmanCollisions)
        if not trans or not collsion:
            return

        if self.new_direction and collsion.can_move_in_direction(self.new_direction):
            self.direction = self.new_direction
        elif not collsion.can_move_in_direction(self.direction):
            return

        rend = self.entity.get_component(RendererComponent)
        if isinstance(rend.renderer, TileRenderer):
            rend.renderer.flip = self.direction.x < 0
            if self.direction.y != 0:
                rend.renderer.rotation = 90 if self.direction.y > 0 else -90
            else:
                rend.renderer.rotation = None

        trans.position += self.direction * self.speed

        tile_size = collsion.field.size
        new_tile = Vector2(trans.x//tile_size, trans.y//tile_size)
        if self.previous_tile is None or self.previous_tile != new_tile:
            if not self.teleport(collsion.field, trans, Meta.teleport1, Meta.teleport2):
                self.teleport(collsion.field, trans, Meta.teleport2, Meta.teleport1)
            self.previous_tile = new_tile

            self.entity.event_manager.trigger_event(PacmanChangeTileEvent(self.entity))

    def teleport(self, field, trans, meta1, meta2):
        if not self.previous_tile:
            return
        prev_meta = field.get_cell_iter(int(self.previous_tile.x), int(self.previous_tile.y)).meta
        if meta1 in field.get_cell(trans.pos).meta and meta2 not in prev_meta:
            new_pos = field.get_cells_by_type(Floor, meta2)[0].rect.xy
            self.new_direction = self.direction
            trans.position = Vector2(new_pos + self.direction * field.size)
            return True
        return False

    def removed(self):
        self.entity.event_manager.bind(UpdateEvent, self.update)

    def applied_on_entity(self, entity):
        self.entity = entity
        entity.event_manager.bind(UpdateEvent, self.update)
