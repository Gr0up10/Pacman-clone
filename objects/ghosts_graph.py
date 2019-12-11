import pygame
from pysmile.math.vector2 import Vector2

from objects.base_cell import Cell, Meta
from objects.field import Field
from math import sqrt


class Vert:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = []

    @property
    def vector(self):
        return Vector2(self.x, self.y)

    def get_neighbour(self, x, y):
        for i in self.neighbours:
            if i[0].x == x and i[1].y == y:
                return i
        return None

    def equal(self,b):
        if self.x == b.x and self.y == b.y:
            return True
        return False

    # Функция возвращает растояние между двумя Vert()
    def distance(self, b):
        (x1, y1) = self.x, self.y
        (x2, y2) = b.x, b.y
        return sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))


class Graph:
    def __init__(self, field):
        self.field = field
        self.verts = []
        self.width = len(self.field.matrix[len(self.field.matrix) - 1])
        self.height = len(self.field.matrix)

    def generate(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if Meta.ghost_turn in self.field.map[y][x].meta:
                    self.verts.append(Vert(x, y))

        for vert in self.verts:
            neighbours = self.find_neighbours(vert.x, vert.y)
            for i in neighbours:
                if i is not None:
                    for v in self.verts:
                        if v.x == i[0] and v.y == i[1]:
                            vert.neighbours.append((v, i[2]))
                            break
        return True

    def check_tile(self, x, y):
        map_obj = self.field.map
        if not map_obj[y][x].state:
            return -1
        if Meta.ghost_turn in map_obj[y][x].meta:
            return x, y

    def find_neighbours(self, x, y):
        map_obj = self.field.map
        width = len(map_obj[0])
        height = len(map_obj)
        res = [None for _ in range(4)]
        can_go = [True for _ in range(4)]
        for i in range(1, max(width, height)):
            if x + i < width and not res[0] and can_go[0]:
                tile = self.check_tile(x + i, y)
                if tile == -1:
                    can_go[0] = False
                elif tile:
                    res[0] = tile + (i,)
            if x - i >= 0 and not res[1] and can_go[1]:
                tile = self.check_tile(x - i, y)
                if tile == -1:
                    can_go[1] = False
                elif tile:
                    res[1] = tile + (i,)
            if y + i < height and not res[2] and can_go[2]:
                tile = self.check_tile(x, y + i)
                if tile == -1:
                    can_go[2] = False
                elif tile:
                    res[2] = tile + (i,)
            if y - i >= 0 and not res[3] and can_go[3]:
                tile = self.check_tile(x, y - i)
                if tile == -1:
                    can_go[3] = False
                elif tile:
                    res[3] = tile + (i,)
        return res

    def is_vert(self, x, y):
        for i in self.verts:
            if i.x == x and i.y == y:
                return True
        return False

    def get_vert_by_coord(self, x, y):
        for i in self.verts:
            if i.x == x and i.y == y:
                return i
        return None

    def get_vert(self, vert):
        x = vert.x
        y = vert.y
        return self.get_vert_by_coord(x, y)


# Заменить в field ../ на ./
def main():
    # Тестовый запуск: генерирует граф, отрисовыввает его в консоли и выдает соседи 1 точки
    g = Graph(Field(None, 32, '../assets/maps/real_map.txt'))
    g.generate()
    a = g.get_vert_by_coord(23, 20)
    print('All verts:')
    for i in g.verts:
        print("({}, {})".format(i.x, i.y))

    print('neighbours: ')
    for i in a.neighbours :
        print("({}, {})".format(i[0].x, i[0].y))

    for i in range(0, g.height):
        for j in range(0, g.width):
            if a.x == j and a.y == i:
                print("1", end="")
            elif g.is_vert(j, i):
                print("0", end="")
            elif not g.field.get_cell_iter(j, i).state:
                print("#", end="")
            else:
                print("-", end="")
        print("\n", end="")


if __name__ == '__main__':
    main()
