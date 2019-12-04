
class Vert:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = []

    def add_neighbour(self, x, y, dist):
        self.neighbours.append((x, y, dist))

    def get_neighbours(self):
        return self.neighbours


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

        self.width = len(map_raw[0])
        self.height = len(map_raw)

        for y in range(0, self.height):
            for x in range(0, self.width):
                if map_raw[y][x] == "W":
                    self.walls.append((x, y))
                if map_raw[y][x] == "C" or map_raw[y][x] == "T":
                    self.verts.append(Vert(x, y))

        for vert in self.verts:
            dist = 0
            for x in range(vert.x + 1, self.width):
                dist += 1
                if map_raw[vert.y][x] == "W":
                    break
                if map_raw[vert.y][x] == "C" or map_raw[vert.y][x] == "T":
                    vert.add_neighbour(x, vert.y, dist)

            dist = 0
            for x in range(vert.x - 1, 0):
                dist += 1
                if map_raw[vert.y][x] == "W":
                    break
                if map_raw[vert.y][x] == "C" or map_raw[vert.y][x] == "T":
                    vert.add_neighbour(x, vert.y, dist)

            dist = 0
            for y in range(vert.y + 1, self.height):
                dist += 1
                if map_raw[y][vert.x] == "W":
                    break
                if map_raw[y][vert.x] == "C" or map_raw[y][vert.x] == "T":
                    vert.add_neighbour(vert.x, y, dist)

            dist = 0
            for y in range(vert.y - 1, 0):
                dist += 1
                if map_raw[y][vert.x] == "W":
                    break
                if map_raw[y][vert.x] == "C" or map_raw[y][vert.x] == "T":
                    vert.add_neighbour(vert.x, y, dist)

        map_file.close()
        return True
