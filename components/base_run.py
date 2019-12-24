from pysmile.component import Component
from pysmile.components.renderer import RendererComponent
from pysmile.components.transform import TransformComponent
from pysmile.events.update import UpdateEvent
from pysmile.math.vector2 import Vector2
from pysmile.renderers.image_renderer import ImageRenderer

from components.ghost_move import GhostMoveComponent
from components.scary_mode import ScaryModeComponent
from objects.base_cell import Meta, Floor


class BaseRunComponent(Component):
    dead_image_path = "./assets/images/ghosts/dead.png"

    def __init__(self, speed=4):
        self.entity = None
        self.speed = speed
        self.previous_speed = None
        self.previous_find = None
        self.previous_renderer = None
        self.target = None
        self.field = None

    def update(self, _):
        pos = self.entity.get_component(TransformComponent).pos
        if Meta.ghost_spawn in self.field.get_cell(pos).meta:
            self.entity.get_component(RendererComponent).renderer = self.previous_renderer
            ghost_move = self.entity.get_component(GhostMoveComponent)
            ghost_move.speed = self.previous_speed
            ghost_move.find_target = self.previous_find
            self.entity.remove_component(BaseRunComponent)

    def applied_on_entity(self, entity):
        self.entity = entity
        self.entity.event_manager.bind(UpdateEvent, self.update)

        self.entity.get_component(ScaryModeComponent).set_scary_mode(False)
        self.previous_renderer = self.entity.get_component(RendererComponent).renderer
        self.entity.get_component(RendererComponent).renderer = ImageRenderer(self.dead_image_path)
        ghost_move = self.entity.get_component(GhostMoveComponent)
        self.field = ghost_move.field
        self.previous_speed = ghost_move.speed
        ghost_move.speed = self.speed
        self.previous_find = ghost_move.find_target
        ghost_move.find_target = self.find_target

    @staticmethod
    def find_target(pacman, field, pos):
        return Vector2(*field.get_cells_by_type(Floor, Meta.ghost_spawn)[0].rect.xy)

    def removed(self):
        self.entity.event_manager.unbind(UpdateEvent, self.update)
