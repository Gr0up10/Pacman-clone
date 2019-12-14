import pygame

from objects.base import DrawObject


class Grain(DrawObject):
    filename = 'assets/images/small_grain.png'

    def __init__(self, game, x=400, y=300):
        super().__init__(game)
        self.image = pygame.image.load(Grain.filename)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.x = x
        self.y = y

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)


class BigGrain(DrawObject):
    filename = 'assets/images/big_grain.png'

    def __init__(self, game, x=200, y=100):
        super().__init__(game)
        self.image = pygame.image.load(BigGrain.filename)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.x = x
        self.y = y

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)
