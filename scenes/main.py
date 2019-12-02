import pygame

from pysmile.colors import Colors
from pysmile.components.name import NameComponent
from pysmile.entity import Entity
from pysmile.components.renderer import RendererComponent
from pysmile.components.transform import TransformComponent
from pysmile.components.key_control import KeyControlComponent
from pysmile.components.collisions.box_collider import BoxCollider
from pysmile.math.vector2 import Vector2
from pysmile.components.pygame_renderer import PyGameRendererComponent
from pysmile.gl.shader import Shader
from pysmile.renderers.image_renderer import ImageRenderer
from pysmile.tilemap.tileset import TileSet
from pysmile.renderers.tile_renderer import TileRenderer
from pysmile.renderers.text import TextRenderer

from components.move_component import MoveComponent
from components.pacman_collisions import PacmanCollisions
from objects.ghost_base import GhostBase
from scenes.base import Scene
from objects.field import Field
from renderers.object_renderer import ObjectRenderer
from objects.base_cell import Floor, Meta
from components.grain_collisions import GrainCollisions


class MainScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.field_obj = None

    def create_objects(self):
        self.field_obj = Field(self.game, 32)
        field = Entity()
        self.add_entity(field)
        shader = Shader.init_from_files("assets/shaders/walls/walls.vert", "assets/shaders/walls/walls.frag")
        field.add_component(TransformComponent(Vector2(0, 0)))
        field.add_component(PyGameRendererComponent(ObjectRenderer(self.field_obj), self.game.screen_size, shader))

        self.objects.append(GhostBase(self.game))

    def add_entities(self):
        grain = Entity()
        self.add_entity(grain)
        grain.add_component(TransformComponent(Vector2(205, 100)))
        grain.add_component(RendererComponent(ImageRenderer("./assets/images/grain.png"), (5, 5)))
        grain.add_component(NameComponent('grain'))

        score_label = Entity()
        self.add_entity(score_label)
        score_label.add_component(TransformComponent(Vector2(self.game.width - 200, 0)))
        score_label.add_component(PyGameRendererComponent(
            TextRenderer("score", font_size=18, color=Colors.white, font="assets/fonts/Emulogic.ttf"), (0, 0)))

        score = Entity()
        self.add_entity(score)
        score.add_component(TransformComponent(Vector2(self.game.width - 200, 20)))
        score.add_component(PyGameRendererComponent(
            TextRenderer("000", font_size=18, color=Colors.white, font="assets/fonts/Emulogic.ttf"), (0, 0)))

        high_score_label = Entity()
        self.add_entity(high_score_label)
        high_score_label.add_component(TransformComponent(Vector2(self.game.width - 200, 50)))
        high_score_label.add_component(PyGameRendererComponent(
            TextRenderer("high score", font_size=18, color=Colors.white, font="assets/fonts/Emulogic.ttf"), (0, 0)))

        high_score = Entity()
        self.add_entity(high_score)
        high_score.add_component(TransformComponent(Vector2(self.game.width - 200, 70)))
        high_score.add_component(PyGameRendererComponent(
            TextRenderer("000", font_size=18, color=Colors.white, font="assets/fonts/Emulogic.ttf"), (0, 0)))

        ts = TileSet()
        ts.load("./assets/tilesets/pacman_tiles.png", "./assets/tilesets/pacman.info")

        for i in range(3):
            pacman_live = Entity()
            self.add_entity(pacman_live)
            pacman_live.add_component(
                TransformComponent(Vector2(self.game.width - 200 + 34 * i, self.game.height - 100)))
            pacman_live.add_component(RendererComponent(TileRenderer(ts.tiles["pacman"], ts, animate=False), (32, 32)))

        player = Entity()
        self.add_entity(player)

        key_bindings = [[pygame.K_a], [pygame.K_d], [pygame.K_w], [pygame.K_s]]

        pacman_pos = self.field_obj.get_cells_by_type(Floor, Meta.pacman_spawn)[0].rect.xy

        player.add_component(MoveComponent(2))
        player.add_component(PacmanCollisions(self.field_obj))
        player.add_component(KeyControlComponent(key_bindings, MoveComponent))
        player.add_component(TransformComponent(Vector2(*pacman_pos)))
        player.add_component(BoxCollider((32, 32)))
        player.add_component(RendererComponent(TileRenderer(ts.tiles["pacman"], ts, animation_speed=0.3), (32, 32)))
        player.add_component(GrainCollisions())
