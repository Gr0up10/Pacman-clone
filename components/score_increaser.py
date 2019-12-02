from pysmile.component import Component
from pysmile.components.pygame_renderer import PyGameRendererComponent
from events.collect_grain import CollectSmallGrainEvent


class ScoreIncreaserComponent(Component):
    def __init__(self):
        super().__init__()
        self.entity = None

    def collect_small_grain(self, _):
        score = self.entity.get_component(PyGameRendererComponent)
        score.renderer.text = "{:03d}".format(int(score.renderer.text) + 1)

    def applied_on_entity(self, entity):
        print("bind")
        self.entity = entity
        entity.event_manager.bind(CollectSmallGrainEvent, self.collect_small_grain)
