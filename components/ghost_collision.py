from pysmile.component import Component
from pysmile.components.transform import TransformComponent
from pysmile.events.update import UpdateEvent
from pysmile.components.collisions.collider import Collider
from pysmile.math.vector2 import Vector2

from components.base_run import BaseRunComponent
from components.scary_mode import ScaryModeComponent
from events.add_score import AddScoreEvent
from events.game_over import GameOverEvent


class GhostCollision(Component):
    def __init__(self, ghosts):
        super().__init__()
        self.entity = None
        self.ghosts = ghosts

    def update(self, _):
        col = self.entity.get_component(Collider)
        if not col:
            return
        pacman_center = Vector2(*col.get_collider()[0].center)

        for ghost in self.ghosts:
            ghost_center = Vector2(*ghost.get_component(Collider).get_collider()[0].center)
            if ghost_center.distance_to(pacman_center) < 32:
                if ghost.contains_component(BaseRunComponent):
                    return
                if ghost.get_component(ScaryModeComponent).scary:
                    self.entity.event_manager.trigger_event(AddScoreEvent(200))
                    ghost.add_component(BaseRunComponent())
                    return
                self.entity.event_manager.trigger_event(GameOverEvent())
                self.entity.remove_component(GhostCollision)
                return

    def removed(self):
        self.entity.event_manager.unbind(UpdateEvent, self.update)

    def applied_on_entity(self, entity):
        self.entity = entity
        entity.event_manager.bind(UpdateEvent, self.update)
