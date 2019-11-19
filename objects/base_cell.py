import pygame
from objects.base import DrawObject

class Cell(DrawObject):
    def __init__(self, game, x, y, state, size):
        super().__init__(game)

        self.rect = pygame.Rect((x,y), (size, size))
        self.state = state
        self.size = size
        #????
        self.width = size
        self.height = size

        # pygame.draw.line(self.game.screen, (100,100,255), (self.rect.x + 0.5*(self.size), self.rect.y),
        #                                                  (self.rect.x + 0.5*(self.size), self.rect.y+self.size))
        # self.game.screen.blit(self.image, self.rect)

class UnWalkableCell(Cell):
    def process_draw(self):
        pygame.draw.rect(self.game.screen, (100, 100, 255), self.rect, 0)

class WalcableCell(Cell):
    def process_draw(self):
        pass