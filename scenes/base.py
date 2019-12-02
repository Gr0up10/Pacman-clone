from renderers.scene_renderer import SceneRenderer

from pysmile.scene import Scene as PSScene
from pysmile.components.game.game_event_manager import GameEventManagerComponent
from pysmile.events.update import UpdateEvent
from pysmile.events.pygame_event import PyGameEvent
from pysmile.entity import Entity
from pysmile.components.pygame_renderer import PyGameRendererComponent
from pysmile.components.transform import TransformComponent
from pysmile.math.vector2 import Vector2
from pysmile.component import Component


class Scene(PSScene):
    def __init__(self, game):
        super().__init__(game)
        self.objects = []
        self.create_objects()
        self.rederer = SceneRenderer()

        rend_entity = Entity()
        self.add_entity(rend_entity)
        rend_entity.add_component(TransformComponent(Vector2(0, 0)))
        rend_entity.add_component(PyGameRendererComponent(self.rederer, game.screen_size))

        self.add_entities()

    def bind_events(self):
        ev = self.game.get_component(GameEventManagerComponent)
        ev.bind(UpdateEvent, self.process_all_logic)
        ev.bind(PyGameEvent, self.process_current_event)

    def removed(self):
        for ent in self.entities:
            [c.removed() for c in ent.get_components(Component)]

        ev = self.game.get_component(GameEventManagerComponent)
        ev.unbind(UpdateEvent, self.process_all_logic)
        ev.unbind(PyGameEvent, self.process_current_event)

    def create_objects(self):
        pass

    def add_entities(self):
        pass

    def process_current_event(self, pg_event):
        event = pg_event.event
        for item in self.objects:
            item.process_event(event)

    def process_all_logic(self, _):
        self.rederer.set_objects(self.objects)

        for item in self.objects:
            item.process_logic()

    def set_next_scene(self, scene):
        self.game.current_scene = scene
