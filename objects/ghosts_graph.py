import pygame
from objects.base_cell import Cell, Meta
from objects.field import Field


class Vert:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = []

    def get_neighbour(self, x, y):
        for i in self.neighbours:
            if i[0].x == x and i[1].y == y:
                return i
        return None
    def equal(self,b):
        if self.x == b.x and self.y == b.y:
            return True
        return False

def check_for_horizontal_neighbours(map_obj, x, y, width, direction):
    dist = 0
    for xx in range(x + direction, width if direction > 0 else 0, direction):
        dist += 1
        if not map_obj[y][xx].state:
            return None
        if Meta.ghost_turn in map_obj[y][xx].meta:
            return xx, y, dist


def check_for_vertical_neighbours(map_obj, x, y, height, direction):
    dist = 0
    for yy in range(y + direction, height if direction > 0 else 0, direction):
        dist += 1
        if not map_obj[yy][x].state:
            return None
        if Meta.ghost_turn in map_obj[yy][x].meta:
            return x, yy, dist

def check_tile(map_obj, x, y):
    if not map_obj[y][x].state:
        return None
    if Meta.ghost_turn in map_obj[y][x].meta:
        return x, y

def find_neighbours(map_obj, x, y):
    width = len(map_obj[0])
    height = len(map_obj)
    res = [None for _ in range(4)]
    for i in range(1, max(width, height)):
        if x + i < width and not res[0]:
            tile = check_tile(map_obj, x + i, y)
            if tile:
                res[0] = tile + (i,)
        if x - i >= 0 and not res[1]:
            tile = check_tile(map_obj, x - i, y)
            if tile:
                res[1] = tile + (i,)
        if y + i < height and not res[2]:
            tile = check_tile(map_obj, x, y + i)
            if tile:
                res[2] = tile + (i,)
        if y -i >= 0 and not res[3]:
            tile = check_tile(map_obj, x, y - i)
            if tile:
                res[3] = tile + (i,)
    return res

class Graph:
    def __init__(self, game, field_size=32):
        self.field = Field(game, field_size)
        self.verts = []
        self.width = len(self.field.matrix[len(self.field.matrix) - 1])
        self.height = len(self.field.matrix)

    def generate(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if Meta.ghost_turn in self.field.map[y][x].meta:
                    self.verts.append(Vert(x, y))

        for vert in self.verts:
            #neighbours = [check_for_horizontal_neighbours(self.field.map, vert.x, vert.y, self.width, 1),
            #              check_for_horizontal_neighbours(self.field.map, vert.x, vert.y, self.width, -1),
            #              check_for_vertical_neighbours(self.field.map, vert.x, vert.y, self.height, 1),
            #              check_for_vertical_neighbours(self.field.map, vert.x, vert.y, self.height, -1)]
            neighbours = find_neighbours(self.field.map, vert.x, vert.y)
            for i in neighbours:
                if i is not None:
                    for v in self.verts:
                        if v.x == i[0] and v.y == i[1]:
                                vert.neighbours.append((v, i[2]))
                                break
        return True

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
    game = pygame.init()
    g = Graph(game=game)
    g.generate()
    a = g.get_vert_by_coord(23,20)
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
