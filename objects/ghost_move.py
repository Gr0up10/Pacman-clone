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
        self.speed = 3
        self.time_lock=60

    def checker(self,r):
        if self.wasd == 0:
            return self.field.get_cell(Vector2(self.rect.centerx - r, self.rect.centery))

        elif self.wasd == 2:
            return self.field.get_cell(Vector2(self.rect.centerx + r, self.rect.centery))

        elif self.wasd == 1:
            return self.field.get_cell(Vector2(self.rect.centerx, self.rect.centery - r))

        elif self.wasd == 3:
            return self.field.get_cell(Vector2(self.rect.centerx, self.rect.centery + r))

    def check(self):
        v=False
        c = self.checker(-16)
        if (c.meta is not None and Meta.ghost_turn in c.meta )and self.time_lock>=40/self.speed:
            self.wasd = randint(0, 3)
            while v==False :
                if (self.wasd == self.stepback or isinstance(self.checker(32), Wall))and self.time_lock>=20/self.speed:
                    self.wasd = randint(0, 3)
                else:
                    v=True
                    self.time_lock=0
                    if self.wasd==3 or self.wasd==2 :
                        self.stepback=abs(self.wasd - 2)
                    else:
                        self.stepback=self.wasd+2

    def go(self):
        if self.wasd == 0:
            self.rect.centerx -= self.speed

        elif self.wasd == 2:
            self.rect.centerx += self.speed

        elif self.wasd == 1:
            self.rect.centery -= self.speed

        elif self.wasd == 3:
            self.rect.centery += self.speed

        self.time_lock+=1

    def process_logic(self):
        self.check()
        self.go()
