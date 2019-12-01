from pysmile.component import Component
from pysmile.components.name import NameComponent
from pysmile.components.transform import TransformComponent
from pysmile.events.update import UpdateEvent
import math


class GrainColisions(Component):
    def __init__(self):
        self.entity = None

    def update(self, _):
        # получаешь позицию пакмана
        trans = self.entity.get_component(TransformComponent)
        if trans is None:
            return
        # получаешь все entity со сцены у которых есть компонет name
        grains = self.entity.scene.get_entities_with_component(NameComponent)
        # фильтруешь entity и оставляешь только те у которых name == 'grain'
        grains = [g for g in grains if g.get_component(NameComponent).name == 'grain']
        for grain in grains:
            grain_pos = grain.get_component(TransformComponent)
            dist = math.sqrt((trans.x - grain_pos.x) ** 2 + (trans.y - grain_pos.y) ** 2)
            if dist <= 15:
                self.entity.scene.remove_entity(grain)

    def applied_on_entity(self, entity):
        self.entity = entity
        entity.event_manager.bind(UpdateEvent, self.update)
