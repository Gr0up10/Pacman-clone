import pygame

from pysmile.entity import Entity
from pysmile.components.renderer import RendererComponent
from pysmile.components.transform import TransformComponent
from pysmile.components.key_control import KeyControlComponent
from pysmile.components.collisions.box_collider import BoxCollider
from pysmile.math.vector2 import Vector2
from pysmile.components.pygame_renderer import PyGameRendererComponent
from pysmile.gl.shader import Shader
from pysmile.tilemap.tileset import TileSet
from pysmile.renderers.tile_renderer import TileRenderer

from components.move_component import MoveComponent
from components.pacman_collisions import PacmanCollisions
from objects.ghost_base import GhostBase
from scenes.base import Scene
from objects.field import Field
from objects.grain import Grain
from renderers.object_renderer import ObjectRenderer
from objects.base_cell import Floor, Meta


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
        self.objects.append(Grain(self.game))

    def add_entities(self):
        player = Entity()
        self.add_entity(player)

        key_bindings = [[pygame.K_a], [pygame.K_d], [pygame.K_w], [pygame.K_s]]

        ts = TileSet()
        ts.load("./assets/tilesets/pacman_tiles.png", "./assets/tilesets/pacman.info")

        pacman_pos = self.field_obj.get_cells_by_type(Floor, Meta.pacman_spawn)[0].rect.xy

        player.add_component(MoveComponent(2))
        player.add_component(PacmanCollisions(self.field_obj))
        player.add_component(KeyControlComponent(key_bindings, MoveComponent))
        player.add_component(TransformComponent(Vector2(*pacman_pos)))
        player.add_component(BoxCollider((32, 32)))
        player.add_component(RendererComponent(TileRenderer(ts.tiles["pacman"], ts, animation_speed=0.3), (32, 32)))
