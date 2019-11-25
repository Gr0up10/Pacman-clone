from pysmile.component import Component
from pysmile.components.transform import TransformComponent
from pysmile.events.update import UpdateEvent
from pysmile.math.vector2 import Vector2
from pysmile.components.renderer import RendererComponent
from pysmile.renderers.tile_renderer import TileRenderer

from components.pacman_collisions import PacmanCollisions


class MoveComponent(Component):
    def __init__(self, speed):
        super().__init__()
        self.entity = None
        self.speed = speed
        self.direction = Vector2(1, 0)
        self.previous_direction = self.direction
        self.new_direction = None

    def add_direction(self, x, y):
        self.direction = Vector2(x, y)

    def update(self, _):
        if self.direction.magnitude() == 0:
            return

        trans = self.entity.get_component(TransformComponent)
        collsion = self.entity.get_component(PacmanCollisions)
        if not trans or not collsion:
            return

        if not collsion.can_move_in_direction(self.direction):
            if collsion.can_move_in_direction(self.previous_direction):
                self.new_direction = self.direction
                self.direction = self.previous_direction
            else:
                return
        else:
            if self.new_direction:
                if collsion.can_move_in_direction(self.new_direction):
                    self.direction = self.new_direction
                    self.new_direction = None

        rend = self.entity.get_component(RendererComponent)
        if isinstance(rend.renderer, TileRenderer):
            rend.renderer.flip = self.direction.x < 0
            if self.direction.y != 0:
                rend.renderer.rotation = 90 if self.direction.y > 0 else -90
            else:
                rend.renderer.rotation = None

        trans.position += self.direction * self.speed
        self.previous_direction = self.direction

    def applied_on_entity(self, entity):
        self.entity = entity
        entity.event_manager.bind(UpdateEvent, self.update)
