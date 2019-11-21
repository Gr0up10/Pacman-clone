import pygame
from objects.base import DrawObject


# Класс Базовая клетка, при создании получает: x, y - координаты; state - стена или нет; size - размер клетки
class Cell(DrawObject):

    def __init__(self, game, x, y, state, size):
        super().__init__(game)

        self.rect = pygame.Rect((x, y), (size, size))
        self.x = x
        self.y = y
        self.state = state
        self.size = size


# Производный класс Стены, отрисовывается
class Wall(Cell):
    def process_draw(self):
        pygame.draw.rect(self.game.screen, (100, 100, 255), self.rect, 0)


# Производный класс Пола, не отрисовывается
class Floor(Cell):
    def process_draw(self):
        pass
