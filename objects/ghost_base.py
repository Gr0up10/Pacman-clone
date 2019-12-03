from random import randint
import pygame

from objects.base import DrawObject


class GhostBase(DrawObject):
    def_texture = 'assets/images/ghosts/red.png'
    scared_speed_devider = 2

    def __init__(self, game, x=32, y=32, base_speed=3, texture=def_texture):
        super().__init__(game)

        self.image = pygame.image.load(texture)
        self.rect = self.image.get_rect()

        self.x = 48
        self.y = 48
        self.rect.centerx = self.x
        self.rect.centery = self.y

        self.window_width = self.game.width
        self.window_height = self.game.height
        self.shift_x = base_speed
        self.shift_y = base_speed
        self.scared_status = False

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)

    def collides_with(self, obj):
        return pygame.sprite.collide_mask(self, obj)

class GhostBaseScared(GhostBase):
    def_texture = 'assets/images/ghosts/afraid_0.png'

    def __init__(self, game, x=100, y=100, base_speed=1):
        super().__init__(game, x, y, base_speed, GhostBaseScared.def_texture)
