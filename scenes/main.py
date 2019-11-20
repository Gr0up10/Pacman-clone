import pygame
from constants import Color
from objects.balls import LinearMovingBall
from objects.ghost_base import GhostBase
from scenes.base import Scene
from objects.grain import Grain


class MainScene(Scene):
    def create_objects(self):
        self.add_entity(GhostBase(self.game))
        self.add_entity(Grain(self.game))
