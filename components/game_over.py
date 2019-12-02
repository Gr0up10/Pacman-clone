from pysmile.component import Component
from scenes.menu import MenuScene
from events.collect_grain import CollectSmallGrainEvent


class GameOverComponent(Component):
    def __init__(self):
        super().__init__()
        self.entity = None
        self.grains_count = 0
        self.max_grains_count = 0

    def collect_grain(self, _):
        self.grains_count += 1
        if self.grains_count >= self.max_grains_count:
            self.entity.current_scene = MenuScene

    def removed(self):
        self.entity.event_manager.unbind(CollectSmallGrainEvent, self.collect_grain)

    def applied_on_entity(self, entity):
        self.entity = entity
        entity.event_manager.bind(CollectSmallGrainEvent, self.collect_grain)
