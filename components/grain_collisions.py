from pysmile.component import Component
from pysmile.components.name import NameComponent
from pysmile.components.transform import TransformComponent
from pysmile.events.update import UpdateEvent
import math
from events.collect_grain import CollectSmallGrainEvent


class GrainCollisions(Component):
    def __init__(self):
        self.entity = None

    def update(self, _):
        # получение позиции пакмана
        trans = self.entity.get_component(TransformComponent)
        if trans is None:
            return
        # получение всех entity со сцены у которых есть компонет name
        grains = self.entity.scene.get_entities_with_component(NameComponent)
        # фильтрование entity и остаются только те у которых name == 'grain'
        grains = [g for g in grains if g.get_component(NameComponent).name == 'grain']
        for grain in grains:
            # получение позиции зерна
            grain_pos = grain.get_component(TransformComponent)
            # вычисление дистанции между зерном и пакманом
            dist = math.sqrt((trans.x - grain_pos.x) ** 2 + (trans.y - grain_pos.y) ** 2)
            # проверка расстояния между зерном и пакманом
            if dist <= 13:
                self.entity.event_manager.trigger_event(CollectSmallGrainEvent())
                self.entity.scene.remove_entity(grain)

    def removed(self):
        self.entity.event_manager.unbind(UpdateEvent, self.update)

    def applied_on_entity(self, entity):
        self.entity = entity
        entity.event_manager.bind(UpdateEvent, self.update)
