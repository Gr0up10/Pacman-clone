import pygame
import collections
from objects.ghosts_graph import Graph, Vert


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
        # Посещённые вершины
        self.frontier = Queue()
        # Создать граф
        self.graph = Graph(field)
        self.graph.generate()

    def vec2vert(self, vec):
        size = self.graph.field.size
        return Vert(vec.x // size, vec.y // size)

    def vert2vec(self, vert):
        return vert.vector*self.graph.field.size

    # Основная функция, для поиска пути использовать её. start/end_coord - кортежи координат (x,y)
    def find_path(self, start_coord, goal_coord):
        real_start = self.vec2vert(start_coord)
        real_goal = self.vec2vert(goal_coord)

        # Ближайшие вершины из нашего графа
        start = self.find_closest_vert(real_start)
        goal = self.find_closest_vert(real_goal)

        # Добавляем "начальную точку" в начало очереди
        self.frontier.put(start)

        # Сохранение предыдущих путей
        came_from = {}
        came_from[start] = None

        while not self.frontier.empty():
            current = self.frontier.get()

            for next in self.graph.get_vert(current).neighbours:

                # В коде ghosts_graph возвращается tuple, где [0] - это Vert, а [1] какое-то число
                if next[0] not in came_from:
                    # Добавляем Этот Vert в проход
                    self.frontier.put(next[0])

                    # Говорим "откуда пришли"
                    came_from[next[0]] = current

        # Создание пути по "проходу"
        path = self.create_route(came_from, goal, start, start_coord, real_goal)
        return path

    # Создаём путь от обратного(от goal до start) и разворачиваем его
    def create_route(self, came_from, goal, start, start_coord, real_goal):
        current = goal

        # Начинаем путь с конца(настоящей точки, а не ближайшей из графа), создаём список с одним элементом
        path = [self.vert2vec(real_goal)]
        while current != start:
            ncurrent = came_from[current]
            # Если реальный старт ближе к следующей вершине то выбираем его
            if ncurrent == start:
                cur_vec = self.vert2vec(current)
                next_vec = self.vert2vec(ncurrent)
                if cur_vec.distance_to(start_coord) < cur_vec.distance_to(next_vec):
                    print("choose")
                    break

            path.append(self.vert2vec(ncurrent))
            current = ncurrent

        # Добавляем настоящую стартовую позицию
        #path.append(real_start)

        # Разворачиваем, чтобы начинать со real_start
        path.reverse()

        # Возвращаем список Vert()
        return path

    # Находим ближайшую точку из графа по расстанию из heuristic()
    def find_closest_vert(self, point):
        min_len = 1000
        closest_vert = None

        for vert in self.graph.verts:
            if point.distance(vert) < min_len:
                min_len = point.distance(vert)
                closest_vert = vert

        return closest_vert


# Функция выводит путь по координатам
def print_path(path):
    for i in path:
        print("({}, {})".format(i.x, i.y))
    print('')


# Функция рисует путь на "карте"
def print_path_on_map(finder, path):
    graph = finder.graph
    print_path(path)
    for i in range(graph.height):
        for j in range(graph.width):
            check = False
            for k in path:
                if Vert(j, i).equal(k):
                    check = True
            if check:
                print("!", end="")
            elif graph.is_vert(j,i):
                print("0", end="")
            else:
                print("-", end="")
        print('')
    print('')


# Пример использования
def main():

    game = pygame.init()
    # Инициализируем поисковик
    finder = Afinder(Field(game, 32, '../assets/maps/real_map.txt'))
    # Можно использовать несколько поисковиков
    aggr_finder = Afinder(Field(game, 32, '../assets/maps/real_map.txt'))

    # Точки
    start = (1, 1)
    goal = (23, 20)
    #goal2 = (10, 12)
    # Поиск пути
    path = finder.find_path(start, goal)
    #path2 = aggr_finder.find_path(start, goal2)

    # Вывод в терминал(для проверки)
    print_path_on_map(finder, path)
    #print_path_on_map(aggr_finder, path2)


if __name__ == '__main__':
    main()
