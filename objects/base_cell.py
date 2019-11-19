import pygame
from objects.base import DrawObject

class Cell(DrawObject):
    def __init__(self, game, x, y, state, size, filename):
        super().__init__(game)

        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (size,size))
        self.rect = self.image.get_rect()
        self.state = state
        self.size = size
        #????
        self.width = size
        self.height = size
        self.rect.x = x
        self.rect.y = y

    def process_draw(self):
        pygame.draw.rect(self.game.screen, (100, 100, 255), self.rect, 0)
        # pygame.draw.line(self.game.screen, (100,100,255), (self.rect.x + 0.5*(self.size), self.rect.y),
        #                                                  (self.rect.x + 0.5*(self.size), self.rect.y+self.size))
        # self.game.screen.blit(self.image, self.rect)