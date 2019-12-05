"""
    - В качестве "имен" точек в графе используются их координаты от левого верхнего угла карты (как в pygame)
    - Граф генерируется автоматически основываясь на карте, создавая точки из клеток, помеченных как C, R и T
    - Точки хранятся в виде списка, т.е. у каждой точки есть массив ее соседей с элементами вида
        (*координата X соседа*, *координата Y соседа*, *число шагов до соседа*)
"""


class Vert:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = []

    def get_all_neighbours(self):
        return self.neighbours

    def get_distance_to(self, x, y):
        for i in self.neighbours:
            if i[0] == x and i[1] == y:
                return i[2]
        return None


def check_for_horizontal_neighbours(map_raw, x, y, width, direction):
    dist = 0
    for xx in range(x + direction, width if direction > 0 else 0, direction):
        dist += 1
        if map_raw[y][xx] == "W":
            return None
        if map_raw[y][xx] == "C" or map_raw[y][xx] == "T" or map_raw[y][xx] == "R":
            return xx, y, dist


def check_for_vertical_neighbours(map_raw, x, y, height, direction):
    dist = 0
    for yy in range(height if direction > 0 else 0, y + direction, direction):
        dist += 1
        if map_raw[yy][x] == "W":
            return None
        if map_raw[yy][x] == "C" or map_raw[yy][x] == "T" or map_raw[yy][x] == "R":
            return x, yy, dist

class Graph:

    def __init__(self):
        self.verts = []
        self.walls = []
        self.width = 0
        self.height = 0
        pass

    def generate(self, map_path):
        try:
            map_file = open(map_path, "r")
        except FileNotFoundError:
            return False

        map_raw = map_file.readlines()

        self.height = len(map_raw)
        self.width = len(map_raw[len(map_raw)-1])

        for y in range(0, self.height):
            for x in range(0, self.width):
                if map_raw[y][x] == "W":
                    self.walls.append((x, y))
                if map_raw[y][x] == "C" or map_raw[y][x] == "T" or map_raw[y][x] == "R":
                    self.verts.append(Vert(x, y))

        for vert in self.verts:
            neighbours = [check_for_horizontal_neighbours(map_raw, vert.x, vert.y, self.width, 1),
                          check_for_horizontal_neighbours(map_raw, vert.x, vert.y, self.width, -1),
                          check_for_vertical_neighbours(map_raw, vert.x, vert.y, self.width, 1),
                          check_for_vertical_neighbours(map_raw, vert.x, vert.y, self.width, -1)]

            for i in neighbours:
                if i is not None:
                    for v in self.verts:
                        if v.x == i[0] and v.y == i[1]:
                                vert.neighbours.append((v, i[2]))
                                break



        map_file.close()
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
    g = Graph()
    g.generate("../assets/maps/real_map.txt")

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
