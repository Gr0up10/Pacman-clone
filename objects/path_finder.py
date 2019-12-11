import pygame
import collections

from objects.base_cell import GhostDoor, Meta
from objects.ghosts_graph import Graph, Vert
from pysmile.math.vector2 import Vector2

# Класс представляет собой "обёртку" для стокового deque. Работает как "Первый вошёл, первый вышел"
from objects.field import Field


class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()


# Основной класс, который обрабатывает поиск по карте
class Afinder:
    def __init__(self, field):
        # Создать граф
        self.graph = Graph(field)
        self.graph.generate()
        # Сохранить поле
        self.field = field

    def vec2vert(self, vec):
        size = self.graph.field.size
        return Vert(vec.x // size, vec.y // size)

    def vert2vec(self, vert):
        return vert.vector*self.graph.field.size

    """ Основная функция, для поиска пути использовать её.
        start_coord = перекрёсток, на котором гост сейчас,
        goal_coord  = позиция пакмена"""
    def find_path(self, start_coord, goal_coord):

        start = self.vec2vert(start_coord)
        goal = self.vec2vert(goal_coord)

        start = self.graph.get_vert(start)

        if not start:
            return self.vert2vec(self.find_closest_vert(start_coord))

        goto = start
        min_dist = 1000
        for path in start.neighbours:
            path = path[0]
            if path.distance(goal) < min_dist:
                goto = path
                min_dist = path.distance(goal)

        goto = self.vert2vec(goto)
        return goto

    def find_closest_vert(self, point):
        current = Vector2(point.x//self.field.size, point.y//self.field.size)
        dirs = [Vector2(0, 1), Vector2(0, -1), Vector2(1, 0), Vector2(-1, 0)]
        for i in range(1, max(len(self.field.matrix), len(self.field.matrix[0]))):
            dirs = [d for d in dirs if not self.field.get_cell(d*i + current).state]
            for d in dirs:
                cur = d*i + current
                if Meta.ghost_turn in self.field.get_cell_iter(int(cur.x), int(cur.y)).meta:
                    return self.graph.get_vert_by_coord(cur.x, cur.y)


# Пример использования
def main():
    # Инициализируем поисковик
    field = Field(None, 32, '../assets/maps/real_map.txt')

    finder = Afinder(field)
    # Можно использовать несколько поисковиков
    _ = Afinder(field)

    # Точки
    start = Vector2()
    goal = Vector2()
    start[:] = 100, 100
    goal[:] = 500, 500

    # Поиск пути
    path = finder.find_path(start, goal)
    print(path)
    """(8, 10)
       (6, 14)
       (6, 6)"""


if __name__ == '__main__':
    main()


