import pygame

from renderers.scene_renderer import SceneRenderer

from pysmile.scene import Scene as PSScene
from pysmile.components.game.game_event_manager import GameEventManagerComponent
from pysmile.events.update import UpdateEvent
from pysmile.entity import Entity
from pysmile.components.pygame_renderer import PyGameRendererComponent


class Scene(PSScene):
    def __init__(self, game):
        super().__init__(game)
        self.objects = []
        self.create_objects()
        self.add_entities()
        self.rederer = SceneRenderer()

        rend_entity = Entity()
        rend_entity.add_component(PyGameRendererComponent(self.rederer, game.screen_size))

    def bind_events(self):
        ev = self.game.get_component(GameEventManagerComponent)
        ev.bind(UpdateEvent, self.process_all_logic)

    def removed(self):
        ev = self.game.get_component(GameEventManagerComponent)
        ev.unbind(UpdateEvent, self.process_all_logic)

    def create_objects(self):
        pass

    def add_entities(self):
        pass

    def process_current_event(self, event):
        for item in self.objects:
            item.process_event(event)

    def process_all_logic(self, _):
        self.rederer.objects = self.objects

        for item in self.objects:
            item.process_logic()

    def set_next_scene(self, index):
        self.game.current_scene = index
