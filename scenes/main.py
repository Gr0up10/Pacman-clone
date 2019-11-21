import pygame

from pysmile.entity import Entity
from pysmile.components.renderer import RendererComponent
from pysmile.components.transform import TransformComponent
from pysmile.components.move import MoveComponent
from pysmile.components.key_control import KeyControlComponent
from pysmile.components.collisions.box_collider import BoxCollider
from pysmile.components.name import NameComponent
from pysmile.math.vector2 import Vector2
from pysmile.renderers.image_renderer import ImageRenderer

from objects.ghost_base import GhostBase
from scenes.base import Scene
from objects.grain import Grain


class MainScene(Scene):
    def create_objects(self):
        self.objects.append(GhostBase(self.game))
        self.objects.append(Grain(self.game))

    def add_entities(self):
        player = Entity()
        self.add_entity(player)

        key_bindings = [[pygame.K_a], [pygame.K_d], [pygame.K_w], [pygame.K_s]]

        player.add_component(MoveComponent(1, 2))
        player.add_component(KeyControlComponent(key_bindings))
        player.add_component(TransformComponent(Vector2(200, 200)))
        player.add_component(BoxCollider((16 * 2, 22 * 2), Vector2(0, 0)))
        player.add_component(RendererComponent(ImageRenderer("images/pacman.png"), (100, 100)))
