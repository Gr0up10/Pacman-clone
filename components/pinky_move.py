from pysmile.component import Component
from pysmile.components.transform import TransformComponent
from pysmile.events.update import UpdateEvent
from pysmile.math.vector2 import Vector2

from components.move_component import MoveComponent
from events.change_tile import PacmanChangeTileEvent
from events.debug_line import DrawDebugLineEvent
from objects.base_cell import Meta
from objects.path_finder import Afinder


class PinkyMoveComponent(Component):
    def __init__(self, field, speed):
        super().__init__()
        self.field = field
        self.speed = speed
        self.entity = None
        self.direction = None
        self.path_finder = Afinder(field)
        self.path = None
        self.current_vert = None

    def update(self, _):
        trans = self.entity.get_component(TransformComponent)
        if not trans:
            return
        if self.path is not None and self.current_vert is not None:
            if self.path[self.current_vert] == trans.pos or self.direction is None:
                self.current_vert += 1
                if self.current_vert >= len(self.path):
                    self.path = None
                    return
                self.update_direction(trans.pos, self.path[self.current_vert])

            trans.position += self.direction * self.speed

    def update_direction(self, pos, tpos):
        new_vec = tpos - pos
        if new_vec.x != 0:
            self.direction = Vector2(1 if new_vec.x > 0 else -1, 0)
        elif new_vec.y != 0:
            self.direction = Vector2(0, 1 if new_vec.y > 0 else -1)

    def update_target(self, event):
        def vec2tuple(vec):
            return int(vec.x), int(vec.y)

        pac_pos = event.pacman.get_component(TransformComponent).pos
        dir = event.pacman.get_component(MoveComponent).direction
        cell_pos = Vector2(pac_pos.x//self.field.size, pac_pos.y//self.field.size)
        c_dirs = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]
        for i in range(4):
            cell = self.field.get_cell_iter(*vec2tuple(cell_pos))
            next_cell = self.field.get_cell_iter(*vec2tuple(cell_pos+dir))
            if (Meta.ghost_turn in cell.meta and not next_cell.state) or cell.state:
                for c_dir in c_dirs:
                    new_pos = cell_pos + c_dir
                    if c_dir.x != -dir.x and c_dir.y != -dir.y and self.field.get_cell_iter(*vec2tuple(new_pos)).state:
                        dir = c_dir
            cell_pos += dir

        target_pos = cell_pos * self.field.size

        trans = self.entity.get_component(TransformComponent)
        self.path = self.path_finder.find_path(trans.pos, target_pos)
        self.current_vert = 0
        self.update_direction(trans.pos, self.path[self.current_vert])
        self.entity.event_manager.trigger_event(DrawDebugLineEvent([v + Vector2(16, 16) for v in self.path + [target_pos]]))

    def removed(self):
        self.entity.event_manager.unbind(UpdateEvent, self.update)
        self.entity.event_manager.unbind(PacmanChangeTileEvent, self.update_target)

    def applied_on_entity(self, entity):
        self.entity = entity
        self.entity.event_manager.bind(UpdateEvent, self.update)
        self.entity.event_manager.bind(PacmanChangeTileEvent, self.update_target)