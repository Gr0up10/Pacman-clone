from random import randint
import pygame

from objects.base import DrawObject


class GhostBase(DrawObject):
    def_texture = 'assets/images/ghost.png'
    scared_speed_devider = 2

    def __init__(self, game, x=100, y=100, base_speed=3, texture=def_texture):
        super().__init__(game)

        self.image = pygame.image.load(texture)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.x = x
        self.y = y

        self.window_width = self.game.width
        self.window_height = self.game.height
        self.shift_x = base_speed
        self.shift_y = base_speed
        self.scared_status = False

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)

    def collides_with(self, obj):
        return pygame.sprite.collide_mask(self, obj)

    # Дефолтное поведение - рандомные направления
    def process_logic(self):
        self.shift_x = 1 if randint(0, 1) == 1 else -1
        self.shift_y = 1 if randint(0, 1) == 1 else -1

        self.rect.x += self.shift_x
        self.rect.y += self.shift_y
        if self.rect.left <= 0 or self.rect.right >= self.window_width:
            self.shift_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= self.window_height:
            self.shift_y *= -1


class GhostBaseScared(GhostBase):
    def_texture = 'assets/images/ghost_scared.png'

    def __init__(self, game, x=100, y=100, base_speed=1):
        super().__init__(game, x, y, base_speed, GhostBaseScared.def_texture)
