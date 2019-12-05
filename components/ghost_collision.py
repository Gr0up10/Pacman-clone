from pysmile.component import Component
from pysmile.components.transform import TransformComponent
from pysmile.events.update import UpdateEvent
from pysmile.components.collisions.collider import Collider
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
        collider = col.get_collider()[0]

        for ghost in self.ghosts:
            if collider.colliderect(ghost.rect):
                self.entity.event_manager.trigger_event(GameOverEvent())
                self.entity.remove_component(GhostCollision)
                return

    def removed(self):
        self.entity.event_manager.unbind(UpdateEvent, self.update)

    def applied_on_entity(self, entity):
        self.entity = entity
        entity.event_manager.bind(UpdateEvent, self.update)
