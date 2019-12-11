import pygame
import collections
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
        #Сохранить поле
        self.field = field
        self.last_pos = None

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
        goto = None
        min_dist = 10000
        for path in start.neighbours:
            path = path[0]
            if path.distance(goal) <= min_dist and path != self.last_pos:
                goto = path
                min_dist = path.distance(goal)

        self.last_pos = start
        goto = self.vert2vec(goto)
        return goto

# Пример использования
def main():
    # Инициализируем поисковик
    field = Field(None, 32, '../assets/maps/real_map.txt')

    finder = Afinder(field)
    # Можно использовать несколько поисковиков
    aggr_finder = Afinder(field)

    # Точки
    start = Vector2()
    goal = Vector2()
    start[:] = 100, 100
    goal[:] = 500,500

    # Поиск пути
    path = finder.find_path(start, goal)
    print(path)
    """(8, 10)
       (6, 14)
       (6, 6)"""

if __name__ == '__main__':
    main()


