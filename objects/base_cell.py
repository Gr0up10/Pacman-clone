import pygame
from objects.base import DrawObject

class Cell(DrawObject):
    def __init__(self, game, x, y, state, size, filename):
        super().__init__(game)

        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()

        self.state = state
        #????
        self.width = size
        self.height = size
        self.rect.x = x
        self.rect.y = y

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)