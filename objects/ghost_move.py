from objects.ghost_base import GhostBase
from random import randint
from objects.base_cell import Meta, Wall
from pysmile.math.vector2 import Vector2


class GhostMove(GhostBase):
    def_texture = 'assets/images/ghosts/red.png'

    def __init__(self, game, field, x=32, y=32, base_speed=3, texture=def_texture):
        super().__init__(game, field)
        self.field = field
        self.stepback = 2
        self.wasd = 2
        self.speed = 2

    def checker(self):
        if self.wasd == 0:
            return self.field.get_cell(Vector2(self.rect.centerx - 32, self.rect.centery))

        elif self.wasd == 2:
            return self.field.get_cell(Vector2(self.rect.centerx + 32, self.rect.centery))

        elif self.wasd == 1:
            return self.field.get_cell(Vector2(self.rect.centerx, self.rect.centery - 32))

        elif self.wasd == 3:
            return self.field.get_cell(Vector2(self.rect.centerx, self.rect.centery + 32))

    def check(self):

        c = self.field.get_cell(Vector2( self.rect.centerx , self.rect.centery ))
        print(c)
        if len(c.meta) > 0 and Meta.ghost_turn in c.meta[0]:
            self.wasd = randint(0, 3)
            print("go")
            if self.wasd == self.stepback or isinstance(self.checker(), Wall):
                self.check()

    def go(self):
        if self.wasd == 0:
            self.rect.centerx -= self.speed

        elif self.wasd == 2:
            self.rect.centerx += self.speed

        elif self.wasd == 1:
            self.rect.centery -= self.speed

        elif self.wasd == 3:
            self.rect.centery += self.speed

    def process_logic(self):
        self.check()
        self.go()
