import pygame
from pysmile.component import Component
from pysmile.components.renderer import RendererComponent
from pysmile.events.key_press import KeyPressEvent
from pysmile.events.key_pressed import KeyPressedEvent
from pysmile.events.update import UpdateEvent
from pysmile.renderers.image_renderer import ImageRenderer

from components.ghost_move import GhostMoveComponent
from events.collect_grain import CollectBigGrainEvent
from objects.path_finder import RandomFinder, AFinder


class ScaryModeComponent(Component):
    scary_image_path = "./assets/images/ghosts/afraid_0.png"

    def __init__(self, scary_time=300):
        super().__init__()
        self.entity = None

        self.scary = False
        self.scary_time = scary_time
        self.time_pass = 0
        self.previous_renderer = None

    def update(self, _):
        if self.scary:
            self.time_pass += 1
            if self.time_pass >= self.scary_time:
                self.set_scary_mode(False)
                self.time_pass = 0

    def set_scary_mode(self, enable):
        self.scary = enable
        move_component = self.entity.get_component(GhostMoveComponent)
        move_component.set_path_finder(RandomFinder if self.scary else AFinder)
        move_component.update_target()
        self.entity.get_component(RendererComponent).renderer = \
            ImageRenderer(self.scary_image_path) if self.scary else self.previous_renderer

    def collect_big_grain(self, _):
        self.set_scary_mode(True)

    def press_key(self, event):
        if event.key == pygame.K_t:
            self.set_scary_mode(not self.scary)

    def applied_on_entity(self, entity):
        self.entity = entity
        self.previous_renderer = entity.get_component(RendererComponent).renderer
        self.entity.event_manager.bind(UpdateEvent, self.update)
        self.entity.event_manager.bind(CollectBigGrainEvent, self.collect_big_grain)
        self.entity.event_manager.bind(KeyPressEvent, self.press_key)

    def removed(self):
        self.entity.event_manager.unbind(UpdateEvent, self.update)
        self.entity.event_manager.unbind(CollectBigGrainEvent, self.collect_big_grain)
        self.entity.event_manager.unbind(KeyPressEvent, self.press_key)
