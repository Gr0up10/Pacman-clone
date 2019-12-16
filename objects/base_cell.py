import enum
import pygame
from objects.base import DrawObject
from pysmile.math.rect import Rect


class Meta(enum.Enum):
    none = 0
    pacman_spawn = 1
    ghost_turn = 2
    grain_small = 3
    grain_big = 4
    teleport1 = 5
    teleport2 = 6
    ghost_spawn = 7


# Класс Базовая клетка, при создании получает: x, y - координаты; state - стена или нет; size - размер клетки
class Cell(DrawObject):

    def __init__(self, game, x, y, state, size, meta=Meta.none):
        # meta - additional information that can be used to, for example, set up spawn positions
        super().__init__(game)

        self.rect = Rect((x, y), (size, size))
        self.x = x
        self.y = y
        self.state = state
        self.size = size
        self.meta = []
        if isinstance(meta, list):
            self.meta = meta
        else:
            self.meta.append(meta)


# Производный класс Стены, отрисовывается
class Wall(Cell):
    def process_draw(self):
        pygame.draw.rect(self.game.screen, (255, 0, 0), self.rect, 0)


class GhostDoor(Cell):
    def process_draw(self):
        pygame.draw.rect(self.game.screen, (0, 0, 255), pygame.Rect(self.rect.x-self.size*0.2, self.rect.y,
                                                                    self.rect.w+self.size*0.2, self.rect.h), 0)


# Производный класс Пола, не отрисовывается
class Floor(Cell):
    def process_draw(self):
        pass
