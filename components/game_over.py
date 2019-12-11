import pygame
from pysmile.component import Component

from constants import Sounds
from events.play_sound import PlaySoundEvent
from scenes.menu import MenuScene
from events.collect_grain import CollectSmallGrainEvent, CollectBigGrainEvent
from events.game_over import GameOverEvent

from pysmile.colors import Colors
from pysmile.entity import Entity
from pysmile.components.transform import TransformComponent
from pysmile.math.vector2 import Vector2
from pysmile.components.pygame_renderer import PyGameRendererComponent
from pysmile.components.renderer import RendererComponent
from pysmile.renderers.text import TextRenderer
from pysmile.events.key_press import KeyPressEvent
from pysmile.components.animation import AnimationComponent
from pysmile.renderers.rect_renderer import RectRenderer
from pysmile.gl.shader import Shader


class GameOverComponent(Component):
    def __init__(self):
        super().__init__()
        self.entity = None
        self.grains_count = 0
        self.max_grains_count = 0

    def collect_grain(self, _):
        self.grains_count += 1
        if self.grains_count >= self.max_grains_count:
            self.game_over()
            #

    def go_to_menu(self):
        self.entity.current_scene = MenuScene

    def game_over_event(self, _):
        self.game_over()

    def game_over(self):
        print("game over")
        self.entity.event_manager.trigger_event(PlaySoundEvent(Sounds.DEATH, 0, 20))

        scene = self.entity.scene

        black_back = Entity()
        scene.add_entity(black_back)
        black_back.add_component(TransformComponent(Vector2(0, 0)))
        shader = Shader.init_from_files("assets/shaders/back/back.vert", "assets/shaders/back/back.frag")
        shader.inject_rect = False
        shader.uniform_alpha = 1.0
        black_back.add_component(RendererComponent(RectRenderer(Colors.black), self.entity.screen_size, shader))
        black_back.add_component(AnimationComponent(step=3, end=100,
                                                    function=lambda x: shader.set_uniform("alpha", x/100.0)))

        game_text = Entity()
        scene.add_entity(game_text)
        game_transform = TransformComponent(Vector2(0, self.entity.height/2-65))
        game_text.add_component(game_transform)
        game_text.add_component(PyGameRendererComponent(
            TextRenderer("Game", font_size=24, color=Colors.white, font="assets/fonts/Emulogic.ttf"), (0, 0)))
        game_text.add_component(AnimationComponent(step=10, end=self.entity.width/2 - 220,
                                function=lambda x: game_transform.position.update(x, game_transform.y)))

        over_text = Entity()
        scene.add_entity(over_text)
        over_transform = TransformComponent(Vector2(0, self.entity.height / 2 - 65))
        over_text.add_component(over_transform)
        over_text.add_component(PyGameRendererComponent(
            TextRenderer("Over", font_size=24, color=Colors.white, font="assets/fonts/Emulogic.ttf"), (0, 0)))
        over_text.add_component(AnimationComponent(step=-22, start=self.entity.width, end=self.entity.width / 2 - 110,
                                function=lambda x: over_transform.position.update(x, game_transform.y)))

        self.entity.add_component(AnimationComponent(end=80, completion=self.go_to_menu))

    def removed(self):
        self.entity.event_manager.unbind(CollectSmallGrainEvent, self.collect_grain)
        self.entity.event_manager.unbind(CollectBigGrainEvent, self.collect_grain)
        self.entity.event_manager.unbind(KeyPressEvent, self.key_press)
        self.entity.event_manager.unbind(GameOverEvent, self.game_over_event)

    def key_press(self, ev):
        if ev.key == pygame.K_g:
            self.game_over()

    def applied_on_entity(self, entity):
        self.entity = entity
        entity.event_manager.bind(CollectSmallGrainEvent, self.collect_grain)
        entity.event_manager.bind(CollectBigGrainEvent, self.collect_grain)
        entity.event_manager.bind(KeyPressEvent, self.key_press)
        entity.event_manager.bind(GameOverEvent, self.game_over_event)
