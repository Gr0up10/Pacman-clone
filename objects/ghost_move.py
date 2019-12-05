from objects.ghost_base import GhostBase
from random import randint
from objects.base_cell import Meta, Wall, Floor
from pysmile.math.vector2 import Vector2


class GhostMove(GhostBase):
    def_texture = 'assets/images/ghosts/red.png'
    speed = 3
    checker_offset = -16
    check_offset = 32

    def __init__(self, game, field, time_lock=60, time_lock_limit=20, speed=3, x=48, y=48, texture=def_texture):
        super().__init__(game, x, y, texture)
        self.field = field
        self.stepback = 2  # направление обратное васду (для того чтобы гост не пошел назад)
        self.wasd = 0  # напровлеие движа
        '''
        0-лево
        1-вверх
        2-право
        3-вниз
        '''
        self.speed = speed  # cкорость можно изменять
        # время которое должно пройти после поворота для предотвращения повторного вызова функции
        self.time_lock = time_lock
        self.time_lock_limit = time_lock_limit

    def checker(self, r):
        if self.wasd == 0:
            return self.field.get_cell(Vector2(self.rect.centerx - r, self.rect.centery))

        elif self.wasd == 2:
            return self.field.get_cell(Vector2(self.rect.centerx + r, self.rect.centery))

        elif self.wasd == 1:
            return self.field.get_cell(Vector2(self.rect.centerx, self.rect.centery - r))

        elif self.wasd == 3:
            return self.field.get_cell(Vector2(self.rect.centerx, self.rect.centery + r))

    def check(self):
        v = False
        c = self.checker(self.checker_offset)  # значение меты
        if (c.meta is not None and Meta.ghost_turn in c.meta) \
                and self.time_lock >= self.time_lock_limit * 2 / self.speed:
            self.wasd = randint(0, 3)
            while not v:
                if (self.wasd == self.stepback or isinstance(self.checker(self.check_offset), Wall)) \
                        and self.time_lock >= self.time_lock_limit / self.speed:
                    self.wasd = randint(0, 3)
                else:
                    v = True
                    self.time_lock = 0
                    if self.wasd == 3 or self.wasd == 2:
                        self.stepback = abs(self.wasd - 2)
                    else:
                        self.stepback = self.wasd + 2
        else:
            self.teleport()

    def go(self):
        if self.wasd == 0:
            self.rect.centerx -= self.speed

        elif self.wasd == 2:
            self.rect.centerx += self.speed

        elif self.wasd == 1:
            self.rect.centery -= self.speed

        elif self.wasd == 3:
            self.rect.centery += self.speed

        self.time_lock += 1

    def teleport(self):
        c = self.checker(self.check_offset)  # значение меты
        if c.meta is not None and Meta.teleport2 in c.meta:
            pos = self.field.get_cells_by_type(Floor, Meta.teleport1)[0].rect
            self.rect.centerx = pos.centerx
            self.rect.centery = pos.centery
        elif c.meta is not None and Meta.teleport1 in c.meta:
            pos = self.field.get_cells_by_type(Floor, Meta.teleport2)[0].rect
            self.rect.centerx = pos.centerx
            self.rect.centery = pos.centery

    def process_logic(self):
        self.check()
        self.go()
