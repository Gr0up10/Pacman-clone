import pygame
import collections
from math import sqrt
from ghosts_graph import Graph, Vert

# Класс представляет собой "обёртку" для стокового deque. Работает как "Первый вошёл, первый вышел"
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
    def __init__(self, game):
        # Посещённые вершины
        self.frontier = Queue()
        # Создать граф
        self.graph = Graph(game=game)
        self.graph.generate()

    # Основная функция, для поиска пути использовать её. start/end_coord - кортежи координат (x,y)
    def find_path(self, start_coord , goal_coord):

        real_start = Vert(*start_coord)
        real_goal = Vert(*goal_coord)

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
        path = self.create_route(came_from, goal, start, real_start, real_goal)
        return path

    # Создаём путь от обратного(от goal до start) и разворачиваем его
    def create_route(self, came_from, goal, start, real_start, real_goal):
        current = goal

        # Начинаем путь с конца(настоящей точки, а не ближайшей из графа), создаём список с одним элементом
        path = [real_goal]

        while current != start:
            current = came_from[current]
            path.append(current)

        # Добавляем настоящую стартовую позицию
        path.append(real_start)

        # Разворачиваем, чтобы начинать со real_start
        path.reverse()

        # Возвращаем список Vert()
        return path

    # Находим ближайшую точку из графа по расстанию из heuristic()
    def find_closest_vert(self, point):
        min_len = 1000
        closest_vert = None

        for vert in self.graph.verts:
            if heuristic(point, vert) < min_len:
                min_len = heuristic(point, vert)
                closest_vert = vert

        return closest_vert

# Функция возвращает растояние между двумя Vert()
def heuristic( a, b):
    (x1, y1) = a.x, a.y
    (x2, y2) = b.x, b.y
    return sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
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
    finder = Afinder(game)
    # Можно использовать несколько поисковиков
    aggr_finder = Afinder(game)

    # Точки
    start= (0,0)
    goal = (20,21)
    goal2 = (10, 12)
    # Поиск пути
    path = finder.find_path(start, goal)
    path2 = aggr_finder.find_path(start, goal2)

    # Вывод в терминал(для проверки)
    print_path_on_map(finder, path)
    print_path_on_map(aggr_finder, path2)

if __name__ == '__main__':
    main()
