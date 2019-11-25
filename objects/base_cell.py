import pygame
from objects.base import DrawObject
from pysmile.math.rect import Rect


# Класс Базовая клетка, при создании получает: x, y - координаты; state - стена или нет; size - размер клетки
class Cell(DrawObject):

    def __init__(self, game, x, y, state, size):
        super().__init__(game)

        self.rect = Rect((x, y), (size, size))
        self.x = x
        self.y = y
        self.state = state
        self.size = size


# Производный класс Стены, отрисовывается
class Wall(Cell):
    def process_draw(self):
        pygame.draw.rect(self.game.screen, (255, 0, 0), self.rect, 0)


# Производный класс Пола, не отрисовывается
class Floor(Cell):
    def process_draw(self):
        pass
