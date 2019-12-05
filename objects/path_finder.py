import pygame
import collections
from ghosts_graph import Graph, Vert


class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()

class A_finder:
    def __init__(self, game):
        #Создаём очередь для Vert
        self.frontier = Queue()
        #Может нужно не здесь инициировать? Зачем инициировать пустую visited?
        self.visited = {}
        #Создаём граф
        self.graph = Graph(game=game)
        #Генерим его
        self.graph.generate()
    #Найти путь между A и B (Заменить x1, y1, x2, y2 на start(vert) и goal(vert)
    def find_path(self, x1,y1 , x2, y2):
        #Временное
        start = self.graph.get_vert_by_coord(x1, y1)
        goal = self.graph.get_vert_by_coord(x2, y2)
        #Добавляем "начальную точку" в начало очереди
        self.frontier.put(start)
        #Сохранение предыдущих путей
        came_from = {}
        came_from[start] = None

        #Пока не прошли все Vert на карте(или не нашли нужную)
        while not self.frontier.empty():
            # current на начале = 1,1
            current = self.frontier.get()
            #Если есть соседи(прочекать эту проверку)
            if self.graph.get_vert(current).neighbours is not None:
                #Проходим по всем соседям
                for next in self.graph.get_vert(current).neighbours:
                    #В коде ghosts_graph возвращается tuple, где [0] - это Vert, а [1] какое-то число(может позиция в сетке)
                    #Если ещё не были здесь
                    if next[0] not in came_from:
                        #Добавляем Этот Vert в проходку
                        self.frontier.put(next[0])
                        #Говорим "откуда пришли"
                        came_from[next[0]] = current
            #Сам алгоритм поиска пути по прошедшему в обратном направлении, от goal до start
            current = goal
            #Начинаем путь с конца, созадём список с одним элементом
            path = [current]
            #Пока не пришли в начало
            while current != start:
                current = came_from[current]
                path.append(current)
        #Тестовый вывод выводит с конца в начало
        print(path[0].x, path[0].y, path[1].x, path[1].y)
def main():
    game = pygame.init()
    graph = Graph(game=game)
    finder = A_finder(game)
    finder.find_path(1,1, 6,1)
    for i in range(0, graph.height):
        for j in range(0, graph.width):
            if graph.is_vert(j, i):
                print("0", end="")
            else:
                print("-", end="")
        print("\n", end="")


if __name__ == '__main__':
    main()

