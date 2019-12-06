from pysmile.component import Component
from pysmile.components.name import NameComponent
from pysmile.components.transform import TransformComponent
from pysmile.components.collisions.box_collider import BoxCollider
from pysmile.events.update import UpdateEvent
from pysmile.math.vector2 import Vector2
import math
from events.collect_grain import CollectSmallGrainEvent, CollectBigGrainEvent
from events.play_sound import PlaySoundEvent
from constants import Sounds


class GrainCollisions(Component):
    def __init__(self):
        self.entity = None

    def update(self, _):
        # получение позиции пакмана
        col = self.entity.get_component(BoxCollider).get_collider()[0]
        if col is None:
            return
        # получение всех entity со сцены у которых есть компонет name
        grains = self.entity.scene.get_entities_with_component(NameComponent)
        # фильтрование entity и остаются только те у которых name == 'grain'
        grains = [g for g in grains if 'grain' in g.get_component(NameComponent).name]
        for grain in grains:
            # получение позиции зерна
            grain_pos = grain.get_component(TransformComponent)
            # вычисление дистанции между зерном и пакманом
            pos = Vector2(col.centerx, col.centery)
            dist = math.sqrt((pos.x - grain_pos.x) ** 2 + (pos.y - grain_pos.y) ** 2)
            # проверка расстояния между зерном и пакманом
            if dist <= 16:
                if 'big' in grain.get_component(NameComponent).name:
                    self.entity.event_manager.trigger_event(CollectBigGrainEvent())
                else:
                    self.entity.event_manager.trigger_event(CollectSmallGrainEvent())
                self.entity.scene.remove_entity(grain)
                self.entity.event_manager.trigger_event(PlaySoundEvent(Sounds.CHOMP, -1, 20))

    def removed(self):
        self.entity.event_manager.unbind(UpdateEvent, self.update)

    def applied_on_entity(self, entity):
        self.entity = entity
        entity.event_manager.bind(UpdateEvent, self.update)
