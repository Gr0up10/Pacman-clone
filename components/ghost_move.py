import random

from pysmile.colors import Colors
from pysmile.component import Component
from pysmile.components.transform import TransformComponent
from pysmile.events.update import UpdateEvent
from pysmile.math.vector2 import Vector2

from components.move_component import MoveComponent
from events.change_tile import PacmanChangeTileEvent
from events.debug_line import DrawDebugLineEvent
from objects.base_cell import Meta
from objects.path_finder import Afinder


class GhostMoveComponent(Component):
    def __init__(self, field, speed, find_target, pacman, color=None):
        super().__init__()
        self.field = field
        self.speed = speed
        self.entity = None
        self.direction = None
        self.path_finder = Afinder(field)
        self.target = None
        self.find_target = find_target
        if not color:
            self.debug_line_color = Colors.from_rgb(*[random.randint(0, 255) for _ in range(3)]).to_float()
        else:
            self.debug_line_color = color.to_float()
        self.pacman = pacman

    def update(self, _):
        trans = self.entity.get_component(TransformComponent)
        if not trans:
            return
        if self.target and self.direction:
            if self.target == trans.pos:
                self.update_target()
            if not self.field.get_cell(trans.pos + self.direction * self.speed).state:
                self.update_target()
                return
            trans.position += self.direction * self.speed
        else:
            self.update_target()

    def update_direction(self, pos, tpos):
        new_vec = tpos - pos
        if new_vec.x != 0:
            self.direction = Vector2(1 if new_vec.x > 0 else -1, 0)
        elif new_vec.y != 0:
            self.direction = Vector2(0, 1 if new_vec.y > 0 else -1)

    def draw_line(self, pos):
        self.entity.event_manager.trigger_event(
            DrawDebugLineEvent([v + Vector2(16, 16) for v in [pos] + self.path],
                               self.debug_line_color))

    def pacman_move(self, event):
        self.pacman = event.pacman
        self.update_target()

    def update_target(self):
        if not self.pacman:
            return

        trans = self.entity.get_component(TransformComponent)
        target_pos = self.find_target(self.pacman, self.field, trans.pos)

        self.target = self.path_finder.find_path(trans.pos, target_pos)
        self.update_direction(trans.pos, self.target)
        self.entity.event_manager.trigger_event(DrawDebugLineEvent([trans.pos, self.target], self.debug_line_color))

    def removed(self):
        self.entity.event_manager.unbind(UpdateEvent, self.update)

    def applied_on_entity(self, entity):
        self.entity = entity
        self.entity.event_manager.bind(UpdateEvent, self.update)
