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

from components.ghost_collision import GhostCollision
from components.line_handler import LineHandlerComponent
from components.move_component import MoveComponent
from components.music_player import MusicPlayerComponent
from components.object_update import ObjectUpdate
from components.ghost_move import GhostMoveComponent
from components.scary_mode import ScaryModeComponent
from components.score_increaser import ScoreIncreaserComponent
from components.pacman_collisions import PacmanCollisions
from events.debug_line import DrawDebugLineEvent
from objects.ghost_base import GhostBase

from objects.ghost_move import GhostMove
from renderers.line_renderer import LineRenderer

from scenes.base import Scene
from objects.field import Field
from renderers.object_renderer import ObjectRenderer
from objects.base_cell import Floor, Meta
from components.grain_collisions import GrainCollisions
from components.game_over import GameOverComponent
from objects.scoreboard import ScoreBoard


class MainScene(Scene):
    def __init__(self, game):
        self.game_over = GameOverComponent()
        game.add_component(self.game_over)
        game.add_component(MusicPlayerComponent())

        self.scoreboard = ScoreBoard()
        self.ghost_obj = None
        self.field_obj = None
        self.pinky = None
        super().__init__(game)

    def create_objects(self):
        self.field_obj = Field(self.game, 32)
        self.ghost_obj = GhostMove(self.game, self.field_obj)

        field = Entity()
        self.add_entity(field)
        shader = Shader.init_from_files("assets/shaders/walls/walls.vert", "assets/shaders/walls/walls.frag")
        field.add_component(TransformComponent(Vector2(0, 0)))
        field.add_component(
            PyGameRendererComponent(ObjectRenderer(self.field_obj), self.game.screen_size, True, shader))

    def add_grain(self, rect, size, big=False):
        grain = Entity()
        self.add_entity(grain)
        grain.add_component(TransformComponent(Vector2(rect.x + rect.w / 2 - size / 2,
                                                       rect.y + rect.h / 2 - size / 2)))
        grain.add_component(RendererComponent(ImageRenderer("./assets/images/small_grain.png"), (size, size)))
        grain.add_component(NameComponent('grain' + ('big' if big else '')))

    def removed(self):
        super().removed()
        self.game.remove_component(GameOverComponent)
        self.game.remove_component(MusicPlayerComponent)

    def add_entities(self):
        grain_size = 8
        for g in self.field_obj.get_cells_by_type(Floor, Meta.grain_small):
            self.game_over.max_grains_count += 1
            self.add_grain(g.rect, grain_size)

        big_grain_size = 16
        for g in self.field_obj.get_cells_by_type(Floor, Meta.grain_big):
            self.game_over.max_grains_count += 1
            self.add_grain(g.rect, big_grain_size, True)

        player = Entity()

        ghost_pos = self.field_obj.get_cells_by_type(Floor, Meta.ghost_spawn)
        self.pinky = Entity()
        self.add_entity(self.pinky)
        self.pinky.add_component(TransformComponent(Vector2(*ghost_pos[0].rect.xy)))
        self.pinky.add_component(BoxCollider((32, 32)))
        self.pinky.add_component(RendererComponent(ImageRenderer("assets/images/ghosts/pink.png"), (32, 32)))
        self.pinky.add_component(GhostMoveComponent(self.field_obj, 2, self.pinky_find_target, player, Colors.pink))
        self.pinky.add_component(ScaryModeComponent())

        red = Entity()
        self.add_entity(red)
        red.add_component(TransformComponent(Vector2(*ghost_pos[1].rect.xy)))
        red.add_component(BoxCollider((32, 32)))
        red.add_component(RendererComponent(ImageRenderer("assets/images/ghosts/red.png"), (32, 32)))
        red.add_component(GhostMoveComponent(self.field_obj, 2, self.red_find_target, player, Colors.red))
        red.add_component(ScaryModeComponent())

        inky = Entity()
        self.add_entity(inky)
        inky.add_component(TransformComponent(Vector2(*ghost_pos[2].rect.xy)))
        inky.add_component(BoxCollider((32, 32)))
        inky.add_component(RendererComponent(ImageRenderer("assets/images/ghosts/blue.png"), (32, 32)))
        inky.add_component(GhostMoveComponent(self.field_obj, 2, self.inky_find_target, player, Colors.purple))
        inky.add_component(ScaryModeComponent())

        debug_line = Entity()
        self.add_entity(debug_line)
        debug_line.add_component(TransformComponent(Vector2(0, 0)))
        debug_line.add_component(RendererComponent(LineRenderer(), (0, 0)))
        debug_line.add_component(LineHandlerComponent())

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
        score.add_component(ScoreIncreaserComponent())

        high_score_label = Entity()
        self.add_entity(high_score_label)
        high_score_label.add_component(TransformComponent(Vector2(self.game.width - 200, 50)))
        high_score_label.add_component(PyGameRendererComponent(
            TextRenderer("high score", font_size=18, color=Colors.white, font="assets/fonts/Emulogic.ttf"), (0, 0)))

        high_score_num = self.scoreboard.get_instance(0)[1]
        high_score = Entity()
        self.add_entity(high_score)
        high_score.add_component(TransformComponent(Vector2(self.game.width - 200, 70)))
        high_score.add_component(PyGameRendererComponent(
            TextRenderer(str(high_score_num), font_size=18, color=Colors.white, font="assets/fonts/Emulogic.ttf"),
            (0, 0)))

        ts = TileSet()
        ts.load("./assets/tilesets/pacman_tiles.png", "./assets/tilesets/pacman.info")

        for i in range(3):
            pacman_live = Entity()
            self.add_entity(pacman_live)
            pacman_live.add_component(
                TransformComponent(Vector2(self.game.width - 200 + 34 * i, self.game.height - 100)))
            pacman_live.add_component(RendererComponent(TileRenderer(ts.tiles["pacman"], ts, animate=False), (32, 32)))

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
        player.add_component(GhostCollision([red, self.pinky, inky]))

    @staticmethod
    def red_find_target(pacman, field, pos):
        return pacman.get_component(TransformComponent).pos

    @staticmethod
    def vec2tuple(vec):
        return int(vec.x), int(vec.y)

    def find_cell_ahead(self, pac_pos, dir, field, distance):
        pdir = Vector2(dir.x, dir.y)
        start_pos = Vector2(pac_pos.x // field.size, pac_pos.y // field.size)
        cell_pos = Vector2(start_pos.x, start_pos.y)
        c_dirs = [Vector2(1, 0), Vector2(-1, 0), Vector2(0, 1), Vector2(0, -1)]
        for i in range(distance):
            cell = field.get_cell_iter(*self.vec2tuple(cell_pos))
            next_cell = field.get_cell_iter(*self.vec2tuple(cell_pos + dir))
            if (Meta.ghost_turn in cell.meta and not next_cell.state) or not cell.state:
                for c_dir in c_dirs:
                    new_pos = cell_pos + c_dir
                    if start_pos != cell_pos + c_dir and (c_dir.x != -pdir.x or c_dir.y != -pdir.y) \
                            and field.get_cell_iter(*self.vec2tuple(new_pos)).state:
                        dir = c_dir
            cell_pos += dir
        return cell_pos

    def pinky_find_target(self, pacman, field, pos):
        pac_pos = pacman.get_component(TransformComponent).pos
        dir = pacman.get_component(MoveComponent).direction
        cell_pos = self.find_cell_ahead(pac_pos, dir, field, 4)

        res_pos = cell_pos * field.size
        if pac_pos.distance_to(pos) < res_pos.distance_to(pos) and pac_pos.distance_to(pos) < 128:
            res_pos = pac_pos

        pacman.event_manager.trigger_event(DrawDebugLineEvent(
            self.create_rect_path(res_pos + Vector2(16, 16)),
            color=Colors.green))
        return res_pos

    def inky_find_target(self, pacman, field, pos):
        pac_pos = pacman.get_component(TransformComponent).pos
        dir = pacman.get_component(MoveComponent).direction
        cell_pos = self.find_cell_ahead(pac_pos, dir, field, 2)*field.size
        pinky_pos = self.pinky.get_component(TransformComponent).pos
        rs = cell_pos*2 - pinky_pos
        dst = cell_pos.distance_to(pinky_pos)
        for i in range(int(dst//field.size//2)):
            cell = field.get_cell(rs.lerp(cell_pos, 0.5+(i*field.size)/dst))
            if cell.state:
                rs = Vector2(*cell.rect.xy)
                break
            cell = field.get_cell(rs.lerp(cell_pos, 0.5-(i*field.size)/dst))
            if cell.state:
                rs = Vector2(*cell.rect.xy)
                break

        res_pos = rs
        if not field.get_cell(res_pos).state:
            res_pos = pac_pos

        pacman.event_manager.trigger_event(DrawDebugLineEvent(
            self.create_rect_path(res_pos + Vector2(16, 16)),
            color=Colors.red))
        pacman.event_manager.trigger_event(DrawDebugLineEvent(
            self.create_rect_path(cell_pos + Vector2(16, 16)),
            color=Colors.pink))
        pacman.event_manager.trigger_event(DrawDebugLineEvent([res_pos, cell_pos, pinky_pos], color=Colors.blue))
        return res_pos

    @staticmethod
    def create_rect_path(pos, size=10):
        offsets = [Vector2(size, size),
                   Vector2(size, -size),
                   Vector2(-size, -size),
                   Vector2(-size, size),
                   Vector2(size, size)]
        return [pos + off for off in offsets]
