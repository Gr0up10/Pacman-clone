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


class Graph:
    def __init__(self, game, field_size=32):
        self.field = Field(game, field_size)
        self.verts = []
        self.width = len(self.field.matrix[len(self.field.matrix)-1])
        self.height = len(self.field.matrix)
        pass

    def generate(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if Meta.ghost_turn in self.field.map[y][x].meta:
                    self.verts.append(Vert(x, y))

        for vert in self.verts:
            neighbours = [check_for_horizontal_neighbours(self.field.map, vert.x, vert.y, self.width, 1),
                          check_for_horizontal_neighbours(self.field.map, vert.x, vert.y, self.width, -1),
                          check_for_vertical_neighbours(self.field.map, vert.x, vert.y, self.height, 1),
                          check_for_vertical_neighbours(self.field.map, vert.x, vert.y, self.height, -1)]

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

    def get_vert(self, x, y):
        for i in self.verts:
            if i.x == x and i.y == y:
                return i
        return None


def main():
    # Тестовый запуск: генерирует граф, отрисовыввает его в консоли и выдает соседи 1 точки
    game = pygame.init()
    g = Graph(game=game)
    g.generate()

    for i in range(0, g.height):
        for j in range(0, g.width):
            if g.is_vert(j, i):
                print("0", end="")
            else:
                print("-", end="")
        print("\n", end="")

    print(g.get_vert(6, 1).get_all_neighbours())


if __name__ == '__main__':
    main()
